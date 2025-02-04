import pygame
import sys
from screen_manager import ScreenManager

class NHLClockApp:
    def __init__(self):
        pygame.init()
        self.manager = ScreenManager()
        self.running = True
        self.clock = pygame.time.Clock()

    def run(self):
        self.manager.switch_to('clock')
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.manager.current_screen:
                    self.manager.current_screen.handle_event(event)

            self.manager.update()
            
            if self.manager.current_screen:
                self.manager.current_screen.draw()
                pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()
        sys.exit()