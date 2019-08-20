from re import search
from json import dumps
from sys import stderr


class SystemReader:
    def __init__(self, system_file_path):
        try:
            self.system_file_content = open(system_file_path).read()
        except OSError:
            stderr.write("System.cfg file not found")
        self.line_list = self.get_line_list()
        self.setting_dictionary = self.get_setting_dictionary()
        self.json_data = dumps(self.setting_dictionary)

    def get_setting_dictionary(self):
        setting_dictionary = {}
        for line in self.line_list:
            regex_result = search('(.*) = \"(.*)\"', line)
            if regex_result:
                setting_dictionary[regex_result.group(1)] = regex_result.group(2)
        return setting_dictionary

    def get_line_list(self):
        return [line for line in self.system_file_content.split('\n') if line]