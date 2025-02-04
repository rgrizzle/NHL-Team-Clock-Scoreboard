import os
import requests

def get_team_abbrs():
    team_list_url = "https://api.nhle.com/stats/rest/en/team"
    print(f"Team List Request URL: {team_list_url}")
    team_list_response = requests.get(team_list_url)
    if team_list_response.status_code == 200:
        print(f"Team List Request Successful")
        team_list_json = team_list_response.json()
    else: 
        print(f"Failed to fetch team list")
        return None
    
    teams = team_list_json.get("data", [])
    print(f"Number of Teams Retrieved: {len(teams)}")
    
    team_abbrs = set()
    
    for team in teams:
        team_abbrs.add(team["triCode"])
    
    print((f"Team Names in Set: {len(team_abbrs)}"))
    
    return team_abbrs
 
def get_team_logos():
    team_abbrs = get_team_abbrs()
    
    if not team_abbrs:
        print(f"Failed to Retrieve Team Abbrs")
        return
    
    logos_dir = "team_logos"
    if not os.path.exists(logos_dir):
        os.makedirs(logos_dir)
    
    for abbr in team_abbrs:
        url = f"https://assets.nhle.com/logos/nhl/svg/{abbr}_light.svg"
        print(f"Request URL: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Request Successful for {abbr}")
            
            file_path = os.path.join(logos_dir, f"{abbr}_logo.svg")
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"Logo for {abbr} saved as {file_path}")
        else: 
            print(f"Failed to fetch logo for {abbr}")

get_team_logos()

