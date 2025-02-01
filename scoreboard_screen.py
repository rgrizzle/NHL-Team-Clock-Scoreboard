import pygame
from datetime import datetime
from constants import *  # Import all constants
from game_utils import get_prev_and_next_game_info
from weather_utils import get_weather  
from base_screen import BaseScreen


class ScoreBoardScreen(BaseScreen):
    def __init__(self, manager):
        super().__init__(manager)
        self.last_weather_update = datetime.now()
        self.last_game_update = datetime.now()
        self.weather_text = "Loading..."
        self.prev_game = None
        self.next_game = None
        self.team_abbr = "SJS"
        self.local_tz = "America/Los_Angeles"


