import os.path
from app import SmLink
import uuid
from os import path, remove


class TestSmLink:

    def test_create_smlink(self):
        input_file_route = path.join(os.getcwd(), 'input_file.txt')
        rand_id = str(uuid.uuid4())
        with open(input_file_route, 'w') as f:
            f.write(rand_id)

        sm_link_file_route = '/tmp/test_create_smlink.txt'
        SmLink.create_sym_link(input_file_route, sm_link_file_route)
        with open(sm_link_file_route, 'r') as f:
            file_content = f.read()

        remove(input_file_route)
        remove(sm_link_file_route)
        assert file_content == rand_id
