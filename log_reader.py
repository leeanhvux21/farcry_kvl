from sys import stderr
from os import path
from re import search
from info_handler import *
from datetime import datetime, timedelta


def read_file(file_path_name):
    if not path.exists(file_path_name):
        raise OSError('File not found')
    elif path.isfile(file_path_name):
        return [line for line in open(file_path_name).read().split('\n') if line]
    elif path.isdir(file_path_name):
        raise OSError(file_path_name, ' is a directory')    


def parse_special_log_info(log_index, log_info, pattern_dict):
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
                return eval('handel_' + info_type + '(log_index, regex_result.groups())')
            except (NameError, TypeError) as Error:
                stderr.write(Error)


def convert_to_datetime(log_start_time, delta_hour, minute, second):
    
    pass


def handle_frag(log_index, info_list):
    if len(info_list) == 5:
        frag_info_dict = {
            'index': log_index,
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
            'index':log_index,
            'suicide':True,
            'time':{
                'minute':info_list[0],
                'second':info_list[1]},
            'killer':None,
            'weapon':None,
            'victim':info_list[2]
        }
    return frag_info_dict


def handle_session_start_time(index, info_list, delta_hour):
    pass
    


def handle_session_end_time(index, info_list, delta_hour):
    pass



if __name__ == '__main__':
    pattern_dict = {
        'frag' : '<([0-5][0-9]):([0-5][0-9])> <Lua> ([^ ]*) killed ([^ ]*) \
            with ([^ \n]*)|<([0-5][0-9]):([0-5][0-9])> <Lua> ([^ ]*) killed itself',
        'start_time':'<([0-5][0-9]):([0-5][0-9])>  Level [^ ]* loaded in [^ ] seconds',
        'end_time':'<([0-5][0-9]):([0-5][0-9])> == Statistics * ==',
        'log_start_time':'Log Started at [^ ]*, ([^ ]*) ([0-2][0-9]), ([0-9]{4}) ([0-5][0-9]):[0-5][0-9]:[0-5][0-9]'
    }