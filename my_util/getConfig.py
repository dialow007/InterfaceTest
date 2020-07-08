import os
import yaml


class GetConfig(object):
    def __init__(self,filename):
        self.file_name = filename

    def get_conf(self, key):
        """
        @param key: 配置文件中的key，获取这个key的数据
        @return:
        """
        data = self.read_yaml()
        return data[key]


    def read_yaml(self):
        with open(self.file_name, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        return data
