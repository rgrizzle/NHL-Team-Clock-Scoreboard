import requests
from constants import *
from datetime import datetime, timedelta, timezone
import pytz


# Function to fetch the NHL schedule
def fetch_nhl_schedule(team_abbr):
    url = f"https://api-web.nhle.com/v1/club-schedule-season/{team_abbr}/now"
    print(f"Request URL: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        print("Request Successful")
        return response.json()
    else:
        print(f"Failed to fetch schedule for {team_abbr}")
        return None


# Function to get previous and next game info
def get_prev_and_next_game_info(team_abbr, local_tz):
    today = datetime.now().date()  # Convert `today` to just a `date` object
    now = datetime.now(pytz.utc)
    
    # Fetch NHL Schedule
    schedule_data = fetch_nhl_schedule(team_abbr)

    if not schedule_data:
        return None, None

    games = schedule_data.get("games", [])
    print(f"Number of Games Retrieved: {len(games)}")

    previous_game = None
    next_game = None
    current_game = None

    # Loop through games to find the previous and next game
    for game in games:
        game_date = datetime.strptime(game["gameDate"], "%Y-%m-%d").date()# Convert to `date` object
        game_start_time = datetime.strptime(game["startTimeUTC"], "%Y-%m-%dT%H:%M:%SZ")  # Convert to datetime
        game_start_time = pytz.utc.localize(game_start_time)  # Localize as UTC

        game_state = game["gameState"]
        
        if game_state == "LIVE" or game_state == "CRIT" or game_state == "PRE":
            current_game = game
        elif game_start_time < now and (game_state == "OFF" or game_state == "FINAL"):
            previous_game = game
        elif game_start_time >= now and next_game is None:
            next_game = game

    # Extract relevant information
    prev_game_info = None
    next_game_info = None
    current_game_info = None

    if previous_game:
        prev_game_info = {
            "game_id": previous_game["id"],
            "date": previous_game["gameDate"],
            "opponent": previous_game["awayTeam"]["placeName"]["default"]
            if previous_game["homeTeam"]["abbrev"] == team_abbr
            else previous_game["homeTeam"]["placeName"]["default"],
            "score": f"{previous_game['homeTeam']['score']} - {previous_game['awayTeam']['score']}",
            "result": f"WIN"
            if (
                (previous_game["homeTeam"]["abbrev"] == team_abbr and previous_game["homeTeam"]["score"] > previous_game["awayTeam"]["score"])
                or (previous_game["awayTeam"]["abbrev"] == team_abbr and previous_game["awayTeam"]["score"] > previous_game["homeTeam"]["score"])
            )
            else f"LOSS",
            "away_score": f"{previous_game['awayTeam']['commonName']['default']} {previous_game['awayTeam']['score']}",
            "home_score": f"{previous_game['homeTeam']['commonName']['default']} {previous_game['homeTeam']['score']}",
            "last_period_type": previous_game["gameOutcome"]["lastPeriodType"]
        }

        if next_game:
            next_game_date = datetime.strptime(next_game["gameDate"], "%Y-%m-%d").date()
            current_date = datetime.now().date()
            next_game_state = next_game["gameState"]

            # Convert and format the game time
            start_time_utc = datetime.strptime(next_game["startTimeUTC"], "%Y-%m-%dT%H:%M:%SZ")
            start_time_utc = pytz.utc.localize(start_time_utc)
            start_time_local = start_time_utc.astimezone(pytz.timezone("America/Los_Angeles"))

            # Format the time and remove the leading zero manually
            next_game_time = start_time_local.strftime("%I:%M %p").lstrip("0")


            # Determine the next game date string
            if next_game_date == current_date:
                next_game_date_str = "Today"
            elif next_game_date == (current_date + timedelta(days=1)):
                next_game_date_str = "Tomorrow"
            else:
                next_game_date_str = next_game_date.strftime("%a, %b %d")

            # Prepare the next game info
            next_game_info = {
                "game_id": next_game["id"],
                "game_state": next_game["gameState"],
                "date": next_game_date_str,
                "time": next_game_time,
                "start_time_local": start_time_local, 
                "start_time_utc": start_time_utc,
                "opponent": next_game["awayTeam"]["placeName"]["default"]
                if next_game["homeTeam"]["abbrev"] == team_abbr
                else next_game["homeTeam"]["placeName"]["default"],
                "matchup": f"{next_game['awayTeam']['placeName']['default']} @ {next_game['homeTeam']['placeName']['default']}",
            }

        if current_game:
            # Convert and format the game time
            start_time_utc = datetime.strptime(current_game["startTimeUTC"], "%Y-%m-%dT%H:%M:%SZ")
            start_time_utc = pytz.utc.localize(start_time_utc)
            start_time_local = start_time_utc.astimezone(pytz.timezone("America/Los_Angeles"))
            
            current_game_info = {
                "game_id": current_game["id"],
                "home_team_abbr": current_game["homeTeam"]["abbrev"],
                "away_team_abbr": current_game["awayTeam"]["abbrev"]
            }
    print(f"Current Game: {current_game_info}" )
    print(f"Next Game State: {next_game_state}" )
    return prev_game_info, next_game_info, current_game_info


# Example usage
if __name__ == "__main__":
    team_abbr = "SJS"  # Example team abbreviation (San Jose Sharks)
    local_timezone = "America/Los_Angeles"  # Replace with your local timezone
    prev_game, next_game = get_prev_and_next_game_info(team_abbr, local_timezone)

    if prev_game:
        print("Previous Game:")
        print(f"Date: {prev_game['date']}")
        print(f"Opponent: {prev_game['opponent']}")
        print(f"Score: {prev_game['score']}")
        print(f"Result: {prev_game['result']}")
        print(f"prev_game: {prev_game}")
    else:
        print("No previous game found.")

    if next_game:
        print("\nNext Game:")
        print(f"Date: {next_game['date']}")
        print(f"Time: {next_game['time']}")  # Display the local time of the next game
        print(f"Opponent: {next_game['opponent']}")
        print(f"next_game: {next_game}")
    else:
        print("No next game found.")

def game_start_status(next_game):
    game_time = next_game['start_time_local'] 
    next_game_start_time_local = next_game['start_time_utc']
    next_game_countdown = next_game_start_time_local - datetime.now(pytz.utc)
    current_time = datetime.now(pytz.timezone("America/Los_Angeles"))
    seconds_until_next_game = next_game_countdown.total_seconds()
    
    if seconds_until_next_game < 1800:
        return "PRE"
    elif game_time <= current_time:
        return "LIVE"


def fetch_pregame_info():
    url = "https://api-web.nhle.com/v1/standings/now"
    print(f"Request URL: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        print("Requests Successful")
        return response.json()
    else: 
        print(f"Failed to fetch Standings/Pregame info")
    

def get_pregame_info(home_team_abbr, away_team_abbr):
    print(f"getting pregame infor for {home_team_abbr}, {away_team_abbr}")
    standings_data = fetch_pregame_info()
    
    if not standings_data:
        return None, None
    
    standings = standings_data.get("standings", [])

    home_team_standing = None
    away_team_standing = None
    
    for standing in standings:
        team_abbr = standing["teamAbbrev"]["default"]
        
        if team_abbr == home_team_abbr:
            home_team_standing = standing
        elif team_abbr == away_team_abbr:
            away_team_standing = standing
    
    home_pregame_info = None
    away_pregame_info = None
    
    if home_team_standing: 
        wins = home_team_standing["wins"]
        losses = home_team_standing["losses"]
        overtime_losses = home_team_standing["otLosses"]
        record = f"{wins} - {losses} - {overtime_losses}"
        
        div_place = home_team_standing["divisionSequence"]
        wild_card_place = home_team_standing["wildcardSequence"]
        
        if div_place <= 3:
            div_place = f"{div_place}*"
        
        if wild_card_place == 0:
            wild_card_place = ""
        elif wild_card_place <= 2:
            wild_card_place = f"{wild_card_place}*"
        
        home_pregame_info = {
            "name": home_team_standing["teamCommonName"]["default"],
            "abbr": home_team_standing["teamAbbrev"]["default"],
            "wins": home_team_standing["wins"],
            "losses": home_team_standing["losses"],
            "ot_losses": home_team_standing["otLosses"],
            "record": record,
            "l10_wins": home_team_standing["l10Wins"],
            "steak_code": home_team_standing["streakCode"],
            "streak_count": home_team_standing["streakCount"],
            "division_name": home_team_standing["divisionName"],
            "division_abbr": home_team_standing["divisionAbbrev"],
            "division_place": home_team_standing["divisionSequence"],
            "division_place_display": div_place,
            "league_place": home_team_standing["leagueSequence"],
            "wild_card_place": home_team_standing["wildcardSequence"],
            "wild_card_display": wild_card_place
        }
        
    if away_team_standing: 
        wins = away_team_standing["wins"]
        losses = away_team_standing["losses"]
        overtime_losses = away_team_standing["otLosses"]
        record = f"{wins} - {losses} - {overtime_losses}"
        
        div_place = away_team_standing["divisionSequence"]
        wild_card_place = away_team_standing["wildcardSequence"]
        
        if div_place <= 3:
            div_place = f"{div_place}*"
        
        if wild_card_place == 0:
            wild_card_place = ""
        elif wild_card_place <= 2:
            wild_card_place = f"{wild_card_place}*"
            
        away_pregame_info = {
            "name": away_team_standing["teamCommonName"]["default"],
            "abbr": away_team_standing["teamAbbrev"]["default"],
            "wins": away_team_standing["wins"],
            "losses": away_team_standing["losses"],
            "ot_losses": away_team_standing["otLosses"],
            "record": record,
            "l10_wins": away_team_standing["l10Wins"],
            "steak_code": away_team_standing["streakCode"],
            "streak_count": away_team_standing["streakCount"],
            "division_name": away_team_standing["divisionName"],
            "division_abbr": away_team_standing["divisionAbbrev"],
            "division_place": away_team_standing["divisionSequence"],
            "division_place_display": div_place,
            "league_place": away_team_standing["leagueSequence"],
            "wild_card_place": away_team_standing["wildcardSequence"],
            "wild_card_display": wild_card_place
        }
        
    return home_pregame_info, away_pregame_info
