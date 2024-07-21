import os


def data_path():
    return os.path.abspath(os.path.curdir) + "/dataset/data"


def env_path():
    return os.path.abspath(os.path.curdir) + "/config/.env"


def py_path():
    return os.path.abspath(os.path.curdir) + "/src"