import pandas as pd
from tqdm import tqdm

RGL_FN = 'RGL.csv'
ETF2L_FN = 'ETF2l.csv'
TRENDSTF_FN = 'TrendsTF.csv'



df_trends = pd.read_csv(TRENDSTF_FN)
df_rgl = pd.read_csv(RGL_FN)
df_etf2l = pd.read_csv(ETF2L_FN)

print("joining dataframes...")
merged_df = df_trends.merge(df_rgl, on="SteamID", how="outer")
merged_df = merged_df.merge(df_etf2l, on="SteamID", how="outer")

'''
    Here's where I will handle the empty value cases (should be NaN or None)
    This only seems to happen when either RGL or the ETF2L api returns a 404 for the player
'''
merged_df.fillna(0, inplace=True) # filled with 0 to denote it being a null value


print("outputting to CSV...")
merged_df.to_csv("players.csv", index=False)
print("Done!")
