from asyncio import constants
import pytest
import os
from appsvc_profiler.constants import CodeProfilerConstants

constants = CodeProfilerConstants()

def setup_local_dev_settings(local_dev_directory = None):
    os.environ[constants.LOCAL_DEVELOP_ENV_NAME]=str(True) 
        
    if local_dev_directory is not None:
        os.environ[constants.LOCAL_DEVELOP_HOME_DIR] = local_dev_directory
    else:
        remove_appsetting(constants.LOCAL_DEVELOP_HOME_DIR)
        
def remove_appsetting(app_setting_name):
    if app_setting_name in os.environ.keys():
        os.environ.pop(app_setting_name)      

@pytest.mark.parametrize(
    "is_local_development, local_dev_directory, expected_result",
    [
        pytest.param(False, None, "/home/LogFiles/CodeProfiler"),
        pytest.param(True,None, "/tmp/kududirs/home/LogFiles/CodeProfiler"),
        pytest.param(True, "/tmp/kududev", "/tmp/kududev/home/LogFiles/CodeProfiler")
    ]
    ) 
def test_CODE_PROFILER_LOGS_DIR(is_local_development,local_dev_directory,expected_result):
    if is_local_development:
        setup_local_dev_settings(local_dev_directory)
    else:
        remove_appsetting(constants.LOCAL_DEVELOP_ENV_NAME)
        
    assert constants.CODE_PROFILER_LOGS_DIR == expected_result
        
    #cleanup
    remove_appsetting(constants.LOCAL_DEVELOP_ENV_NAME)
    remove_appsetting(constants.LOCAL_DEVELOP_HOME_DIR)

@pytest.mark.parametrize(
    "is_local_development, local_dev_directory, expected_result",
    [
        pytest.param(False, None, "/home/site/CodeProfiler/StatusFiles"),
        pytest.param(True,None, "/tmp/kududirs/home/site/CodeProfiler/StatusFiles"),
        pytest.param(True, "/tmp/kududev", "/tmp/kududev/home/site/CodeProfiler/StatusFiles")
    ]
    ) 
def test_CODE_PROFILER_LOCKS_DIR(is_local_development,local_dev_directory,expected_result):
    if is_local_development:
        setup_local_dev_settings(local_dev_directory)
    else:
        remove_appsetting(constants.LOCAL_DEVELOP_ENV_NAME)
        
    assert constants.CODE_PROFILER_LOCKS_DIR == expected_result
        
    #cleanup
    remove_appsetting(constants.LOCAL_DEVELOP_ENV_NAME)
    remove_appsetting(constants.LOCAL_DEVELOP_HOME_DIR)

@pytest.mark.parametrize(
    "instance_id, expected_result",
    [
        pytest.param(None, "defaul"),
        pytest.param("test12345", "test12")
    ]
    ) 
def test_INSTANCE_ID_TRIMMED(instance_id,expected_result):
    
    if instance_id is None:
        remove_appsetting(constants.INSTANCE_ID_ENV_NAME)
    else:
        os.environ[constants.INSTANCE_ID_ENV_NAME]=instance_id
        
    assert constants.INSTANCE_ID_TRIMMED == expected_result
        
    #cleanup
    remove_appsetting(constants.INSTANCE_ID_ENV_NAME)

@pytest.mark.parametrize(
    "is_local_development, local_dev_directory, instance_id, expected_result",
    [
        pytest.param(False, None,None, "/home/LogFiles/CodeProfiler/defaul_master_process.pid"),
        pytest.param(True, None,"test12345", "/tmp/kududirs/home/LogFiles/CodeProfiler/test12_master_process.pid"),
        pytest.param(True, "/tmp/kududev" ,"test12345", "/tmp/kududev/home/LogFiles/CodeProfiler/test12_master_process.pid")
    ]
    ) 
def test_PID_FILE_LOCATION(is_local_development, local_dev_directory, instance_id,expected_result):
    if is_local_development:
        setup_local_dev_settings(local_dev_directory)
    else:
        remove_appsetting(constants.LOCAL_DEVELOP_ENV_NAME)
    
    if instance_id is None:
        remove_appsetting(constants.INSTANCE_ID_ENV_NAME)
    else:
        os.environ[constants.INSTANCE_ID_ENV_NAME]=instance_id
        
    assert constants.PID_FILE_LOCATION == expected_result
        
    #cleanup
    remove_appsetting(constants.INSTANCE_ID_ENV_NAME)