import requests as req
import json

'''
    Module to fetch and parse batch API requests to RGL.GG to get players rank information
'''


def batch_request(steam_ids: list):
    url = "https://api.rgl.gg/v0/profile/getmany"
    headers = {
    "accept": "*/*",
    "Content-Type": "application/json"
    }
    
    response = req.post(url, headers=headers, json=steam_ids)

    if response.ok:
        return response.json()
        
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return RuntimeError
    

def single_request(steam_id):
    url = f'https://api.rgl.gg/v0/profile/{steam_id}'
    res = req.get(url)

    if res.ok:
        return res.json()

    else:
        # print(f"Error: {res.status_code}")
        # print(res.text)
        return -1


def parse_data(response: json):
    player_data = []

    if response == -1:
        return
    
    if isinstance(response, dict):
        response = [response]

    for player in response:
        
        teams = player.get('currentTeams') or {}
        sixes = (teams.get('sixes') or {}).get('divisionName', '')
        highlander = (teams.get('highlander') or {}).get('divisionName', '')
        prolander = (teams.get('prolander') or {}).get('divisionName', '')
    
        data = {'sixes': sixes,
                'highlander': highlander,
                'prolander': prolander
                }

        

        steam_id = player.get('steamId')

        if steam_id is not None:
            player_data.append({steam_id : data})
        else:
            print("Warning: Missing steamID for player:", player)
            
    return player_data
