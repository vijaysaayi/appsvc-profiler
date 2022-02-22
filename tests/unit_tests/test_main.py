import os
import pytest
from appsvc_profiler import main, is_code_profiler_disabled, is_signal_handlers_initialized_based_on_statusfile_value
from appsvc_profiler.constants import CodeProfilerConstants as constants
from appsvc_profiler.installer import CodeProfilerInstaller
from click.testing import CliRunner

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def test_no_arguments_provided():
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 2
    assert "Usage:" in result.output 
    
def test_attach_argument_provided_profiler_not_enabled():
    runner = CliRunner()
    os.environ[constants.APP_SETTING_TO_ENABLE_CODE_PROFILER]=str(False)
    result = runner.invoke(main,["--attach","10"])
    assert "To enable code profiler, add/update the App Setting " in result.output
    assert result.exit_code == 0
    
    #cleanup
    remove_appsetting(constants.APP_SETTING_TO_ENABLE_CODE_PROFILER)

def remove_appsetting(app_setting_name):
    if app_setting_name in os.environ.keys():
        os.environ.pop(app_setting_name)

@pytest.mark.parametrize(
    "input,expected_result",
    [
        pytest.param(None, True),
        pytest.param(0, False),
        pytest.param(1, True),
        pytest.param("true", True),
        pytest.param("True", True),
        pytest.param("false", False),
        pytest.param("False", False),
        pytest.param("anytext", True),
    ]
    ) 
def test_profiler_enabled(input,expected_result):    
    if input is None:
        remove_appsetting(constants.APP_SETTING_TO_ENABLE_CODE_PROFILER)
    else:
        os.environ[constants.APP_SETTING_TO_ENABLE_CODE_PROFILER]=str(input)
    
    is_profiler_enabled = not is_code_profiler_disabled()
    assert is_profiler_enabled == expected_result
    
    #clean up
    remove_appsetting(constants.APP_SETTING_TO_ENABLE_CODE_PROFILER)

@pytest.mark.parametrize(
    "input,expected_result",
    [
        pytest.param(False, False),
        pytest.param(True, True)
    ]
    ) 
def test_signal_handler_initialized(input,expected_result):    
    cpi = CodeProfilerInstaller()
    cpi._set_signal_handler_initialized_status(input)
    assert is_signal_handlers_initialized_based_on_statusfile_value() == expected_result
    
    #clean up
    cpi._cleanup_signal_handler_initialized_status_file()


