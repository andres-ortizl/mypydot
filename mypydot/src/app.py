from dataclasses import dataclass
from os.path import exists, join, isdir
from mypydot.src.logging_manager import logging
from mypydot.src.cfg import Cfg
import os
from shutil import copytree
from typing import Union, Callable
import emoji
from enum import Enum


class Opt(str, Enum):
    CREATE = "create"
    SYNC = "sync"


@dataclass
class FileManager:
    @classmethod
    def file_exists(cls, file_route: str) -> bool:
        result = exists(file_route)
        return result

    @classmethod
    def folder_exists(cls, folder_route: str) -> bool:
        return isdir(folder_route)


@dataclass
class SmLink:

    @classmethod
    def create_sym_link(cls, src, dst) -> bool:
        if FileManager.file_exists(dst):
            logging.debug(f'Destination symlink {dst=} file already exists')
            return False
        if not FileManager.file_exists(src):
            logging.debug(f'Source symlink {src=} file does not exists')
            return False
        logging.debug(f'Creating symlink.. {src=}  {dst=} '
                      f'{emoji.emojize(":check_mark_button:")}')
        os.link(src, dst)
        return True


@dataclass
class App:
    _default_dotfiles_dir: str = join(os.getenv('HOME'), '.mypydotfiles')
    _mypydotfiles_env_var_name: str = 'MYPYDOTFILES'
    _dot_files_dir: str = os.getenv(
        _mypydotfiles_env_var_name,
        _default_dotfiles_dir
    )
    _package_directory: str = os.path.dirname(os.path.abspath(__file__))
    _bash_rc_route: str = join(os.getenv('HOME'), '.bashrc')
    _zsh_rc_route: str = join(os.getenv('HOME'), '.zshrc')
    _main_shell_script: str = f'${_mypydotfiles_env_var_name}/shell/main.sh'

    def __post_init__(self):
        self._opt = {
            Opt.CREATE: self.create,
            Opt.SYNC: self.sync,
        }

    def parse_opt(self, opt) -> Union[None, Callable]:
        r = self._opt.get(opt, None)
        if r:
            return r
        opt_list = list(self._opt.keys())
        logging.error(f'{opt=} not recognized, possible {opt_list}')
        exit(1)

    def _copy_template(self):
        logging.info(f'copying template to {self._dot_files_dir} '
                     f'{emoji.emojize(":green_book:")}')
        if FileManager.folder_exists(self._dot_files_dir):
            logging.error(f'Folder {self._dot_files_dir} already exists')
            exit(1)
        copytree(
            join(self._package_directory, '../template'),
            self._dot_files_dir
        )

    @staticmethod
    def _write_to_file(value: str, file_route: str) -> None:
        """
        Add new export env sentence to file
        :param value: Name of the variable
        :param file_route: Route of the file which we want to use to write
        the export sentence
        :return: None
        """
        if not FileManager.file_exists(file_route):
            msg = f'{file_route=} doest not exist, ' \
                  f'cant add new env {emoji.emojize(":green_book:")}'
            logging.warning(msg)
            return
        with open(file_route, 'a') as f:
            msg = f'New {value=} in {file_route}'
            logging.info(msg)
            f.write(f'{value}\n')

    def _set_up_env_vars(self):
        self._write_to_file(
            f'export {self._mypydotfiles_env_var_name}={self._dot_files_dir}',
            file_route=self._bash_rc_route)
        self._write_to_file(
            f'export {self._mypydotfiles_env_var_name}={self._dot_files_dir}',
            file_route=self._zsh_rc_route)

        self._write_to_file(
            f'source {self._main_shell_script}',
            file_route=self._bash_rc_route)
        self._write_to_file(
            f'source {self._main_shell_script}',
            file_route=self._zsh_rc_route)
        os.environ[self._mypydotfiles_env_var_name] = self._dot_files_dir

    def create(self) -> None:
        """
        Initialize a new folder with the template structure. Add new env var
        with the route of the dotfiles folder
        Use case : First time you install the application and want to
        track every dotfile you want in your new
        repository
        :return: None
        """
        self._copy_template()
        self._set_up_env_vars()
        logging.info('Restart your shell to apply the new changes')
        self._sync()

    @staticmethod
    def _sync() -> None:
        """
        Sync files creating a symlink using the conf.yml files.
        :return:
        """
        logging.info('syncing dotfiles from conf.yml')
        cfg: Cfg = Cfg()
        for module, sm_links_dict in cfg.symlinks.items():
            logging.info(f'Creating symlinks for {module=}')
            list(map(
                lambda key: SmLink.create_sym_link(
                    key,
                    sm_links_dict[key]
                ),
                sm_links_dict.keys()
            ))
            logging.info(f'Ready {module=} {emoji.emojize(":thumbs_up:")}')

    def sync(self):
        """
        Try to sync again the files inside the $MYPYDOTFILES
        folder ( if existing )
        :return:
        """
        dotfiles_env = os.getenv(self._mypydotfiles_env_var_name, False)
        logging.info(f'Sync  {dotfiles_env=}')
        if not dotfiles_env:
            self._set_up_env_vars()
        self._sync()
