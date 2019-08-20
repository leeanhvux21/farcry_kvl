import requests
from log_reader import *
from gamecfg_reader import *
from system_reader import *
from hashlib import md5
from sys import argv

def call_API_submit(match_name, match_start_time,
                    match_end_time, match_frags,
                    token, player_name):
    url = "hhttps://farcryserver.herokuapp.com/farcryAPI/v1/matches/submit/"
    headers = {"Authorization":token}
    params = {
        "player_name":player_name,
    }
    data = {"match_name":match_name,
            "match_start_time":match_start_time,
            "match_end_time":match_end_time,
            "match_frags":match_frags,
            }
    response = requests.post(url, params=params, json=data, headers=headers)
    return response.status_code, response.json()


if __name__ == "__main__":
    log = Log(argv[1])
    call_API_submit(str(md5(log.json_data).digest()),log['session_start_time'],
                    log['session_end_time'], log['frags'],
                    , argv[2])