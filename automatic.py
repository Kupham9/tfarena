import TrendsTF as ttf
import RGL as rgl
import ETF2L as etf2l
import json
import pandas as pd
import threading
import time
from tqdm import tqdm
import os

BASE_CSV_DIR = os.path.join(os.path.dirname(__file__), "csvs")
os.makedirs(BASE_CSV_DIR, exist_ok=True) 

RGL_FN = os.path.join(BASE_CSV_DIR, "RGL.csv")
ETF2L_FN = os.path.join(BASE_CSV_DIR, "ETF2L.csv")
TRENDSTF_FN = os.path.join(BASE_CSV_DIR, "TrendsTF.csv")
CONV_JSON = os.path.join(BASE_CSV_DIR, "rank_conversion.json")

SLEEP_VALUE_TTF = 9.5 # time delay between TrendsTF requests
SLEEP_VALUE_RGL = 3 # time delay between RGL API requests
SLEEP_VALUE_ETF2L = 3 # time delay between ETF2L requests

CSV_HEADERS = {
    TRENDSTF_FN: "Username,SteamID,Steam Profile URL,Logs,Wins-Losses-Ties,Winrate,Rounds Won-Lost-Tied,Round winrate,Kills,Deaths,Assists,Time played,Damage,Damage taken,Heals received,Airshots,Medkit score,Healing from medkits,Backstabs,Headshots,Headshot kills,Sentry score,Healing,Capture points captured,Intelligences captured,Übers,Drops,Advantages lost,Deaths after über,Deaths before über,Kills per 30 minutes,Deaths per 30 minutes,Assists per 30 minutes,Damage per minute,Damage taken per minute,Heals received per minute,Airshots per 30 minutes,Medkit score per 30 minutes,Healing from medkits per minute,Backstabs per 30 minutes,Headshots per 30 minutes,Headshot kills per 30 minutes,Sentry score per 30 minutes,Capture points captured per 30 minutes,Intelligences captured per 30 minutes,Healing per minute,Übers per 30 minutes,Drops per 30 minutes,Advantages lost per 30 minutes,Deaths after über per 30 minutes,Deaths before über per 30 minutes",
    ETF2L_FN   : "SteamID,ETF2L Sixes,ETF2L Highlander",
    RGL_FN     : "SteamID,RGL Sixes Division,RGL Highlander Division",
}		


# def convert_id64_to_id3(id64: int) -> tuple[int, str]:
#     conversion_factor: int = 76561197960265728
#     id3_prefix = 'U:1:'
#     id3 = abs(id64 - conversion_factor) 
#     return (id3, id3_prefix + id3)


# def get_rank_conversions(filename: str) -> json:
#     with open(filename) as f:
#         return json.loads(f)

def validateIDFormat(steam_id: str) -> int:
    steam_id = steam_id.strip()
    if len(steam_id) == 17 and steam_id.isnumeric():
        return 1 # valid, return 1
    elif steam_id.lower() == "null":
        return 0 # valid, return 0

    return -1 # invalid, return -1


# TrendsTF loop:
def trendsTF_main_loop(ids: list) -> None:
    header_cols = CSV_HEADERS[TRENDSTF_FN].split(",")
    for id in tqdm(ids, desc="TTF", position=0, leave=True, colour="blue"):
        id = id.strip()

        if validateIDFormat(id) == -1:
            continue

        elif validateIDFormat(id) == 0:
            data = [""] * len(header_cols)
            # data[header_cols.index("SteamID")] = id

        else:
            time.sleep(SLEEP_VALUE_TTF)
            req = ttf.get_player_https_request(id)
            if hasattr(req, "text"):
                data = ttf.parse_player_data(req, id)
                if not data:                # API failed → blank row
                    data = [""] * len(header_cols)
                # data[header_cols.index("SteamID")] = id
        


        pd.DataFrame([data], columns=header_cols).to_csv(
            TRENDSTF_FN, mode="a",
            header=not os.path.exists(TRENDSTF_FN),
            index=False
        )


def rgl_main_loop(ids: list) -> None:
    header_cols = CSV_HEADERS[RGL_FN].split(",")
    for id in tqdm(ids, desc="RGL", position=1, leave=True, colour='red'):
        id = id.strip()
        if validateIDFormat(id) == 1:
            req = rgl.single_request(id)
            time.sleep(SLEEP_VALUE_RGL)
            if req == -1:
                continue # skipping garbage ID
            else:
                rank = rgl.parse_request(req)
                if rank is None:
                    data = [""] * len(header_cols)
                    # data[header_cols.index("SteamID")] = id
                else:
                    data = [id, rank[0], rank[1]]

        elif validateIDFormat(id) == 0:
            data = [""] * len(header_cols)
            # data[header_cols.index("SteamID")] = id

        else:
            # print(f"Invalid ID: {id} entered...")
            # print("Skipping...")
            continue

        pd.DataFrame([data], columns=header_cols).to_csv(RGL_FN, mode="a", header=not os.path.exists(RGL_FN),index=False)


def etf2l_main_loop(ids: list) -> None:
    header_cols = CSV_HEADERS[ETF2L_FN].split(",")
    for id in tqdm(ids, desc="ETF2L", position=2, leave=True, colour='green'):
        id = id.strip()
        if validateIDFormat(id) == -1:
            continue # garbage ID, skip

        elif validateIDFormat(id) == 0:
            data = [""] * len(header_cols)

        if validateIDFormat(id) == 1:
            rank = etf2l.parse_req_json(etf2l.single_request(id))
            time.sleep(SLEEP_VALUE_ETF2L)
            if rank is None:
                data = [""] * len(header_cols)
            else:
                data = [id, rank[0], rank[1]]
                
        
        pd.DataFrame([data], columns=header_cols).to_csv(ETF2L_FN, mode="a", header=not os.path.exists(ETF2L_FN),index=False)
        
        


def ensure_csv(path, header_line):
    if (not os.path.exists(path)) or os.path.getsize(path) == 0:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(header_line + "\n")
        print(f"[init] created empty cache: {path}")

def init_cache_files():
    for fn, hdr in CSV_HEADERS.items():
        ensure_csv(fn, hdr)
#main loop:

def main() -> None:
    init_cache_files()

    ids = []
    # open file of steam ids and verify length and whether it is numeric
    with open('steam_ids.txt') as steam_ids:
        for steam_id in steam_ids.readlines():
            # print(steam_id, '\t', type(steam_id))
            steam_id = steam_id.strip()
            if len(steam_id) == 17 and steam_id.isnumeric(): # has to be 17 in length
                ids.append(steam_id)
            else:
                ids.append('null')
    print("Opened Steam IDs...")

    # threading each task in parallel
    t1 = threading.Thread(target=trendsTF_main_loop, args=(ids,))
    t2 = threading.Thread(target=rgl_main_loop, args=(ids,))
    t3 = threading.Thread(target=etf2l_main_loop, args=(ids,))


    t1.start()
    t2.start()
    t3.start()


    t1.join()
    t2.join()


    print('Done!')
     
    
if __name__ == "__main__":
    main()

