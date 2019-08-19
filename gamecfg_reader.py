from re import search
from json import dumps
from sys import stderr


class GamecfgReader:
    def __init__(self, game_cfg_file_path):
        try:
            self.game_cfg_content = open(game_cfg_file_path).read()
        except OSError:
            stderr.write("Game.cfg file not found")
        self.line_list = self.get_line_list()
        self.game_config = self.get_game_config()
        self.json_data = dumps(self.game_config)

    def get_line_list(self):
        return [line for line in self.game_cfg_content.split('\n') if line]

    def get_game_config(self):
        config_dictionary = {}
        bind_action_dictionary = {}
        bind_command_to_key_dictionary = {}
        for _, line in enumerate(self.line_list):
            try:
                if 'BindAction' in line:
                    config = search('Input:(.*)\(\"(.*)\", \"(.*)\", \"(.*)\", (.*)\)', line).groups()
                    try:
                        bind_action_dictionary[config[1]].append(config[2:])
                    except:
                        bind_action_dictionary[config[1]] = [config[2:]]
                elif 'BindCommandToKey' in line:
                    config = search('Input:(.*)\(\"(.*)\", \"(.*)\", (.*)\)', line).groups()
                    try:
                        bind_command_to_key_dictionary[config[0]].append(config[1:])
                    except:
                        bind_command_to_key_dictionary[config[0]] = [config[1:]]
                    bind_command_to_key_dictionary[config[0]] = []
                elif 'SetMouseSensitivity' in line or 'SetInvertedMouse' in line:
                    config = search('Input:(.*)\((.*)\)', line).groups()
                    config_dictionary[config[0]] = config[1]
            except (IndexError, AttributeError):
                pass
        config_dictionary['bind_action'] = bind_action_dictionary
        config_dictionary['bind_command_to_key'] = bind_command_to_key_dictionary
        return config_dictionary
