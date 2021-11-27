from dataclasses import dataclass, field
from os.path import exists
import logging
import os
from cfg import Cfg
from shutil import copytree
from typing import Union, Callable


@dataclass
class FileManager:
    @classmethod
    def file_exists(cls, file_route: str) -> bool:
        result = exists(file_route)
        return result


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
        logging.debug(f'Creating symlink ..{src=}  {dst=}')
        os.symlink(src, dst)
        return True


@dataclass
class App:
    _opt: field(default_factory=dict)
    _dot_files_dir: str = os.getenv('MYPYDOTFILES')

    def __post_init__(self):
        self._opt = {
            'init': self.init,
            'install': self.install,
            'doctor': self.doctor,
            'sync': self.sync,
            'restore': self.restore
        }

    def parse_opt(self, opt) -> Union[None, Callable]:
        r = self._opt.get(opt, None)
        if r:
            return r
        opt_list = list(self._opt.keys())
        logging.error(f'{opt=} not recognized, possible {opt_list}')

    def init(self) -> None:
        """
        Initialize a new folder with the template structure.
        :return: None
        """
        logging.info(f'copying template to {self._dot_files_dir}')
        # TODO: Use relative path to library
        copytree('/Users/andrew/Code/mypydot/template', self._dot_files_dir)

    def sync(self) -> None:
        """
        Sync files creating a symlink using the conf.yml files.
        :return:
        """
        logging.info('syncing dotfiles from conf.yml')
        cfg: Cfg = Cfg()
        # TODO: Review
        list(map(
            lambda key: SmLink.create_sym_link(
                key,
                cfg.symlinks[key]
            ),
            cfg.symlinks.keys()
        ))

    def install(self):
        """
        Given an existing dotfiles, restore the information.
        :return:
        """
        print('install')

    def doctor(self):
        print('doctor')

    def restore(self):
        print('restore')
