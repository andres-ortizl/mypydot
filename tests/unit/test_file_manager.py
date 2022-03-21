from mypydot.src.app import FileManager
from os import getcwd
from os.path import join, dirname, abspath
import uuid


class TestFileManager:
    def test_file_exists(self):
        test_file = join(getcwd(), 'exists.txt')
        rand_id = str(uuid.uuid4())
        with open(test_file, 'w') as f:
            f.write(rand_id)
        assert FileManager.file_exists(test_file) is True

    def test_dir_exists(self):
        assert FileManager.folder_exists(dirname(abspath(__file__))) is True
