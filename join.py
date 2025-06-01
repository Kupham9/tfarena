# join.py
import pandas as pd
import os

BASE = os.path.join(os.path.dirname(__file__), "csvs")
FILES = {
    "ttf":  os.path.join(BASE, "TrendsTF.csv"),
    "rgl":  os.path.join(BASE, "RGL.csv"),
    "etf":  os.path.join(BASE, "ETF2L.csv"),
}
OUT   = os.path.join(BASE, "players.csv")

# ── read the three caches ───────────────────────────────────────────────────────
ttf  = pd.read_csv(FILES["ttf"])
rgl  = pd.read_csv(FILES["rgl"])
etf  = pd.read_csv(FILES["etf"])

# quick sanity-check – tells you immediately if the files slipped out of sync
if not (len(ttf) == len(rgl) == len(etf)):
    raise ValueError(
        f"Row-count mismatch: TrendsTF={len(ttf)}, RGL={len(rgl)}, ETF2L={len(etf)}"
    )

# get rid of the extra SteamID columns so we keep only the one that’s already in ttf
rgl = rgl.drop(columns=["SteamID"], errors="ignore")
etf = etf.drop(columns=["SteamID"], errors="ignore")

# ── horizontal concatenation keeps the exact row order you already have ─────────
players = pd.concat([ttf, rgl, etf], axis=1)

# **don’t** overwrite blanks – leave NaN/"" exactly as they are
players.to_csv(OUT, index=False)
print("Done!")