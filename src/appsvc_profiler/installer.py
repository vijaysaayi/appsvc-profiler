from pathlib import Path
from .helpers import SignalHelper, is_like_true
from .constants import CodeProfilerConstants
import logging
import os 

constants = CodeProfilerConstants()
LOG_LEVEL = logging.DEBUG
class CodeProfilerInstaller:    
    def __init__(self):
        self.is_profiler_enabled = False
        self._ensure_logs_dir_is_created(constants.CODE_PROFILER_LOGS_DIR)
        # Explicitly setting logger name so that root logger of the application is not modified
        self.logger = logging.getLogger("appsvc_profiler.installer")
        self.logger.setLevel(LOG_LEVEL)
        self.logger.info("Code Profiler Installer is starting up")  
        
        self.signal_helper = SignalHelper(self.logger)
        self._cleanup_signal_handler_initialized_status_file()

    def _ensure_logs_dir_is_created(self,path):
        Path(path).mkdir(parents=True, exist_ok=True)
    
    def _cleanup_signal_handler_initialized_status_file(self):
        self.logger.info("Cleaning up any existing status file which indicated signal handlers initialized status")
        self.instance_id = os.environ.get(constants.INSTANCE_ID_ENV_NAME, "default")
        self._ensure_logs_dir_is_created(constants.CODE_PROFILER_LOCKS_DIR)
        self.status_file_path = f"{constants.CODE_PROFILER_LOCKS_DIR}/{self.instance_id}"
        if os.path.exists(self.status_file_path):
            self.logger.info(f"Attempting to delete the signal_handler status file for instance id {self.instance_id}")
            os.remove(self.status_file_path)
            self.logger.info(f"successfully deleted the status file")
    
    def install(self):
        try:
            should_profiler_be_installed = self._should_profiler_be_enabled()
            can_usr_signals_be_used = self.signal_helper.can_usr_signals_be_used()
            if should_profiler_be_installed and can_usr_signals_be_used:
                from viztracer import VizTracer 
                tracer = VizTracer(output_file= constants.CODE_PROFILER_TRACE_NAME,
                                   ignore_c_function=True, 
                                   plugins=['vizplugins.cpu_usage','vizplugins.memory_usage'], 
                                   max_stack_depth=20)
                self.logger.info("Attempting to install the default code profiler.")
                tracer.install()
                self.logger.info("Successfully installed code profiler.")
                self._set_signal_handler_initialized_status(True)
                self.is_profiler_enabled = True
            else:
                if not should_profiler_be_installed:
                    self.logger.error("Disabling code profiler functionality as it is not enabled")    
                elif not can_usr_signals_be_used:
                    self.logger.error("Disabling code profiler functionality because application is already using signal handlers")    
                self._disable_code_profiler()
                
        except Exception as e:
            self.logger.error("Disabling code profiler due to the following exception")    
            self.logger.exception(e)                        
            self._disable_code_profiler()
            
        finally:
            self.shut_down()
    
    def _should_profiler_be_enabled(self):
        code_profiler_enabled_app_setting_value = os.getenv(constants.APP_SETTING_TO_ENABLE_CODE_PROFILER, None)
        code_profiler_enabled = code_profiler_enabled_app_setting_value is None or is_like_true(code_profiler_enabled_app_setting_value)
        self.logger.debug(f"{constants.APP_SETTING_TO_ENABLE_CODE_PROFILER} : {code_profiler_enabled_app_setting_value}")
                    
        if not code_profiler_enabled:
            self.logger.error(code_profiler_enabled_app_setting_value)        
            self.logger.error(f"Code Profiler is not enabled. {constants.APP_SETTING_TO_ENABLE_CODE_PROFILER} = {code_profiler_enabled_app_setting_value}")        
        
        return code_profiler_enabled
        
    def _set_signal_handler_initialized_status(self,status):
        if status:
            success_message=f"Signal Handlers SIGUSR for needed code-profiler have been initialized for gunicorn process on instance {self.instance_id}"
            with open(self.status_file_path, 'w') as f:
                f.write(success_message)
            self.logger.info(success_message)                   
        else:
            self._cleanup_signal_handler_initialized_status_file()    
    
    def _disable_code_profiler(self):
        self.logger.info("Signal handler status files if set would be deleted")
        self._set_signal_handler_initialized_status(False)        
    
    def shut_down(self):
        self.logger.debug("Code Profiler Installer is exiting as installation is completed")                
    