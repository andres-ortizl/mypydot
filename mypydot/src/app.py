from dataclasses import dataclass
from os.path import exists, join, isdir
from mypydot.src.logging_manager import logging
from mypydot.src.cfg import Cfg
import os
from shutil import copytree
import emoji
from enum import Enum
from mypydot.src.view.render import Render


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
            logging.debug(f"Destination symlink {dst=} file already exists")
            return False
        if not FileManager.file_exists(src):
            logging.debug(f"Source symlink {src=} file does not exists")
            return False
        logging.debug(
            f"Creating symlink.. {src=}  {dst=} "
            f'{emoji.emojize(":check_mark_button:")}'
        )
        os.link(src, dst)
        return True


@dataclass
class App:
    _default_dotfiles_dir: str = join(os.getenv("HOME"), ".mypydotfiles")
    _mypydotfiles_env_var_name: str = "MYPYDOTFILES"
    _dot_files_dir: str = os.getenv(_mypydotfiles_env_var_name, _default_dotfiles_dir)
    _package_directory: str = os.path.dirname(os.path.abspath(__file__))
    _bash_rc_route: str = join(os.getenv("HOME"), ".bashrc")
    _zsh_rc_route: str = join(os.getenv("HOME"), ".zshrc")
    _main_shell_script: str = f"${_mypydotfiles_env_var_name}/shell/main.sh"
    render = Render()

    def _look_for_existing_config(self) -> tuple[bool, list | str]:
        """
        Look for existing config file in the $MYPYDOTFILES folder
        :return:
        """
        dotfiles_env = os.getenv(self._mypydotfiles_env_var_name, False)
        if not dotfiles_env:
            logging.info(f"No existing config found in {self._dot_files_dir}")
            return False, [".conf.yml"]
        logging.info(f"Found existing config {dotfiles_env=}")
        # return list of files with pattern .conf.yml
        return True, [f for f in os.listdir(dotfiles_env) if f.endswith("conf.yml")]

    def _copy_template(self):
        logging.info(
            f"copying template to {self._dot_files_dir} "
            f'{emoji.emojize(":green_book:")}'
        )
        if FileManager.folder_exists(self._dot_files_dir):
            logging.error(f"Folder {self._dot_files_dir} already exists")
            exit(1)
        copytree(join(self._package_directory, "../template"), self._dot_files_dir)

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
            msg = (
                f"{file_route=} doest not exist, "
                f'cant add new env {emoji.emojize(":green_book:")}'
            )
            logging.warning(msg)
            return
        with open(file_route, "a") as f:
            msg = f"New {value=} in {file_route}"
            logging.info(msg)
            f.write(f"{value}\n")

    def _set_up_env_vars(self):
        self._write_to_file(
            f"export {self._mypydotfiles_env_var_name}={self._dot_files_dir}",
            file_route=self._bash_rc_route,
        )
        self._write_to_file(
            f"export {self._mypydotfiles_env_var_name}={self._dot_files_dir}",
            file_route=self._zsh_rc_route,
        )

        self._write_to_file(
            f"source {self._main_shell_script}", file_route=self._bash_rc_route
        )
        self._write_to_file(
            f"source {self._main_shell_script}", file_route=self._zsh_rc_route
        )
        os.environ[self._mypydotfiles_env_var_name] = self._dot_files_dir

    @staticmethod
    def _sync(cfg, package_list: list) -> None:
        """
        Sync files creating a symlink using the conf.yml files.
        :return:
        """
        logging.info("syncing dotfiles from conf.yml")
        # filter package_list in cfg.data

        for module, sm_links_dict in cfg.data.items():
            if module not in package_list:
                continue
            logging.info(f"Creating symlinks for {module=}")
            list(
                map(
                    lambda key: SmLink.create_sym_link(key, sm_links_dict[key]),
                    sm_links_dict.keys(),
                )
            )
            logging.info(f'Ready {module=} {emoji.emojize(":thumbs_up:")}')

    def run(self):
        found, r = self._look_for_existing_config()
        if not found:
            self._copy_template()
            self._set_up_env_vars()
        cfg_file = self.render.home_screen(found, r)
        cfg: Cfg = Cfg(join(self._dot_files_dir, cfg_file))
        package_list = self.render.package_selection(list(cfg.data.keys()))
        self.render.package_installation(package_list)
        self._sync(cfg, package_list)
        self.render.goodbye(self._dot_files_dir)
