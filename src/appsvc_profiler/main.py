import string
import click
import logging
import os

from .constants import CodeProfilerConstants , CodeProfilerExitCodes
from .helpers import is_like_false, check_if_process_is_running
from pathlib import Path
from .profiler import CodeProfiler

constants = CodeProfilerConstants()
def ensure_logs_dir_is_created():
    try:
        Path(constants.CODE_PROFILER_LOGS_DIR).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(e)

def initialize_logger():
    instance_id = constants.INSTANCE_ID_TRIMMED
    # Explicitly setting logger name so that root logger of the application is not modified
    logger = logging.getLogger("appsvc_profiler")
    logger.setLevel(logging.DEBUG)
    
    fh = logging.FileHandler(f"{constants.CODE_PROFILER_LOGS_DIR}/{instance_id}_debug.log")
    fh.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',datefmt="%Y_%m_%d_%H_%M_%S")
    fh.setFormatter(formatter)
    
    logger.addHandler(fh)
    return logger

ensure_logs_dir_is_created()
logger = initialize_logger()
logger.setLevel= logging.DEBUG

def is_code_profiler_disabled():
    code_profiler_enabled_app_setting_value = os.getenv(constants.APP_SETTING_TO_ENABLE_CODE_PROFILER, None)
    code_profiler_enabled = code_profiler_enabled_app_setting_value is not None and  is_like_false(code_profiler_enabled_app_setting_value)
    logger.debug(f"{constants.APP_SETTING_TO_ENABLE_CODE_PROFILER} : {code_profiler_enabled_app_setting_value}")
    logger.debug(f"Is Code Profiled Disabled : {code_profiler_enabled}")
    
    return code_profiler_enabled

def is_signal_handlers_initialized_based_on_statusfile_value():
    instance_id = os.environ.get(constants.INSTANCE_ID_ENV_NAME, "default")
    status_file_path = f"{constants.CODE_PROFILER_LOCKS_DIR}/{instance_id}"
    status =  os.path.exists(status_file_path)
    logger.debug(f"Are signal handlers initialized : {status}")
    return status

@click.command()
@click.option("--attach", "-a", help="PID of the gunicorn worker process to profile", required=True,type=int)
@click.option("--time-to-profile", "-t", help="Number of seconds to profiler", type=int, default=0)
@click.option("--output-filename", "-o", help="Output Filename", type=str,default="")
def main(attach, time_to_profile, output_filename):
    if not check_if_process_is_running("gunicorn"):
        display("[Limitation] Code profiler is disabled when custom startup scripts are used in App Service.")
        exit(CodeProfilerExitCodes.Limitation)
    if is_code_profiler_disabled():
        display("To enable code profiler, add/update the App Setting WEBSITE_ENABLE_DEFAULT_CODE_PROFILER=true")
        display("NOTE : Updating this App Setting will restart your App Service !!")
        display("")
        exit(CodeProfilerExitCodes.Disabled)
    
    if not is_signal_handlers_initialized_based_on_statusfile_value():
        display("There was an issue while installing code profiler.")
        display(f"Please review debug log in {constants.CODE_PROFILER_LOGS_DIR}")
        exit(CodeProfilerExitCodes.SignalHandlersNotInitialized)
    else:
        logger.info("Code Profiler is enabled and signal handlers are initialized")
        code_profiler = CodeProfiler(attach, time_to_profile, output_filename)        
        try:
            code_profiler.profile()
        except KeyboardInterrupt :
            pass
            
        code_profiler.save_traces()
        code_profiler.show_step_to_review_traces()
        exit(CodeProfilerExitCodes.Success)

# Rich library spinners are overlapping with logging console handlers.
# Hence using logger seperately and printing the statements manually
def display(message):
    print(message)    
    logger.info(message)
        
