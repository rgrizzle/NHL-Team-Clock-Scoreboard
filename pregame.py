from game_utils import get_pregame_info

def test_get_pregame():
    try:
        print("Starting pregame.py...")
        home_team_abbr = "COL"
        away_team_abbr = "WPG"
        
        home_pregame_info, away_pregame_info = get_pregame_info(home_team_abbr, away_team_abbr)
        print(f"home: {home_pregame_info}")
        print(f"away: {away_pregame_info}")
        
        print("pregame.py completed.")
    except Exception as e:
        print(f"Error: {e}")

# Ensure the function runs when executing pregame.py
if __name__ == "__main__":
    test_get_pregame()
