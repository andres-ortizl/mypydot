import time
import pytermgui as ptg
from dataclasses import dataclass
from threading import Thread
from time import sleep
from mypydot.src.view.style import GRADIENT_PURPLE, SUCCESS_LABEL
from pytermgui import Container


@dataclass
class HomeScreen:
    OUTPUT = ""
    manager: ptg.WindowManager = None

    def _submit(self, button: ptg.Button):
        self.OUTPUT = button.label
        self.manager.stop()

    @staticmethod
    def default_found_cfg_message():
        return [
            ptg.Label("[bold] Configurations file found[/bold]"),
            ptg.Label("[bold]Select a configuration file to sync  [/bold]"),
        ]

    @staticmethod
    def default_not_found_cfg_message():
        return [
            ptg.Label("[bold] Configuration file not found.[/bold]"),
            ptg.Label("[bold] Creating a new one for you.[/bold]"),
        ]

    def render(self, found: bool, configuration_file_list: list[str]) -> str:
        message = self.default_not_found_cfg_message()
        if found:
            message = self.default_found_cfg_message()

        with ptg.WindowManager() as manager:
            self.manager = manager
            window = (
                ptg.Window(
                    "",
                    ptg.Label(
                        "[bold] Welcome to mypydot setup! [/bold]",
                    ),
                    "",
                    *message,
                    "",
                    *[
                        ptg.Button(cfg_file, onclick=self._submit)
                        for cfg_file in configuration_file_list
                    ],
                    "",
                    width=60,
                    box="DOUBLE",
                )
                .set_title(f"{GRADIENT_PURPLE}MyPyDot")
                .center()
            )
            manager.add(window)
        return self.OUTPUT


@dataclass
class PackageSelection:
    package_list: list
    package_to_install = []
    manager: ptg.WindowManager = None

    def submit(self, button: ptg.Button) -> None:
        if button.label == "install all":
            self.package_to_install = self.package_list
        elif button.label == "install selected":
            if not self.package_to_install:
                self.manager.toast("No package selected")
            else:
                self.manager.stop()
        else:
            button.styles._current = SUCCESS_LABEL
            self.package_to_install.append(button.label)

    def render(self) -> list:
        with ptg.WindowManager() as manager:
            self.manager = manager
            install_selected = ptg.Button("install selected", onclick=self.submit)
            install_all = ptg.Button("install all", onclick=self.submit)
            window = (
                ptg.Window(
                    "",
                    ptg.Label(
                        "[bold] Package installation [/bold]",
                    ),
                    "",
                    *[
                        ptg.Button(package, onclick=self.submit)
                        for package in self.package_list
                    ],
                    "",
                    install_selected,
                    install_all,
                    "",
                    width=60,
                    box="DOUBLE",
                )
                .set_title(f"{GRADIENT_PURPLE}MyPyDot")
                .center()
            )
            manager.add(window)
        return list(set(self.package_to_install))


class InstallingLoop(Container):
    def __init__(self, package_list, timeout: float, **attrs) -> None:
        super().__init__(**attrs)
        self.timeout = timeout
        self.package_list = package_list
        self.thread = Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()

    def _monitor_loop(self) -> None:
        self.update_content()

    def update_content(self) -> None:
        for package in self.package_list:
            widget = ptg.Label(f"[bold] {package} [/bold]")
            self._add_widget(widget)
            time.sleep(self.timeout)


@dataclass
class InstallPackages:
    package_list: list
    """
    Render the installation of packages with
    an animation using the window manager and the animation class
    """
    manager = None

    def finish(self, button: ptg.Button):
        self.manager.toast("[bold] Installation completed [/bold]")
        sleep(2)
        self.manager.stop()

    def render(self):
        with ptg.WindowManager() as manager:
            self.manager = manager
            window = (
                ptg.Window(
                    "",
                    ptg.Label(
                        "[bold] Installing.. [/bold]",
                    ),
                    "",
                    InstallingLoop(self.package_list, 0.5),
                    "",
                    ptg.Button("Finish", onclick=self.finish),
                    width=60,
                    box="ROUNDED",
                    height=20,
                    overflow=ptg.Overflow.SCROLL,
                )
                .set_title(f"{GRADIENT_PURPLE}[ bold] MyPyDot [/bold]")
                .center()
            )
            manager.add(window)


@dataclass
class GoodByeScreen:
    installed_dir: str

    def render(self):
        with ptg.WindowManager() as manager:
            window = (
                ptg.Window(
                    "",
                    ptg.Label(
                        f"[bold] Package installed at {self.installed_dir} [/bold]",
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
