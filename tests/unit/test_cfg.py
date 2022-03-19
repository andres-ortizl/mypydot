from cfg import Cfg
from os import getenv, environ
from os.path import join


class TestCfg:
    def test_load_cfg(self):
        environ['MYPYDOTFILES'] = './tests/unit/assets'
        cfg = Cfg(_default_conf_name='mock_cfg.yml')
        home = getenv('HOME')

        assert 'git' in cfg._data
        assert 'zsh' in cfg._data

        config_path = '/./tests/unit/assets/git/.gitconfig'
        gitconfig_key = cfg._data['git'][str(join(home, '.gitconfig'))]
        assert gitconfig_key == config_path
