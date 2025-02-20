import requests as req
import json

'''
    Module to fetch and parse batch API requests to RGL.GG to get players rank information
'''

### DEPRECATED

# def batch_request(steam_ids: list) -> dict | RuntimeError:
#     url = "https://api.rgl.gg/v0/profile/getmany"
#     headers = {
#     "accept": "*/*",
#     "Content-Type": "application/json"
#     }
    
#     response = req.post(url, headers=headers, json=steam_ids)

#     if response.ok:
#         return response.json()
        
#     else:
#         print(f"Error: {response.status_code}")
#         print(response.text)
#         return RuntimeError
    

# def single_request(steam_id) -> dict | int:
#     url = f'https://api.rgl.gg/v0/profile/{steam_id}'
#     res = req.get(url)

#     if res.ok:
#         return res.json()

#     else:
#         # print(f"Error: {res.status_code}")
#         # print(res.text)
#         return -1


# def parse_data(response: json) -> list:
#     player_data = []

#     if response == -1:
#         return
    
#     if isinstance(response, dict):
#         response = [response]

#     for player in response:
        
#         teams = player.get('currentTeams') or {}
#         sixes = (teams.get('sixes') or {}).get('divisionName', '')
#         highlander = (teams.get('highlander') or {}).get('divisionName', '')
#         prolander = (teams.get('prolander') or {}).get('divisionName', '')
    
#         data = {'sixes': sixes,
#                 'highlander': highlander,
#                 'prolander': prolander
#                 }

        

#         steam_id = player.get('steamId')

#         if steam_id is not None:
#             player_data.append({steam_id : data})
#         else:
#             print("Warning: Missing steamID for player:", player)
            
#     return player_data

###


def single_request(steam_id: int) -> list | int:
    url = f'https://api.rgl.gg/v0/profile/{steam_id}/teams'
    res = req.get(url)

    if res.ok:
        return res.json()

    else:
        # print(f"Error: {res.status_code}")
        # print(res.text)
        return -1
    

def parse_request(teams: list) -> tuple:
    if teams == -1:
        return (1, 1)
    
    with open("rank_conversion.json") as f:
        conv = json.load(f)

    allowed = list(conv['RGL'].keys())

    HL = [] # list to store integer values of ranks from each team
    SIXES = []

    for team in teams:
        if not (team.get("seasonName") or team.get("divisionName")): 
            continue

        if not team.get("divisionName") in allowed:
            continue
        
        if team["seasonName"].startswith("HL Season"):
            numeric_rank = conv["RGL"][team["divisionName"]]
            HL.append(numeric_rank)
        
        elif team["seasonName"].startswith("6s Season"):
            numeric_rank = conv["RGL"][team["divisionName"]]
            
            SIXES.append(numeric_rank)

    if not HL:
        HL.append(1)

    if not SIXES:
        SIXES.append(1)

    return (max(HL), max(SIXES))



# id = 76561198049086812
# print(parse_request(single_request(id)))





