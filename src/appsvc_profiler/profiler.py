import logging
import random
import subprocess 
import string
import sys
import shutil

from .constants import CodeProfilerConstants
from datetime import datetime, timezone
from time import sleep
from os import makedirs, path, rename, environ
from pathlib import Path
from textwrap import wrap
from rich.console import Console

console = Console()
logger = logging.getLogger(__name__)
constants = CodeProfilerConstants()

WAIT_FOR_VIZTRACER_TO_SAVE_TRACE_TIMEOUT=environ.get(constants.APP_SETTING_TO_SET_SAVE_TRACE_MAX_TIMEOUT, 60)
WAIT_FOR_VIZTRACER_TO_SAVE_TRACE_MAX_TIMEOUT=180
if WAIT_FOR_VIZTRACER_TO_SAVE_TRACE_TIMEOUT > WAIT_FOR_VIZTRACER_TO_SAVE_TRACE_MAX_TIMEOUT :
    WAIT_FOR_VIZTRACER_TO_SAVE_TRACE_TIMEOUT=180

class ViztracerCodeProfiler():
    def __init__(self,pid, time_to_profile=0) -> None:
        self.pid = pid
        self.time_to_profile = time_to_profile        
        
    def generate_command(self):
        args = ["viztracer","--attach", str(self.pid)]
        
        if self.time_to_profile > 0:
            args.append("-t")
            args.append(str(self.time_to_profile))
        
        return args
    
class CodeProfiler():
    def __init__(self, pid, time_to_profile=0, output_filename="") -> None:
        self.pid = pid
        self.time_to_profile = time_to_profile
        self.output_filename = output_filename
            
    def _initialize(self):
        # not backing up the file if the output filename is same as constants.CODE_PROFILER_TRACE_FILENAME
        if path.isfile(constants.CODE_PROFILER_TRACE_NAME) and self.output_filename != constants.CODE_PROFILER_TRACE_FILENAME:
            log_info(f"- Profiler trace {constants.CODE_PROFILER_TRACE_NAME} already exists")
            self._rename_default_trace_file_name()
        log_info("- Ready to profile the application")
        log_info("")
    
    def _rename_default_trace_file_name(self):
        random_name = get_random_string()
        new_filename= f"{constants.CODE_PROFILER_TRACE_NAME}_{random_name}.backup"        
        shutil.move(constants.CODE_PROFILER_TRACE_NAME, new_filename)
        log_info(f"- Successfully renamed the file to {new_filename}")
    
    def _collect_traces(self):        
        viztracer = ViztracerCodeProfiler(self.pid, self.time_to_profile)
        command = viztracer.generate_command()                
        log_info("- Started code profiler")
        if self.time_to_profile == 0:
            log_info("- Press Ctrl-C to stop profiling")
        process = subprocess.run(command)                  
        if process.returncode != 0:
            # The viztracer executable exited. Hence we are exiting the wrapper as well.
            sys.exit()
        log_info("- Stopped code profiler")      
    
    def _get_new_file_name(self):
        now = datetime.now(timezone.utc).strftime("%Y_%m_%d_%H_%M_%S")
        # Considering only first 6 digits of instance id.
        # This helps us to correlate with date in Applens
        instance_id=constants.INSTANCE_ID_TRIMMED
        
        return f"{now}_{instance_id}_{constants.CODE_PROFILER_TRACE_FILENAME}"        
    
    # This test results in false positive result when path to directory is specified (e.g. /tmp )
    def _looks_like_absolute_path(self, filename):
        return filename.startswith("/")
    
    def _get_output_file_path(self):
        output_filepath = self.output_filename
        if self.output_filename == "":
               output_filepath = self._get_new_file_name()
            
        if not self._looks_like_absolute_path(output_filepath):                    
            output_filepath = f"{constants.CODE_PROFILER_LOGS_DIR}/{output_filepath}"

        # returning 
        return output_filepath
    
    def _create_directory_if_not_exists(self, filepath):
        directory_name = path.dirname(filepath) 
        try:
            makedirs(directory_name, exist_ok=True)
        except Exception as e:
            log_info(f"Unable to create directory '{directory_name}' due to {e}")
    
    def save_traces(self):
        with console.status("[bold green] Saving the profiler traces") as status:            
            output_file_path = self._get_output_file_path()            
            self._create_directory_if_not_exists(output_file_path)
                
            log_info(f"- The traces would be saved with the filename - {output_file_path}")
            self._wait_for_viztracer_to_save_traces()
            # renaming the file only if the name is different from constants.CODE_PROFILER_TRACE_FILENAME
            if self.output_filename != constants.CODE_PROFILER_TRACE_FILENAME:
                if path.exists(constants.CODE_PROFILER_TRACE_NAME):
                    # move /home/LogFiles/CodeProfiler/instance_id_profiler_trace.json to /exithome/LogFiles/CodeProfiler/<timestamp>_instanceid_profiler_trace.json
                    shutil.move(constants.CODE_PROFILER_TRACE_NAME , f"{output_file_path}")
                else:
                    log_info(f"- Unable to save the trace by the name {output_file_path}")
            
    def _wait_for_viztracer_to_save_traces(self):
        log_info(f"- Waiting for profiler trace to be saved. This operation will timeout in {WAIT_FOR_VIZTRACER_TO_SAVE_TRACE_TIMEOUT} seconds")
        time_elapsed = 0
        sleep_time_in_seconds = 20
        while not path.exists(constants.CODE_PROFILER_TRACE_NAME):
            sleep(sleep_time_in_seconds)
            time_elapsed += sleep_time_in_seconds
            
            if time_elapsed >= WAIT_FOR_VIZTRACER_TO_SAVE_TRACE_TIMEOUT:
                log_info(f"- Error : Profiler traces could not be generated even after {WAIT_FOR_VIZTRACER_TO_SAVE_TRACE_TIMEOUT} seconds.")
                sys.exit()
            
            log_info(f"- {time_elapsed} seconds passed.")
        log_info("- Successfully saved profiler trace")
        
    # static help message on how to review the trace
    def show_step_to_review_traces(self):
        print()
        log_info("Step 3 : Review the traces", is_header=True)
        url= environ.get( "WAS-DEFAULT-HOSTNAME" , f"https://'<app_name>'.scm.azurewebsites.net")
        print("Please use the following steps to download and review the trace locally:")
        print(f"""1. Ensure Python is installed in you Linux machine / Windows Subsystem for Linux (WSL)
2. Run the following command :
   pip install viztracer
3. Navigate to file manager of Kudu site of the App Service 
   (e.g. {url}/newui/fileManager)
4. Navigate to /home/LogFiles/CodeProfiler/ and download profiler_trace.json
5. In your local machine (Linux / WSL), run the following command
   vizviewer profiler_trace.json
             """)
    
    def profile(self):
        with console.status("[bold green] Initilizing Code Profiler") as status:            
            log_info("Step 1 : Initilizing Code Profiler", is_header=True)
            self._initialize()
        
        with console.status("[bold green] Profiling your application") as status:   
            log_info("Step 2 : Profiling your Application",is_header=True)
            self._collect_traces()        
    
def get_random_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# Rich library spinners are overlapping with logging console handlers.
# Hence printing the statements manually
def log_info(message, is_header=False):
    logger.info(message)
    if is_header:
        show_header(message)
    else:
        print(message)

# Displays the message in a box:
# +-----------------------------+
# |      Message                |
# +-----------------------------+
def show_header(message):
    width = 40
    print('+-' + '-' * width + '-+')
    for line in wrap(message, width):
        print('| {0:^{1}} |'.format(line, width))

    print('+-' + '-'*(width) + '-+')

        