from mypydot.src.view.render import Render
import os
import pyte
import select
import pytest
from typing import Callable


class TestRender:
    @staticmethod
    @pytest.mark.parametrize(
        "render, assertion, kwargs",
        [
            (
                Render.home_screen,
                "Welcome to mypydot setup!",
                {"configuration_file_list": [], "found": False},
            ),
            (Render.package_selection, "Package installation", {"package_list": []}),
            (Render.package_installation, "Installing..", {"package_list": []}),
            (Render.goodbye, "Thank you", {"installed_dir": "/home/"}),
        ],
    )
    def test_render_tui(render: Callable, assertion: str, kwargs):
        pid, fd = os.forkpty()
        if pid == 0:
            render(**kwargs)
        else:
            # parent process sets up virtual screen of
            # identical size
            screen = pyte.Screen(150, 30)
            stream = pyte.ByteStream(screen)
            # scrape pseudo-terminal's screen
            while True:
                try:
                    [fd], _, _ = select.select([fd], [], [], 1)
                except (KeyboardInterrupt, ValueError):
                    # either test was interrupted or the
                    # file descriptor of the child process
                    # provides nothing to be read
                    break
                else:
                    try:
                        # scrape screen of child process
                        data = os.read(fd, 1024)
                        stream.feed(data)
                    except OSError:
                        # reading empty
                        break
            r = ""
            for line in screen.display:
                r += line
            assert assertion in r.strip()
        # exit test properly

    def test_dummy(self):
        assert 1 == 1
