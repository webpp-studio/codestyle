import os

BASE_DIR = os.path.dirname(__file__)

CONFIG_DIRS = (
    os.path.join(BASE_DIR, 'conf'),
)

def get_config_path(relative_path):
    path = None
    for dir_ in CONFIG_DIRS:
        abspath = os.path.join(dir_, relative_path)
        if os.path.exists(abspath):
            path = abspath
    return path
