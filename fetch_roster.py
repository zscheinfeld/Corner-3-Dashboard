#!/usr/bin/env python3
"""
Fetch shot chart data for every player on the 2024-25 Knicks roster.
Skips any player whose file already exists (e.g. brunson_shots.json → shots_1628973.json).

Usage:
    .venv/bin/python3 fetch_roster.py
"""
import json, os, shutil, time
from nba_api.stats.endpoints import commonteamroster, shotchartdetail

KNICKS_ID = 1610612752
SEASON    = "2024-25"
DATA_DIR  = "data"

def get_roster():
    time.sleep(0.5)
    r  = commonteamroster.CommonTeamRoster(team_id=KNICKS_ID, season=SEASON)
    df = r.get_data_frames()[0]
    return [{"name": row["PLAYER"], "id": int(row["PLAYER_ID"])} for _, row in df.iterrows()]

def fetch_shots(player_id):
    time.sleep(1.2)  # polite delay
    chart = shotchartdetail.ShotChartDetail(
        team_id=0,
        player_id=player_id,
        season_nullable=SEASON,
        season_type_all_star="Regular Season",
        context_measure_simple="FGA",
        timeout=60,
    )
    return chart.get_data_frames()[0].to_dict(orient="records")

def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    # Migrate existing Brunson file if present
    old = os.path.join(DATA_DIR, "brunson_shots.json")
    new = os.path.join(DATA_DIR, "shots_1628973.json")
    if os.path.exists(old) and not os.path.exists(new):
        shutil.copy(old, new)
        print("✓ Copied brunson_shots.json → shots_1628973.json")

    roster = get_roster()
    print(f"Roster: {len(roster)} players\n")

    for p in roster:
        out = os.path.join(DATA_DIR, f"shots_{p['id']}.json")
        if os.path.exists(out):
            print(f"  ↳ {p['name']:25s} already cached")
            continue

        print(f"  Fetching {p['name']}…", end=" ", flush=True)
        try:
            shots = fetch_shots(p["id"])
            with open(out, "w") as f:
                json.dump(shots, f)
            made = sum(1 for s in shots if s["SHOT_MADE_FLAG"] == 1)
            print(f"{len(shots)} shots  ({made} made)")
        except Exception as e:
            print(f"ERROR — {e}")

    print("\nDone. Reload http://localhost:8000")

if __name__ == "__main__":
    main()
