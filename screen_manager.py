import pygame
from clock_screen import ClockScreen
from datetime import datetime, timezone
from scoreboard_screen import ScoreBoardScreen
from game_utils import game_start_status
from constants import *

class ScreenManager:
    def __init__(self):
        from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR
        
        # Initialize display using constants
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        window_caption = f"{TEAM_ABBR} Clock/Scoreboard"
        pygame.display.set_caption(window_caption)
        self.background_color = BACKGROUND_COLOR
        self.current_screen = None
        self.screens = {
            'clock': ClockScreen(self),
            'scoreboard': ScoreBoardScreen(self)
        }
        
    def switch_to(self, screen_name):
        self.current_screen = self.screens[screen_name]
    
    def update(self):
        self.check_screen_transitions()
        if self.current_screen:
            # Fetch current game from ClockScreen
            current_game = self.screens['clock'].current_game  
            self.current_screen.update(current_game)

    def check_screen_transitions(self):
        next_game = self.screens['clock'].next_game
        current_game = self.screens['clock'].current_game
        #print(next_game)
        next_game_start_time = next_game['start_time_local']
        next_game_countdown = next_game_start_time - datetime.now(timezone.utc)
        seconds_until_next_game = next_game_countdown.total_seconds()
        
        if current_game:
            self.switch_to('scoreboard')
        elif next_game and game_start_status(next_game) == "PRE":
            self.switch_to('scoreboard')
        elif next_game and game_start_status(next_game) == "LIVE":
            self.switch_to('scoreboard')
        else:
            self.switch_to('clock')
