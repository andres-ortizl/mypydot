from mypydot.src.app import App
import pytest
import uuid
from os import getcwd
from os.path import join
import shutil
import os
from mypydot.src.main import main


class TestApp:
    def test_init(self):
        app = App()
        assert isinstance(app, App)

    def test_parse_opt_fake(self):
        with pytest.raises(SystemExit):
            app = App()
            app.parse_opt('not_exists')

    def test_parse_opt(self):
        app = App()
        res = app.parse_opt('create')
        assert res is not None

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

    def test_create(self):
        f = main('create')
        f()

    def test_sync(self):
        f = main('sync')
        f()
