import pygame
import requests
from datetime import datetime
from constants import *  # Import all constants
from base_screen import BaseScreen
import time
import sys
import time
from game_utils import get_pregame_info

class ScoreBoardScreen(BaseScreen):
    def __init__(self, manager):
        super().__init__(manager)
        self.load_resources()
        self.last_game_update = time.time()  # Track the last time the game data was updated
        self.team_abbr = TEAM_ABBR
        self.local_tz = LOCAL_TIMEZONE
        self.current_game = None  
        self.polling_interval = 5  # Poll every x seconds
        
        self.home_team_abbr = 'XXX'
        self.away_team_abbr = 'XXX'
        
        self.fade_alpha = 0
        self.fade_direction = 2.5 #speed of fading
        
        self.loading_text = "Loading"
        self.loading_dots = ""
        self.loading_counter = 0
        self.loading_interval = 50  # Controls speed of dot animation
        
        self.pregame_info_fetched = False
        

    def update(self, current_game):
        if current_game:
            # Process the current game data as needed
            self.current_game = current_game
            game_id = current_game['game_id']
            self.home_team_abbr = current_game["home_team_abbr"]
            self.away_team_abbr = current_game["away_team_abbr"]
            
            # Load logos only when we have valid team abbreviations
            self.home_logo_path = get_logo(self.home_team_abbr)
            self.home_logo = pygame.image.load(self.home_logo_path)
            width, height = self.home_logo.get_size()
            self.home_logo = pygame.transform.scale(self.home_logo, (int(width * 0.5), int(height * 0.5)))
            
            self.away_logo_path = get_logo(self.away_team_abbr)
            self.away_logo = pygame.image.load(self.away_logo_path)
            width, height = self.away_logo.get_size()
            self.away_logo = pygame.transform.scale(self.away_logo, (int(width * 0.5), int(height * 0.5)))

            if not self.pregame_info_fetched:
                get_pregame_info(self.home_team_abbr, self.away_team_abbr)
                self.pregame_info_fetched = True
            
            # Poll for game info periodically
            self.poll_game_info(game_id)

        self.draw()  

    def load_resources(self):
        # Load fonts using constants
        self.time_font = pygame.font.Font("broken_console.ttf", TIME_FONT_SIZE)
        self.date_font = pygame.font.Font("broken_console.ttf", DATE_FONT_SIZE)
        self.game_font = pygame.font.Font("broken_console.ttf", GAME_FONT_SIZE)
        self.weather_font = pygame.font.Font("broken_console.ttf", WEATHER_FONT_SIZE)
        self.score_font = pygame.font.Font("broken_console.ttf", TIME_FONT_SIZE)
        self.loading_font = pygame.font.Font("broken_console.ttf", 60)


    def poll_game_info(self, game_id):
        # Check if the polling interval has passed
        current_time = time.time()
        if current_time - self.last_game_update >= self.polling_interval:
            # Call the API to get game info
            game_info = get_game_info(game_id)
            self.draw()

            if game_info:
                self.current_game.update(game_info)  # Update current game with new data
                print("Game Info Updated")
            else:
                print("Failed to update game info")
            
            self.last_game_update = current_time  # Reset the last update time

    def draw(self):
        super().draw()  # Clears screen with background color
        screen = self.manager.screen  

        # Fill the screen with the background color
        screen.fill(BACKGROUND_COLOR)

        # Get screen dimensions
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Ensure game info is valid before using it
        game_info_updated = False
        if self.current_game:
            game_info_updated = self.current_game.get("game_info_updated", False)

        # Display Loading Screen if Data is not ready
        if not game_info_updated:
            self.loading_counter += 1
            if self.loading_counter % self.loading_interval == 0:
                dots = "." * ((self.loading_counter // self.loading_interval) % 4)  # Cycles '', '.', '..', '...'
                self.loading_dots = dots

            loading_surface = self.loading_font.render(self.loading_text + self.loading_dots, True, TEXT_COLOR)
            loading_rect = loading_surface.get_rect(center=(screen_width // 2, screen_height // 2 ))
            screen.blit(loading_surface, loading_rect)
            pygame.display.flip()
            return  # Stop drawing if game data is not available

        # Get current time and date
        current_time = datetime.now().strftime("%I:%M").lstrip('0').replace(" 0", " ") 
        current_date = datetime.now().strftime("%A, %B %d")
        

        # Set Game Info (assuming current_game has been updated with live game data)
        in_intermission = self.current_game.get("in_intermission", False) if self.current_game else False
        #print(self.current_game)
        period = self.current_game.get("period", "x")
        clock_running = self.current_game.get("clock_running", False) if self.current_game else False
        game_state = self.current_game.get("game_state", False) if self.current_game else False
        game_info_updated = self.current_game.get("game_info_updated", False) if self.current_game else False
        
        if in_intermission == True: 
            period_desc = "INTERMISSION"
        else:
            period_desc = "PERIOD"
            
        time_remaining = self.current_game.get("time_remaining", "xx:xx").lstrip("0")
        home_score = self.current_game.get("home_team_score", 0)
        home_sog = self.current_game.get("home_team_sog", 0)
        #print(f"home_sog: {home_sog}")
        away_score = self.current_game.get("away_team_score", 0)
        away_sog = self.current_game.get("away_team_sog", 0)
        #print(f"away_sog: {away_sog}")
        
        

        # Render Surfaces
        period_surface = self.game_font.render(f"{period_desc} {period}", True, TEXT_COLOR)
        time_remaining_surface = self.game_font.render(time_remaining, True, TEXT_COLOR)
        
        
        home_score_surface = self.score_font.render(str(home_score), True, TEXT_COLOR)
        home_sog_surface = self.game_font.render(f"SOG {str(home_sog)}", True, TEXT_COLOR)
        
        away_score_surface = self.score_font.render(str(away_score), True, TEXT_COLOR)
        away_sog_surface = self.game_font.render(f"SOG {str(away_sog)}", True, TEXT_COLOR)
        
        home_record_surface = self.game_font.render(f"", True, TEXT_COLOR)

        # Positioning Game Information
        period_rect = period_surface.get_rect(center=((screen_width // 2 ), screen_height // 2 - 150 ))
        time_remaining_rect = time_remaining_surface.get_rect(center=((screen_width // 2 ), screen_height // 2 - 120 ))
        clock_running_pos = (screen_width // 2 + 50, screen_height // 2 - 150)
        clock_running_radius = 10  # Adjust size as needed
        
        # Update fade effect
        self.fade_alpha += self.fade_direction
        if self.fade_alpha >= 255 or self.fade_alpha <= 0:
            self.fade_direction *= -1  # Reverse fading direction

        # Create a surface for the circle with an alpha channel
        clock_running_circle_surface = pygame.Surface((20, 20), pygame.SRCALPHA)  # Adjust size as needed
        clock_running_circle_surface.set_alpha(self.fade_alpha)  # Apply transparency
        pygame.draw.circle(clock_running_circle_surface, GREEN, (10, 10), 10)  # Draw circle in the center of surface
        
        clock_not_running_circle_surface = pygame.Surface((20, 20), pygame.SRCALPHA)  # Adjust size as needed
        pygame.draw.circle(clock_not_running_circle_surface, RED, (10, 10), 10)
        
        home_logo_rect =self.home_logo.get_rect(center=((screen_width // 2 + 400 ), screen_height // 2 ))
        away_logo_rect =self.away_logo.get_rect(center=((screen_width // 2 - 400 ), screen_height // 2 ))
        
        home_score_rect = home_score_surface.get_rect(center=((screen_width // 2 + 150 ), screen_height // 2 ))
        home_sog_rect = home_sog_surface.get_rect(center=((screen_width // 2 + 150 ), screen_height // 2 + 150))
        
        away_score_rect = away_score_surface.get_rect(center=((screen_width // 2 - 150 ), screen_height // 2 ))
        away_sog_rect = away_sog_surface.get_rect(center=((screen_width // 2 - 150 ), screen_height // 2 + 150))

        # Blit (draw) everything onto the screen
        screen.blit(self.home_logo, home_logo_rect)
        screen.blit(self.away_logo, away_logo_rect)
        #if game_state == "PRE":
            
        
        if game_state == "LIVE" or game_state == "CRIT":
            screen.blit(period_surface, period_rect)
            screen.blit(time_remaining_surface, time_remaining_rect)
            
            screen.blit(home_score_surface, home_score_rect)
            screen.blit(away_score_surface, away_score_rect)
            
            screen.blit(home_sog_surface, home_sog_rect)
            screen.blit(away_sog_surface, away_sog_rect)
        
            if in_intermission == False: 
                if clock_running:
                    #pygame.draw.circle(screen, RED, clock_running_pos, clock_running_radius)
                    screen.blit(clock_running_circle_surface, (screen_width // 2 + 50, screen_height // 2 - 133))
                else:
                    screen.blit(clock_not_running_circle_surface, (screen_width // 2 + 50, screen_height // 2 - 133))
            
        
        # Update the Display
        pygame.display.flip()

def get_game_info(game_id):
    url = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/play-by-play"
    print(f"Request URL: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        print("Request Successful")
    else:
        print(f"Failed to fetch schedule for {game_id}")
        return None

    game_info = None
    if response:
        home_team = response.json().get("homeTeam", {})
        away_team = response.json().get("awayTeam", {}
                                        )
        game_info = {
            "game_info_updated":  True,
            "game_state": response.json()["gameState"],
            "period": response.json()["displayPeriod"],
            "time_remaining": response.json()["clock"]["timeRemaining"],
            "in_intermission": response.json()["clock"]["inIntermission"],
            "clock_running": response.json()["clock"]["running"],
            "home_team": response.json()["homeTeam"]["commonName"]["default"],
            "home_team_place": response.json()["homeTeam"]["placeName"],
            "home_team_abbr": response.json()["homeTeam"]["abbrev"],
            "home_team_score": response.json()["homeTeam"]["score"],
            "home_team_sog": home_team.get("sog", 0),
            "away_team": response.json()["awayTeam"]["commonName"]["default"],
            "away_team_place": response.json()["awayTeam"]["placeName"],
            "away_team_abbr": response.json()["awayTeam"]["abbrev"],
            "away_team_score": response.json()["awayTeam"]["score"],
            "away_team_sog": away_team.get("sog", 0)
        }
        
        print(game_info)
    return game_info

def get_logo(team_abbr):
    if team_abbr == 'XXX':  # Default case for uninitialized values
        return "team_logos/SJS_logo.png"
    elif team_abbr == 'SJS':
        return "team_logos/SJS_logo.png"
    else:
        return f"team_logos/{team_abbr}_logo.svg"
    
#def get_pregame_info(home_team_abbr, away_team_abbr):
