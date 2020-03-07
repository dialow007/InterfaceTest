import os


def get_base_dir():
    path = os.path.split(os.path.realpath(__file__))[0]
    return path
