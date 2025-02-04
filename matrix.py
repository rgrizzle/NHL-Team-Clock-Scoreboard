import pygame
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from pygame.locals import QUIT

class MatrixDisplay:
    def __init__(self, width=32, height=32):
        # Initialize the RGB matrix
        self.options = RGBMatrixOptions()
        self.options.rows = height
        self.options.chain_length = 1  # Adjust for your setup
        self.options.parallel = 1
        self.options.hardware_mapping = 'adafruit-hat'  # Adjust hardware mapping if needed
        self.matrix = RGBMatrix(options=self.options)

        # Create a Pygame surface that matches the size of the matrix
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width, self.height))

    def blit_to_matrix(self, surface):
        """Converts a Pygame surface to the RGB matrix format and blits it."""
        # Blit the Pygame surface onto the matrix
        self.matrix.SetImage(pygame.image.tostring(surface, "RGB"))

    def clear(self):
        """Clear the matrix display."""
        self.surface.fill((0, 0, 0))  # Black to clear the display

    def update(self, surface):
        """Updates the matrix with the current Pygame surface."""
        self.blit_to_matrix(surface)

class GameScreen:
    def __init__(self):
        # Initialize your game screen logic here
        self.width = 32
        self.height = 32
        self.surface = pygame.Surface((self.width, self.height))
    
    def render(self):
        # Add your game rendering logic here
        self.surface.fill((255, 0, 0))  # Example: fill the screen with red
        return self.surface

class MainApp:
    def __init__(self):
        pygame.init()
        self.matrix_display = MatrixDisplay(width=32, height=32)  # Initialize matrix display
        self.game_screen = GameScreen()  # Initialize game screen

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            
            # Render the game screen
            surface = self.game_screen.render()
            
            # Update the matrix with the rendered surface
            self.matrix_display.update(surface)

            pygame.display.update()  # Optional, if you want to show on Pygame screen as well

        pygame.quit()

if __name__ == "__main__":
    app = MainApp()
    app.run()
