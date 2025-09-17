import pygame
import time

class Game:
    def __init__(self):
        pygame.init()

        self.isRunning = True

        self.screen = pygame.display.set_mode((1000, 800))

    def handleLoop(self):
        while self.isRunning:
            # Handle Loop Events
            for event in pygame.event.get():
                pass
            
            # Draw
            self.screen.fill((255, 255, 255))

            pygame.display.flip()

            # Clock Ticker
            time.sleep(0.01)
        
        pygame.quit()
    
    def quit(self):
        self.isRunning = False