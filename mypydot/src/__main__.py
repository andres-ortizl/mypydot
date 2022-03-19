from app import App
from logging_manager import LoggingConf
import click
from cfg import Cfg


@click.command()
@click.argument('option')
def main(option: str):
    """Options can be :


        - Create : It's going to initialize a new dotfiles folder and sync
        the available symlinks

        - Resync : Will try to sync new dotfiles

        - Install : It's going to install an existing dotfiles folder

        """
    LoggingConf()
    app = App()
    f = app.parse_opt(option)
    f()


if __name__ == '__main__':
    main()

