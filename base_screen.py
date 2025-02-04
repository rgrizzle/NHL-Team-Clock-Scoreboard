class BaseScreen:
    def __init__(self, manager):
        self.manager = manager
        self.screen = manager.screen
        self.background_color = manager.background_color
        
    def handle_event(self, event):
        pass
        
    def update(self, current_game=None):  # Accept optional argument
        pass
        
    def draw(self):
        self.screen.fill(self.background_color)
