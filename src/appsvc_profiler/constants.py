import os
class CodeProfilerConstants():
    APPSVC_PROFILER_VERSION="1.0.0"
    APP_SETTING_TO_ENABLE_CODE_PROFILER = "APPSETTING_WEBSITE_ENABLE_DEFAULT_CODE_PROFILER" 
    APP_SETTING_TO_SET_SAVE_TRACE_MAX_TIMEOUT = "APPSETTING_WEBSITE_CODE_PROFILER_SAVE_TRACE_TIMEOUT"
    
    CODE_PROFILER_LOGS_DIR = "/home/LogFiles/CodeProfiler"
    CODE_PROFILER_LOCKS_DIR = "/home/site/CodeProfiler/StatusFiles"
    CODE_PROFILER_TRACE_FILENAME="profiler_trace.json"
    CODE_PROFILER_TRACE_NAME = f"{CODE_PROFILER_LOGS_DIR}/{CODE_PROFILER_TRACE_FILENAME}"    
    
    GUNICORN_LOGFILE_SIGNAL_HANDLER_INFO = "Worker.handle_usr1 of <gunicorn.workers.sync.SyncWorker object"
    INSTANCE_ID_ENV_NAME = "WEBSITE_INSTANCE_ID"
    
    PID_FILE_LOCATION = f"{CODE_PROFILER_LOGS_DIR}/master_process.pid"
    WEBSITE_HOSTNAME_ENV_NAME = "WEBSITE_INSTANCE_ID"  

class CodeProfilerExitCodes:
    Success=0    
    Limitation=1
    Disabled=2
    SignalHandlersNotInitialized=3 