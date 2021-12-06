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

        sm_link_file_route = path.join(os.getcwd(), 'test_create_smlink.txt')
        res = SmLink.create_sym_link(input_file_route, sm_link_file_route)
        with open(sm_link_file_route, 'r') as f:
            file_content = f.read()

        remove(input_file_route)
        remove(sm_link_file_route)
        assert file_content == rand_id
        assert res is True

    def test_create_smlink_wrong(self):
        res = SmLink.create_sym_link(str(uuid.uuid1()), str(uuid.uuid1()))
        assert res is False

    def test_create_smlink_exists(self):
        output_file_route = path.join(os.getcwd(), 'exists.txt')
        rand_id = str(uuid.uuid4())
        with open(output_file_route, 'w') as f:
            f.write(rand_id)
        res = SmLink.create_sym_link(str(uuid.uuid1()), output_file_route)
        remove(output_file_route)
        assert res is False
