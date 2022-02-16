
from .constants import CodeProfilerConstants as constants
import signal
import logging

def is_like_true(value):
    return (str(value) == "1"
            or str(value).lower() == "true")

def is_like_false(value):
    return (str(value) == "0"
            or str(value).lower() == "false")
class SignalHelper():
    def __init__(self,logger=None):
        if logger is None:
           logger = logging.getLogger()
        self.logger = logger
        
    def can_usr_signals_be_used(self):
        is_sigusr1_available = self._is_signal_usr_signal_handlers_used(signal.SIGUSR1)
        is_sigusr2_available = self._is_signal_usr_signal_handlers_used(signal.SIGUSR2)
        
        return is_sigusr1_available and is_sigusr2_available

    def _is_signal_usr_signal_handlers_used(self, signal_to_test):
        signal_handler = signal.getsignal(signal_to_test)
        is_signal_handlers_used = (signal_handler is None
                                    or self._is_default_signal_handler(signal_handler)
                                    or self._is_ignore_signal_handler(signal_handler)
                                    or self._is_gunicorn_logfile_signal_handler(signal_handler) )
                                    # Gunicorn is configured to emit logs to std. Hence
                                    # we can safely override SIGUSR1 handler
        if not is_signal_handlers_used:
            self.logger.error(f"{signal_to_test.name} is not available as it is used by {signal_handler}")
        
        return is_signal_handlers_used

    def _is_default_signal_handler(self, signal_handler):
        return (signal_handler is not None
                and hasattr(signal_handler , "name")
                and signal_handler.name == signal.SIG_DFL.name)

    def _is_ignore_signal_handler(self, signal_handler):
        return (signal_handler is not None
                and hasattr(signal_handler , "name")
                and signal_handler.name == signal.SIG_IGN.name)

    def _is_gunicorn_logfile_signal_handler(self, signal_handler):
        return (signal_handler is not None
                and constants.GUNICORN_LOGFILE_SIGNAL_HANDLER_INFO in str(signal_handler))
