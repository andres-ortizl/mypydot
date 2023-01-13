from dataclasses import dataclass
from mypydot.src.view.components import HomeScreen, PackageSelection, InstallPackages, GoodByeScreen
from mypydot.src.view.style import Style


@dataclass
class Render:
    configuration_file_list = []

    def __post_init__(self):
        Style().configure_widgets()

    def home_screen(self):
        HomeScreen().render(self.configuration_file_list)

    def package_selection(self):
        PackageSelection(["vim", "zsh", "nano"]).render()

    def package_installation(self):
        InstallPackages(["vim", "zsh", "nanaso", "nonable"]).render()

    def goodbye(self):
        GoodByeScreen().render()
