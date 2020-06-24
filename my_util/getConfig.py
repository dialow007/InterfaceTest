import os
import yaml
import getWorkDir

path = getWorkDir.get_base_dir()
conf_file = os.path.join(path, 'config.yaml')


def get_conf(key):
    """
    @param key:
    @return:
    """
    data = read_yaml()
    return data[key]


def read_yaml():
    with open(conf_file, 'r',encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data
