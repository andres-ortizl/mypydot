import time
import pytermgui as ptg
from dataclasses import dataclass
from threading import Thread
from time import sleep
from mypydot.src.view.style import GRADIENT_PURPLE, GRADIENT_GREEN
from pytermgui import Container


@dataclass
class HomeScreen:

    @staticmethod
    def submit(button: ptg.Button) -> None:
        print(button.label)

    def default_cfg_options(self):
        return [ptg.Button('.conf.yml', onclick=self.submit)]

    @staticmethod
    def default_found_cfg_message():
        return [ptg.Label("[bold] Configurations file found[/bold]"),
                ptg.Label("[bold]Select a configuration file to sync  [/bold]")]

    @staticmethod
    def default_not_found_cfg_message():
        return [ptg.Label("[bold] Configuration file not found.[/bold]"),
                ptg.Label("[bold] Creating a new one for you.[/bold]")]

    def render(self, configuration_file_list: list[str]) -> None:
        cfg_options = self.default_cfg_options()
        message = self.default_not_found_cfg_message()
        if configuration_file_list:
            cfg_options = [ptg.Button(cfg_file) for cfg_file in configuration_file_list]
            message = self.default_found_cfg_message()
        with ptg.WindowManager() as manager:
            window = (
                ptg.Window(
                    "",
                    ptg.Label(
                        "[bold] Welcome to mypydot setup! [/bold]",
                    ),
                    "",
                    *message,
                    "",
                    *cfg_options,
                    "",
                    width=60,
                    box="DOUBLE",
                )
                .set_title(f"{GRADIENT_PURPLE}MyPyDot")
                .center()
            )
            manager.add(window)


@dataclass
class PackageSelection:
    package_list: list
    package_to_install = []

    def submit(self, button: ptg.Button) -> None:
        if button.label == "all":
            self.package_to_install = self.package_list
        elif button.label == "install":
            print(self.package_to_install)
        else:
            self.package_to_install.append(button.label)

    def render(self) -> None:
        package_list_buttons = [ptg.Button(label=package, onclick=self.submit) for package in self.package_list]
        # Package selection using a simple checkbox for each of them
        # that are available in the conf.yml file
        with ptg.WindowManager() as manager:
            window = (
                ptg.Window(
                    "",
                    ptg.Label(
                        "[bold] Package installation [/bold]",
                    ),
                    "",
                    *package_list_buttons,
                    "",
                    ptg.Button("all", onclick=self.submit),
                    "",
                    ptg.Button("install", onclick=self.submit),
                    "",
                    width=60,
                    box="DOUBLE",
                )
                .set_title(f"{GRADIENT_PURPLE}MyPyDot")
                .center()
            )
            manager.add(window)


class InstallingLoop(Container):

    def __init__(self, package_list, timeout: float, **attrs) -> None:
        super().__init__(**attrs)
        self.timeout = timeout
        self.package_list = package_list
        Thread(target=self._monitor_loop, daemon=True).start()

    def _monitor_loop(self) -> None:
        self.update_content()
        sleep(self.timeout)

    def update_content(self) -> None:
        for package in self.package_list:
            widget = ptg.Label(f"{GRADIENT_GREEN} [bold] {package} [/bold]")
            self._add_widget(widget)
            time.sleep(self.timeout)


@dataclass
class InstallPackages:
    package_list: list

    # render the installation of packages with an animation using the window manager and the animation class
    def render(self):
        with ptg.WindowManager() as manager:
            window = (
                ptg.Window(
                    "",
                    ptg.Label(
                        "[!gradient(105)] [bold] Installing.. [/bold]",
                    ),
                    "",
                    InstallingLoop(self.package_list, 0.2),
                    "",
                    width=60,
                    box="ROUNDED",
                    height=20,
                    overflow=ptg.Overflow.SCROLL,
                ).set_title(f"{GRADIENT_PURPLE}[ bold] MyPyDot [/bold]")
                .center()
            )
            manager.add(window)


class GoodByeScreen:
    @staticmethod
    def render():
        with ptg.WindowManager() as manager:
            window = (
                ptg.Window(
                    "",
                    ptg.Label(
                        "[bold] Package installed at $HOME/pepo [/bold]",
                    ),
                    "",
                    "",
                    width=60,
                    box="DOUBLE",
                )
                .set_title(f"{GRADIENT_PURPLE}Thank you !")
                .center()
            )
            manager.add(window)
