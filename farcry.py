from datetime import datetime
from datetime import timedelta
from re import search
from sys import argv
from json import dumps


class Log(dict):
    def __init__(self, log_file_pathname):
        self.log_file_pathname = log_file_pathname
        self.log_data = self.read_log_file()
        self.cvar_dictionary = self.get_cvar_dictionary()
        self.start_time = self.parse_log_start_time()
        self.map_name, self.mode_name = self.parse_session_mode_and_map()
        self.frags, self.delta = self.parse_frags()
        self.session_start_time, self.session_end_time = self. \
            parse_game_session_start_and_end_times()
        self.json_data = self.convert_data_to_json()

    def read_log_file(self):
        """
        return bytes object
        :param log_file_pathname: path to the log_file file
        :return: string object
        """
        try:
            with open(self.log_file_pathname, 'r') as data:
                return data.read().split('\n')
        except OSError:
            return ''

    def get_cvar_dictionary(self):
        """
        read the log data, if a line contain cvar, get its name as a key and
        its value as a value in cvar_dictionary
        :return: dictionary
        """
        cvar_dictionary = {}
        for line in self.log_data:
            if 'cvar' in line:
                try:
                    name, value = search('[(](.*)[)]', line).groups()[0]. \
                        split(',')
                    cvar_dictionary[name] = value
                except ValueError:
                    pass
        return cvar_dictionary

    def parse_log_start_time(self):
        """
        get a date_time object by read the first line of the log_file
        :return: date_time object
        """
        start_time_info = self.log_data[0][2:]
        time_zone = self.cvar_dictionary['g_timezone']
        if len(time_zone) == 2:
            time_zone = time_zone[0] + '0' + time_zone[1] + '00'
        else:
            time_zone = '+' + '0' + time_zone + '00'
        start_time_info += time_zone
        for index, charactor in enumerate(start_time_info):
            if charactor == ',':
                return datetime.strptime(start_time_info[index + 2:],
                                         '%B %d, %Y %H:%M:%S%z')

    def parse_session_mode_and_map(self):
        """
        get map and mode name
        :param log_data: string
        :return: tuple
        """
        for line in self.log_data:
            if 'Loading level' in line:
                map, mode = search('.*Levels/(.*), mission (.*) .*',
                                   line).groups()
                return map, mode

    def check_if_hour_increase(self,
                               current_time,
                               flag):
        """
        get current_time and flag as 2 string reference for current line's time
        and the last line's time, compare them if current time is smaller than
        flag that mean the hour increase 1
        :param current_time: string
        :param flag: string
        :return: Boolean
        """
        flag_minute, flag_second = flag.split(':')
        current_time_minute, current_time_second = current_time.split(':')
        if int(current_time_minute) > int(flag_minute):
            return False
        elif int(current_time_minute) < int(flag_minute):
            return True
        else:
            if int(current_time_second) > int(flag_second):
                return False
            elif int(current_time_second) < int(flag_second):
                return True

    def increase_time(self,
                      current_time,
                      delta_hour,
                      delta_day):
        """
        get current as a string("<nn:nn>"), return a datetime object base on
        delta hour and delta day.
        :param current_time: string
        :param delta_hour: int
        :param delta_day: int
        :return: datetime object
        """
        start_time = self.start_time
        current_minute, current_second = current_time.split(':')
        current_time = start_time.replace(minute=int(current_minute),
                                          second=int(current_second)) + \
                                          timedelta(hours=delta_hour,
                                                    days=delta_day)
        return current_time

    def parse_frags(self):
        """
        get data from log file and return a list of kill information. Kill
        information is a tuple contain time, killer, weapon and victim. If
        there some suicides, the kill information only contain time and his
        name
        :param log_data: string
        :return: list
        """
        delta_hour = 0
        delta_day = 0
        kill_infomation_list = []
        flag = '00:00'
        for line in self.log_data:
            kill_infomation = line.split()
            try:
                kill_infomation[0] = kill_infomation[0][1:-1]
            except IndexError:
                continue
            if not search('[0-9][0-9]:[0-9][0-9]',
                          kill_infomation[0]):
                continue
            if 'itself' in kill_infomation:
                kill_infomation = kill_infomation[:3]
                kill_infomation.pop(1)
            elif 'killed' in line and 'with' in line:
                kill_infomation = [x for x in kill_infomation if x
                                   not in ['killed',
                                           'with',
                                           '<Lua>']]
            else:
                try:
                    if self.check_if_hour_increase(kill_infomation[0],
                                                   flag):
                        delta_hour += 1
                    flag = kill_infomation[0]
                    continue
                except (ValueError, IndexError):
                    continue
            if self.check_if_hour_increase(kill_infomation[0],
                                           flag):
                delta_hour += 1
            flag = kill_infomation[0]
            kill_infomation[0] = self.increase_time(kill_infomation[0],
                                                    delta_hour,
                                                    delta_day)
            kill_infomation_list.append(tuple(kill_infomation))
            if delta_hour > 24:
                delta_day += 1
        return kill_infomation_list, [delta_hour, delta_day]

    def parse_game_session_start_and_end_times(self):
        for line in self.log_data:
            if search('<[0-9][0-9]:[0-9][0-9]>  Level ' +
                      self.map_name + ' loaded in .* seconds', line):
                session_start_time = line.split()[0][1:-1]
            elif 'Statistics' in line:
                session_end_time = line.split()[0][1:-1]
        session_start_time = self.increase_time(session_start_time, 0, 0)
        try:
            session_end_time
        except ValueError:
            session_end_time = self.log_data[-1].split('')[0][-1:1]
        session_end_time = self.increase_time(session_end_time,
                                              self.delta[0],
                                              self.delta[1])
        return session_start_time, session_end_time


    def convert_data_to_json(self):
        pass


class Reporter:
    def __init__(self, log_data):
        pass

    def json(self):
        pass


class Stupid(dict):
    def __init__(self):
        self['asd'] = 'qwe'
        self.zxc = self.get_stupid()

    def get_stupid(self):
        self['map'] = 123
        self['mode'] = 456
        return 1

if __name__ == '__main__':
    log = Log(argv[1])
    # print(log.json_data)
    stupid = Stupid()
    # print(stupid['asd'])
    print(dumps(stupid))