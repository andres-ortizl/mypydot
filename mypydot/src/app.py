from dataclasses import dataclass
from os.path import exists, join, isdir
import logging
import os
from cfg import Cfg
from shutil import copytree
from typing import Union, Callable
import emoji


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
        logging.debug(f'Creating symlink.. {src=}  {dst=} {emoji.emojize(":check_mark_button:")}')
        os.symlink(src, dst)
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

    def __post_init__(self):
        self._opt = {
            'create': self.create,
            'install': self.install,
            'resync': self.resync,
        }

    def parse_opt(self, opt) -> Union[None, Callable]:
        r = self._opt.get(opt, None)
        if r:
            return r
        opt_list = list(self._opt.keys())
        logging.error(f'{opt=} not recognized, possible {opt_list}')

    def _copy_template(self):
        logging.info(f'copying template to {self._dot_files_dir} {emoji.emojize(":green_book:")}')
        if FileManager.folder_exists(self._dot_files_dir):
            logging.error(f'Folder {self._dot_files_dir} already exists')
            exit(1)
        copytree(
            join(self._package_directory, '../template'),
            self._dot_files_dir
        )

    @staticmethod
    def _add_env_var(var_name: str, var_value: str, file_route: str) -> None:
        """
        Add new export env sentence to file
        :param var_name: Name of the variable
        :param var_value: Value of the variable
        :param file_route: Route of the file which we want to use to write
        the export sentence
        :return: None
        """
        if not FileManager.file_exists(file_route):
            msg = f'{file_route=} doest not exist, cant add new env {emoji.emojize(":green_book:")}'
            logging.error(msg)
            exit(0)
        with open(file_route, 'w') as f:
            msg = f'New env var to {file_route=}, {var_name=}, {var_value}'
            logging.info(msg)
            f.write(f'export {var_name}={var_value}')
            os.environ[var_name] = var_value

    def create(self) -> None:
        """
        Initialize a new folder with the template structure.
        Add new env var with the route of the dotfiles folder
        :return: None
        """
        self._copy_template()
        self._add_env_var(
            var_name=self._mypydotfiles_env_var_name,
            var_value=self._dot_files_dir,
            file_route=join(os.getenv('HOME'), '.bashrc'))
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

    def install(self, dotfiles_route: str):
        """
        Given an existing dotfiles, sync the information
        :return:
        """
        print('install')

    def resync(self):
        pass
