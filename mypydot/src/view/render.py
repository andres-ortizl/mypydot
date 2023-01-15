from dataclasses import dataclass
from mypydot.src.view.components import (
    HomeScreen,
    PackageSelection,
    InstallPackages,
    GoodByeScreen,
)
from mypydot.src.view.style import Style


@dataclass
class Render:
    @staticmethod
    def __post_init__():
        Style().configure_widgets()

    @staticmethod
    def home_screen(found: bool, configuration_file_list: list[str]) -> str:
        return HomeScreen().render(found, configuration_file_list)

    @staticmethod
    def package_selection(package_list: list) -> list[str]:
        return PackageSelection(package_list).render()

    @staticmethod
    def package_installation(package_list: list) -> None:
        InstallPackages(package_list).render()

    @staticmethod
    def goodbye(installed_dir: str) -> None:
        GoodByeScreen(installed_dir).render()
