import os

class CodeProfilerConstants():
    APPSVC_PROFILER_VERSION="1.0.0"
    APP_SETTING_TO_ENABLE_CODE_PROFILER = "APPSETTING_WEBSITE_ENABLE_DEFAULT_CODE_PROFILER" 
    APP_SETTING_TO_SET_SAVE_TRACE_MAX_TIMEOUT = "APPSETTING_WEBSITE_CODE_PROFILER_SAVE_TRACE_TIMEOUT"
    
    @property
    def CODE_PROFILER_LOGS_DIR(self):
        log_dir = "home/LogFiles/CodeProfiler"
        return self._get_directory(log_dir)
    
    @property
    def CODE_PROFILER_LOCKS_DIR(self):
        log_dir = "home/site/CodeProfiler/StatusFiles"
        return self._get_directory(log_dir)
    
    def _check_if_local_development_is_used(self):
        is_local_development_env = os.getenv(self.LOCAL_DEVELOP_ENV_NAME, 'false')
        return (str(is_local_development_env) == "1"
                or str(is_local_development_env).lower() == "true")
    
    def _get_directory(self, logs_directory):
        is_local_development = self._check_if_local_development_is_used()
        local_development_dir = os.getenv(self.LOCAL_DEVELOP_HOME_DIR, '/tmp/kududirs')
        if(is_local_development):
            return f"{local_development_dir}/{logs_directory}"        
        return f"/{logs_directory}"
    
    CODE_PROFILER_TRACE_FILENAME="profiler_trace.json"
    
    @property
    def CODE_PROFILER_TRACE_NAME(self):
        return f"/tmp/{self.INSTANCE_ID_TRIMMED}_{self.CODE_PROFILER_TRACE_FILENAME}"    
    
    GUNICORN_LOGFILE_SIGNAL_HANDLER_INFO = "Worker.handle_usr1 of <gunicorn.workers.sync.SyncWorker object"
    INSTANCE_ID_ENV_NAME = "WEBSITE_INSTANCE_ID"
    
    @property
    def INSTANCE_ID_TRIMMED(self):
        instance_id = os.getenv(self.INSTANCE_ID_ENV_NAME,"default")
        return instance_id[:6]
    
    @property
    def PID_FILE_LOCATION(self):
        return f"{self.CODE_PROFILER_LOGS_DIR}/{self.INSTANCE_ID_TRIMMED}_master_process.pid"
    
    WEBSITE_HOSTNAME_ENV_NAME = "WEBSITE_HOSTNAME"  
    LOCAL_DEVELOP_ENV_NAME = "APPSVC_PROFILER_USE_LOCAL_DEVELOPMENT"
    LOCAL_DEVELOP_HOME_DIR = "APPSVC_PROFILER_LOCAL_DEVELOPMENT_HOME_DIR"

class CodeProfilerExitCodes:
    Success=0    
    Limitation=1
    Disabled=2
    SignalHandlersNotInitialized=3 