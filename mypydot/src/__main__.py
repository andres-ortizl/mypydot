from app import App
from logging_manager import LoggingConf

if __name__ == '__main__':
    LoggingConf()
    app = App(None)
    f = app.parse_opt('init')
    f()
