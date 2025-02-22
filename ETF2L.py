import requests as req
import json
import pprint as pp

def single_request(steam_id):
    url = f'https://api-v2.etf2l.org/player/{steam_id}'
    res = req.get(url)

    if res.ok:
        return res.json()
        
    else:
        # print(f"Error: {res.status_code}")
        return -1
        # print(res.text)
        # raise ValueError("Error during runtime!")
    

def parse_req_json(data):
    competitions = ['Highlander Season', '6v6 Season']

    with open("rank_conversion.json", "r") as f:
        conv = json.load(f)

    HL_comps = []
    SIXES_comps = []

    if data == -1:
        return (1, 1)


    for team in data["player"].get("teams", []):
        for comp in team.get("competitions", {}).values():
            category = comp.get("category", "")
            if category in competitions:
                div_name = comp.get("division").get("name")
                if div_name:
                    if category == competitions[0]:
                        HL_comps.append(div_name)
                    else:
                        SIXES_comps.append(div_name)
    HL_temp = []
    SIXES_temp = []  

    for comp in HL_comps:
        HL_temp.append(conv['ETF2L'][comp])

    for comp in SIXES_comps:
        SIXES_temp.append(conv['ETF2L'][comp])

    if not HL_temp:
        HL_temp.append(1)

    if not SIXES_temp:
        SIXES_temp.append(1)



    return (max(SIXES_temp), max(HL_temp))

