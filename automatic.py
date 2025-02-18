import TrendsTF as ttf
import RGL as rgl
import ETF2L as etf2l
import json
import pandas as pd
import threading
import time

RGL_FN = 'RGL.csv'
ETF2L_FN = 'ETF2l.csv'
TRENDSTF_FN = 'TrendsTF.csv'
CONV_JSON = 'rank_conversion.json'
SLEEP_VALUE_TTF = 9.5
SLEEP_VALUE_RGL = 3
SLEEP_VALUE_ETF2L = 3


def convert_id64_to_id3(id64: int) -> tuple[int, str]:
    conversion_factor: int = 76561197960265728
    id3_prefix = 'U:1:'
    id3 = abs(id64 - conversion_factor) 
    return (id3, id3_prefix + id3)


def get_rank_conversions(filename: str) -> json:
    with open(filename) as f:
        return json.loads(f)

def append_row(frame, data):
    frame.loc[len(frame)] = data
    return(frame)


# TrendsTF loop:
def trendsTF_main_loop(ids):
    trends_df = pd.read_csv(TRENDSTF_FN)

    for id in ids:
        steam_id_set = set(trends_df['SteamID'].astype(str))
        if id not in steam_id_set:
            data = ttf.parse_player_data(ttf.get_player_https_request(id), id)
            if data:
                trends_df.loc[len(trends_df)] = data
                time.sleep(SLEEP_VALUE_TTF) # added to avoid rate limiting... fml

    trends_df.to_csv(TRENDSTF_FN, index=False)




def rgl_main_loop(ids):
    rgl_df = pd.read_csv(RGL_FN)
    for id in ids:
        steam_id_set = set(rgl_df['SteamID'].astype(str))
        if id not in steam_id_set:
            data = rgl.parse_data((rgl.single_request(id)))
            if data:
                with open(CONV_JSON) as f:
                    conv = json.load(f)

                steam_id =  list(data[0].keys())[0]
                fields = data[0][steam_id]
                
                val = [steam_id, conv['RGL'][fields.get('sixes')], conv['RGL'][fields.get('highlander')], conv['RGL'][fields.get('prolander')]]
                rgl_df.loc[len(rgl_df)] = val
                time.sleep(SLEEP_VALUE_RGL)


    rgl_df.to_csv(RGL_FN, index=False)



def etf2l_main_loop(ids):
    etf2l_df = pd.read_csv(ETF2L_FN)
    for id in ids:
        steam_id_set = set(etf2l_df['SteamID'].astype(str))
        if id not in steam_id_set:
            data = etf2l.parse_req_json(etf2l.single_request(id))
            if data:
                val = [id, data[0], data[1]]
                etf2l_df.loc[len(etf2l_df)] = val
                time.sleep(SLEEP_VALUE_ETF2L)

    etf2l_df.to_csv(ETF2L_FN, index=False)



#main loop:

def main():
    ids = []
    # open file of steam ids and verify length and whether it is numeric
    with open('steam_ids.txt') as steam_ids:
        for steam_id in steam_ids.readlines():
            # print(steam_id, '\t', type(steam_id))
            steam_id = steam_id.strip()
            if len(steam_id) == 17 and steam_id.isnumeric(): # has to be 17 in length
                ids.append(steam_id)


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
