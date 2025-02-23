import TrendsTF as ttf
import RGL as rgl
import ETF2L as etf2l
import json
import pandas as pd
import threading
import time
from tqdm import tqdm

RGL_FN = 'RGL.csv' #rgl csv file name
ETF2L_FN = 'ETF2l.csv' #etf2l csv file name
TRENDSTF_FN = 'TrendsTF.csv' # trendstf csv file name
CONV_JSON = 'rank_conversion.json' # rank conversion file name
SLEEP_VALUE_TTF = 9.5 # time delay between TrendsTF requests
SLEEP_VALUE_RGL = 3 # time delay between RGL API requests
SLEEP_VALUE_ETF2L = 3 # time delay between ETF2L requests


# def convert_id64_to_id3(id64: int) -> tuple[int, str]:
#     conversion_factor: int = 76561197960265728
#     id3_prefix = 'U:1:'
#     id3 = abs(id64 - conversion_factor) 
#     return (id3, id3_prefix + id3)


# def get_rank_conversions(filename: str) -> json:
#     with open(filename) as f:
#         return json.loads(f)

# def append_row(frame, data):
#     frame.loc[len(frame)] = data
#     return(frame)


# TrendsTF loop:
def trendsTF_main_loop(ids: list) -> None:
    for id in tqdm(ids, desc="TTF", position=0, leave=True, colour="blue"):
        trends_df = pd.read_csv(TRENDSTF_FN)
        steam_id_set = set(trends_df['SteamID'].astype(str))
        if id not in steam_id_set:
            data = ttf.parse_player_data(ttf.get_player_https_request(id), id)
            if data:
                trends_df.loc[len(trends_df)] = data
                time.sleep(SLEEP_VALUE_TTF) # added to avoid rate limiting... fml
            # print(f"TTF: {id}")
        trends_df.to_csv(TRENDSTF_FN, index=False, mode="w")
    




def rgl_main_loop(ids: list) -> None:
    for id in tqdm(ids, desc="RGL", position=1, leave=True, colour='red'):
        rgl_df = pd.read_csv(RGL_FN)
        steam_id_set = set(rgl_df['SteamID'].astype(str))
        if id not in steam_id_set:
            rank = rgl.parse_request((rgl.single_request(id)))
            row = [id, rank[0], rank[1]]
            rgl_df.loc[len(rgl_df)] = row
            time.sleep(SLEEP_VALUE_RGL)
            # print(f"RGL: {id}")

        rgl_df.to_csv(RGL_FN, index=False, mode="w")



def etf2l_main_loop(ids: list) -> None:
    for id in tqdm(ids, desc="ETF2L", position=2, leave=True, colour='green'):
        etf2l_df = pd.read_csv(ETF2L_FN)
        steam_id_set = set(etf2l_df['SteamID'].astype(str))
        if id not in steam_id_set:
            data = etf2l.parse_req_json(etf2l.single_request(id))
            if data:
                row = [id, data[0], data[1]]
                etf2l_df.loc[len(etf2l_df)] = row
                time.sleep(SLEEP_VALUE_ETF2L)
            # print(f"ETF2L: {id}")
        etf2l_df.to_csv(ETF2L_FN, index=False, mode="w")



#main loop:

def main() -> None:
    ids = []
    # open file of steam ids and verify length and whether it is numeric
    with open('steam_ids.txt') as steam_ids:
        for steam_id in steam_ids.readlines():
            # print(steam_id, '\t', type(steam_id))
            steam_id = steam_id.strip()
            if len(steam_id) == 17 and steam_id.isnumeric(): # has to be 17 in length
                ids.append(steam_id)
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

