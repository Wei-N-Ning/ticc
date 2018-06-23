
import os


def file_path(file_name):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), file_name))
