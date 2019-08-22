from datetime import datetime
from hashlib import sha1


class TimeMark:
    def __init__(self):
        self.index = index
        self.time = time
        self.hash_value = hash_value

    def increase_time(self):
        pass


class LogTimeHandler:
    def __init__(self, base_time):
        self.base_time = base_time
        self.time_mark_dict = []

    def increase_time_mark(self, time_mark):
        self.time_mark_dict[time_mark.index] = time_mark

    @staticmethod
    def check_if_hour_increase(time_1, time_2):
        if (int(time_1[0]) * 60 + int(time_1[1])) > (int(time_2[0]) * 60 + int(time_2[1])):
            return True
        return False

    def get_delta_time(self):
        pass
    