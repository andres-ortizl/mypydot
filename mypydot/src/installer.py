from dataclasses import dataclass
import subprocess
import logging
from app import FileManager


@dataclass
class OSInstaller:

    @classmethod
    def install_homebrew_packages(cls, brew_file_route: str) -> bool:
        if not FileManager.file_exists(brew_file_route):
            logging.error(f'file {brew_file_route} does not exist')
            exit(1)
        cmd = f'brew bundle --file {brew_file_route}'
        proc = subprocess.Popen(cmd, shell=True, stdout=True)
        proc.communicate()
        return_code_brew = proc.wait()
        logging.info(f"return code brew : {return_code_brew}")

        if return_code_brew == 0:
            logging.info("Homebrew installation was fine")
            logging.info(f"Here is the successful command: {cmd}")
            return True

        logging.info("Homebrew installation was not fine!")
        return False

    def dump_brew_file(self):
        """TBD implement dump of the brew file
        containing all the SO packages"""
        pass


@dataclass
class LinuxInstaller:
    pass
