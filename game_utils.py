import requests
from datetime import datetime, timedelta
import pytz
from pytz import timezone, UTC


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
    
    # Fetch NHL Schedule
    schedule_data = fetch_nhl_schedule(team_abbr)

    if not schedule_data:
        return None, None

    games = schedule_data.get("games", [])
    print(f"Number of Games Retrieved: {len(games)}")

    previous_game = None
    next_game = None

    # Loop through games to find the previous and next game
    for game in games:
        game_date = datetime.strptime(game["gameDate"], "%Y-%m-%d").date()  # Convert to `date` object
        if game_date < today:
            previous_game = game
        elif game_date >= today and next_game is None:
            next_game = game

    # Extract relevant information
    prev_game_info = None
    next_game_info = None

    if previous_game:
        prev_game_info = {
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
                "date": next_game_date_str,
                "time": next_game_time,
                "opponent": next_game["awayTeam"]["placeName"]["default"]
                if next_game["homeTeam"]["abbrev"] == team_abbr
                else next_game["homeTeam"]["placeName"]["default"],
                "matchup": f"{next_game['awayTeam']['placeName']['default']} @ {next_game['homeTeam']['placeName']['default']}",
            }



    return prev_game_info, next_game_info


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

from datetime import datetime

def game_is_live(next_game):
    # Extract date and time
    game_date = next_game['date']
    game_time = next_game['time']
    
    # If the date is 'Today', replace it with the current date
    if game_date == 'Today':
        game_date = datetime.now().strftime('%a, %b %d')  # Format the current date to match the expected format
    
    # Combine date and time for parsing
    game_datetime_str = f"{game_date} {game_time}"
    
    # Parse the datetime string into a datetime object
    try:
        game_time = datetime.strptime(game_datetime_str, "%a, %b %d %I:%M %p")
    except ValueError as e:
        print(f"Error parsing game time: {game_datetime_str} - {e}")
        return False  # Return False or handle the error as needed

    # Compare the game time to the current time to determine if the game is live
    current_time = datetime.now()
    #return game_time <= current_time
    return False

