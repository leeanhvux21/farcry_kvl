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
    """
    :param log_info: (str) a line or an element in the log file
    :param pattern_dict: (dict) dictionary with key is the type of log_info and
    value is the pattern for regex
    :return: (list) infomation get from log_info
    """
    for info_type, pattern in pattern_dict.items():
        try:
            regex_result = search(pattern, log_info)
        except TypeError as Error:
            stderr.write(Error)
        if regex_result:
            try:
                return eval('handel_' + info_type + '(' + regex_result + ',')
            except (NameError, TypeError) as Error:
                stderr.write(Error)
                

def check_if_hour_increase(time_1, time_2):
    if (int(time_1[0]) * 60 + int(time_1[1])) > (int(time_2[0]) * 60 + int(time_2[1])):
        return True
    return False


def handle_frag(regex_result):
    info_list = regex_result.groups()
    if len(info_list) == 5:
        frag_info_dict = {
            'suicide':False,
            'time':{
                'minute':info_list[0],
                'second':info_list[1]},
            'killer':info_list[2],
            'weapon':info_list[3],
            'victim':info_list[4]
        }
    elif len(info_list) == 3:
        frag_info_dict = {
            'suicide':True,
            'time':{
                'minute':info_list[0],
                'second':info_list[1]},
            'killer':None,
            'weapon':None,
            'victim':info_list[2]
        }
    return frag_info_dict


def handle_start_time(regex_result):
    pass


def handle_end_time(regex_result):
    pass



if __name__ == '__main__':
    pattern_dict = {
        'frag' : '(.*):(.*)> <Lua> ([^ ]*) killed ([^ ]*) \
            with ([^ \n]*)|<(.*):(.*)> <Lua> ([^ ]*) killed itself',
        'start_time':'',
        'end_time':'',
        'normal_info_line':'<([0-5][0-9]):([0-5][0-9])>',
        'player_name':"OS User name: '(.*)'"
    }