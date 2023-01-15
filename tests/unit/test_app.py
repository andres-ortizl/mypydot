from mypydot.src.app import App
import pytest
import uuid
from os import getcwd
from os.path import join
import shutil
import os
from mypydot.src.cfg import Cfg


class TestApp:
    def test_init(self):
        app = App()
        assert isinstance(app, App)

    def test_copy_template(self):
        app = App()
        app._dot_files_dir = join(getcwd(), str(uuid.uuid4()))
        app._copy_template()
        shutil.rmtree(app._dot_files_dir)

    def test_copy_template_existing_folder(self):
        path = join(getcwd(), str(uuid.uuid4()))
        os.mkdir(path)
        app = App()
        app._dot_files_dir = path
        with pytest.raises(SystemExit):
            app._copy_template()
        shutil.rmtree(app._dot_files_dir)

    def test_write_to_file(self):
        f_name = "test_write_to_file.txt"
        with open(f_name, "w") as f:
            f.write("test")
        app = App()
        id_txt = str(uuid.uuid4())
        app._write_to_file(id_txt, f_name)
        data = open(f_name, "r").read()
        os.remove(f_name)
        assert data == "test" + id_txt + "\n"

    def test_look_for_config_files(self):
        os.environ["MYPYDOTFILES"] = "tests/unit/assets"
        app = App()
        found, r = app._look_for_existing_config()
        assert found is True
        assert r == ["empty_mock_conf.yml", "mock_conf.yml"]

    def test_create_symlinks(self):
        app = App()
        dotfiles_dir = join("/tmp/", str(uuid.uuid4()))
        app._dot_files_dir = dotfiles_dir
        app._copy_template()
        os.environ["MYPYDOTFILES"] = dotfiles_dir
        cfg = Cfg("./tests/unit/assets/empty_mock_conf.yml")
        app._sync(cfg, ["fake"])
        shutil.rmtree(app._dot_files_dir)
