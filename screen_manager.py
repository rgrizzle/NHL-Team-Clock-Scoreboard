import pygame
from clock_screen import ClockScreen
from scoreboard_screen import ScoreBoardScreen
from game_utils import game_is_live
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
            self.current_screen.update()
            

    def check_screen_transitions(self):
        next_game = self.screens['clock'].next_game
        if next_game and game_is_live(next_game):
            self.switch_to('scoreboard')
        else:
            self.switch_to('clock')
