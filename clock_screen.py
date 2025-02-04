import pygame
import requests
from datetime import datetime, timezone
from constants import *  
from game_utils import get_prev_and_next_game_info
from weather_utils import get_weather  
from base_screen import BaseScreen
import os



class ClockScreen(BaseScreen):
    def __init__(self, manager):
        super().__init__(manager)
        self.load_resources()
        self.last_weather_update = datetime.now()
        self.last_game_update = datetime.now()
        self.weather_text = "Loading..."
        self.team_abbr = TEAM_ABBR
        self.local_tz = LOCAL_TIMEZONE
        self.prev_game, self.next_game, self.current_game = get_prev_and_next_game_info(TEAM_ABBR, LOCAL_TIMEZONE)

    def load_resources(self):
        # Load fonts using constants
        self.time_font = pygame.font.Font("broken_console.ttf", TIME_FONT_SIZE)
        self.date_font = pygame.font.Font("broken_console.ttf", DATE_FONT_SIZE)
        self.game_font = pygame.font.Font("broken_console.ttf", GAME_FONT_SIZE)
        self.weather_font = pygame.font.Font("broken_console.ttf", WEATHER_FONT_SIZE) 
        
        # Load and scale logo
        if TEAM_ABBR == 'SJS':
            team_logo_path = os.path.join("team_logos", "SJS_logo.png") 
        else:
            team_logo_path = os.path.join("team_logos", f"{TEAM_ABBR}_logo.svg")
        self.team_logo = pygame.image.load(team_logo_path)
        
        if TEAM_ABBR == 'SJS':
            self.team_logo = pygame.transform.scale(self.team_logo, (290, 290))
        else:
            #self.team_logo = pygame.transform.scale_by(self.team_logo, .5)
            width, height = self.team_logo.get_size()
            self.team_logo = pygame.transform.scale(self.team_logo, (int(width * 0.5), int(height * 0.5)))

        
        

    def draw(self):
        super().draw()  # Clears screen with background color
        screen = self.manager.screen  

        # Fill the screen with the background color
        screen.fill(BACKGROUND_COLOR)

        # Get screen dimensions
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Get current time and date
        current_time = datetime.now().strftime("%I:%M").lstrip('0').replace(" 0", " ") 
        current_date = datetime.now().strftime("%A, %B %d")
        
        # Use weather data
        weather_text = self.weather_text

        # Render Clock Surfaces
        time_surface = self.time_font.render(current_time, True, TEXT_COLOR)
        date_surface = self.date_font.render(current_date, True, TEXT_COLOR)
        weather_surface = self.weather_font.render(weather_text, True, TEXT_COLOR)

        # Set Prev Game Data
        prev_game_result = str(self.prev_game['result'])
        prev_game_last_period_type = str(self.prev_game['last_period_type'])
        prev_game_result_text = f"{prev_game_result} {prev_game_last_period_type}"
        if prev_game_result == 'WIN':
            result_color = GREEN
        else:
            result_color = RED
        prev_game_home_score = str(self.prev_game['home_score'])
        prev_game_away_score = str(self.prev_game['away_score'])

        # Set Next Game Data
        next_game_date = self.next_game['date']
        next_game_time = self.next_game['time']
        next_game_opponent = self.next_game['opponent']
        next_game_start_time_local = self.next_game['start_time_utc']
        next_game_countdown = next_game_start_time_local - datetime.now(timezone.utc)
        # Convert countdown to HH:MM:SS format
        hours, remainder = divmod(int(next_game_countdown.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_countdown = f"{hours:02}:{minutes:02}:{seconds:02}"
        seconds_until_next_game = next_game_countdown.total_seconds()
        if seconds_until_next_game < 1800:
            self.current_game = self.next_game

        # Render the game information
        result_surface = self.game_font.render(prev_game_result_text, True, result_color)
        prev_game_home_score_surface = self.game_font.render(prev_game_home_score, True, TEXT_COLOR)
        prev_game_away_score_surface = self.game_font.render(prev_game_away_score, True, TEXT_COLOR)
        next_game_date_surface = self.game_font.render(next_game_date, True, TEXT_COLOR)
        next_game_time_surface = self.game_font.render(next_game_time, True, TEXT_COLOR)
        next_game_opponent_surface = self.game_font.render(next_game_opponent, True, TEXT_COLOR)
        next_game_countdown_surface = self.game_font.render(str(seconds_until_next_game), True, TEXT_COLOR)

        # Centering calculations
        time_rect = time_surface.get_rect(center=(screen_width // 2, screen_height // 4 + 50))
        date_rect = date_surface.get_rect(center=(screen_width // 2, screen_height // 4 + 50))
        weather_rect = weather_surface.get_rect(center=(screen_width // 2, screen_height // 4 + 100))
        logo_rect = self.team_logo.get_rect(center=(screen_width // 2, screen_height // 2 + 115))
        
        # Positioning the game information
        result_rect = result_surface.get_rect(center=(screen_width // 6 , screen_height // 2 + 80))
        prev_game_home_score_rect = prev_game_home_score_surface.get_rect(center=(screen_width // 6, screen_height // 2 + 115))
        prev_game_away_score_rect = prev_game_away_score_surface.get_rect(center=(screen_width // 6, screen_height // 2 + 150))
        next_game_date_rect = next_game_date_surface.get_rect(center=((screen_width // 2 + 260), screen_height // 2 + 80))
        next_game_time_rect = next_game_time_surface.get_rect(center=((screen_width // 2 + 260), screen_height // 2 + 115))
        next_game_opponent_rect = next_game_opponent_surface.get_rect(center=((screen_width // 2 + 260), screen_height // 2 + 150))
        next_game_countdown_rect = next_game_countdown_surface.get_rect(center=((screen_width // 2 + 260), screen_height // 2 + 40))

        # Blit (draw) everything onto the screen
        screen.blit(time_surface, time_rect)
        #screen.blit(date_surface, date_rect)
        #screen.blit(weather_surface, weather_rect)
        screen.blit(self.team_logo, logo_rect)
        screen.blit(result_surface, result_rect)
        screen.blit(prev_game_home_score_surface, prev_game_home_score_rect)
        screen.blit(prev_game_away_score_surface, prev_game_away_score_rect)
        screen.blit(next_game_date_surface, next_game_date_rect)
        screen.blit(next_game_time_surface, next_game_time_rect)
        screen.blit(next_game_opponent_surface, next_game_opponent_rect)
        #screen.blit(next_game_countdown_surface, next_game_countdown_rect)
        

        # Update the display
        pygame.display.flip()
