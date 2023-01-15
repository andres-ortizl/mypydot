from mypydot.src.logging_manager import LoggingConf
from mypydot.src.app import App


def main():
    LoggingConf()
    App().run()


def entry_point():
    main()


if __name__ == "__main__":
    main()
