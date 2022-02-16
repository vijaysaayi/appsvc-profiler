import os
import pytest
import signal
from appsvc_profiler.main import is_signal_handlers_initialized_based_on_statusfile_value
from simple_flask_app.app import create_app
from appsvc_profiler.helpers import SignalHelper
from appsvc_profiler.installer import CodeProfilerInstaller
from appsvc_profiler.constants import CodeProfilerConstants as constants

def handler():
    print("This is a test handler")

@pytest.fixture(scope="function")
def add_usr_signals_fixture():
    signal.signal(signal.SIGUSR1, handler)
    signal.signal(signal.SIGUSR1, handler)

@pytest.fixture(scope="function")
def remove_user_signal_handler_fixture():
    signal.signal(signal.SIGUSR1, signal.SIG_DFL)
    signal.signal(signal.SIGUSR2, signal.SIG_DFL)

def test_simple_flask_app():
    flask_app = create_app()
    
    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        assert response.data.decode('utf-8') == 'Testing, Flask!'
        
    signal_helper = SignalHelper()
    assert signal_helper.can_usr_signals_be_used()

def test_simple_flask_app_with_signal_handlers(add_usr_signals_fixture):
    flask_app = create_app()
    
    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        assert response.data.decode('utf-8') == 'Testing, Flask!'
    
    signal_helper = SignalHelper()
    assert signal_helper.can_usr_signals_be_used() == False
    
def test_simple_flask_app(remove_user_signal_handler_fixture):
    flask_app = create_app()
    
    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        assert response.data.decode('utf-8') == 'Testing, Flask!'
        
    signal_helper = SignalHelper()
    assert signal_helper.can_usr_signals_be_used()

def test_simple_flask_app_with_viztracer_handlers(remove_user_signal_handler_fixture):
    flask_app = create_app()
    
    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        assert response.data.decode('utf-8') == 'Testing, Flask!'
        
    signal_helper = SignalHelper()
    assert signal_helper.can_usr_signals_be_used()
    
    os.environ[constants.APP_SETTING_TO_ENABLE_CODE_PROFILER]=str(True)
    
    cpi = CodeProfilerInstaller()
    cpi.install()
    
    assert is_signal_handlers_initialized_based_on_statusfile_value() == True
    
    #clean up
    if constants.APP_SETTING_TO_ENABLE_CODE_PROFILER in os.environ.keys():
        os.environ.pop(constants.APP_SETTING_TO_ENABLE_CODE_PROFILER)