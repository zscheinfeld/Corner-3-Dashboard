#!/usr/bin/env python3
"""
Fetch Jalen Brunson's 2024-25 shot chart data via nba_api.
Run once to generate data/brunson_shots.json, then open index.html.

Usage:
    .venv/bin/python3 fetch_brunson.py
    python3 -m http.server 8000
    open http://localhost:8000
"""
import json
import os
from nba_api.stats.endpoints import shotchartdetail

PLAYER_ID = 1628973   # Jalen Brunson
SEASON    = "2024-25"

def fetch_shots():
    print("Fetching shot data from NBA Stats API (may take 10-20s)...")

    chart = shotchartdetail.ShotChartDetail(
        team_id=0,
        player_id=PLAYER_ID,
        season_nullable=SEASON,
        season_type_all_star="Regular Season",
        context_measure_simple="FGA",
        timeout=60,
    )

    df = chart.get_data_frames()[0]
    shots = df.to_dict(orient="records")
    return shots


def main():
    os.makedirs("data", exist_ok=True)

    shots = fetch_shots()

    out_path = "data/brunson_shots.json"
    with open(out_path, "w") as f:
        json.dump(shots, f)

    made   = sum(1 for s in shots if s["SHOT_MADE_FLAG"] == 1)
    missed = len(shots) - made
    print(f"✓  {len(shots)} shots saved  ({made} made / {missed} missed)")
    print(f"   → {out_path}")
    print()
    print("Now serve the project:")
    print("   python3 -m http.server 8000")
    print("   open http://localhost:8000")


if __name__ == "__main__":
    main()
