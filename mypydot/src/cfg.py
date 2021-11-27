import yaml
import os
from dataclasses import dataclass


@dataclass
class Cfg:
    def __post_init__(self):
        self._data = self.__load_cfg()
        self.symlinks = self._data['symlinks']

    def __load_cfg(self):
        with open(os.getenv('CONFIG_PATH')) as f:
            data = yaml.full_load(f)
            res = self._parse_env_vars(data)
            return res

    @staticmethod
    def _parse_env_vars(d: dict):
        res = {}

        def parse_env(path):
            if path.startswith('$'):
                return os.getenv(path[1:])
            if path == '~':
                return os.getenv('HOME')
            return path

        for k, v in d.items():
            res[k] = {}
            for s, s_value in d[k].items():
                path_list = list(map(parse_env, s.split('/')))
                s_value_list = list(map(parse_env, s_value.split('/')))
                p = os.path.join(os.sep, *path_list)
                s_v = os.path.join(os.sep, *s_value_list)
                res[k][p] = s_v
        return res
