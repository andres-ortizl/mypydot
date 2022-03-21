from mypydot.src.logging_manager import LoggingConf
import logging


class TestLogging:
    def test_init_logging(self):
        assert isinstance(LoggingConf(), LoggingConf)
        root = logging.getLogger()
        assert root.level == logging.DEBUG
        assert root.hasHandlers() is True
