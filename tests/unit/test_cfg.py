import pytest
from mypydot.src.cfg import Cfg
from os import getenv, environ
from os.path import join


class TestCfg:
    def test_load_cfg(self):
        environ["MYPYDOTFILES"] = "./tests/unit/assets"
        cfg = Cfg("./tests/unit/assets/mock_conf.yml")
        home = getenv("HOME")

        assert "git" in cfg.data
        assert "zsh" in cfg.data

        config_path = "/./tests/unit/assets/git/.gitconfig"
        gitconfig_key = cfg.data["git"][str(join(home, ".gitconfig"))]
        assert gitconfig_key == config_path

    def test_not_found_cfg(self):
        with pytest.raises(SystemExit):
            environ["MYPYDOTFILES"] = "./tests/unit/assets"
            Cfg("mock_fake_cfg.yml")
