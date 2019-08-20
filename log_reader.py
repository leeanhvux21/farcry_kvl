from sys import stderr
from os import path
from re import search
from info_handler import *


def read_file(file_path_name):
    if not path.exists(file_path_name):
        raise OSError('File not found')
    elif path.isfile(file_path_name):
        return [line for line in open(file_path_name).read().split('\n') if line]
    elif path.isdir(file_path_name):
        raise OSError(file_path_name, ' is a directory')


def parse_frag(log_info, pattern_dict):
    time = ''
    for type, pattern in pattern_dict.items():
        re_result = search(pattern, log_info)
        if re_result:
            return eval('handel_' + pattern_name + '(' + re_result + ',')
        else:
            return None


def handle_frag(info_group):
    pass


def handle_start_time(info_group):
    pass

if __name__ == '__main__':
    pass

