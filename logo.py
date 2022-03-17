import pygame

from settings import Settings

class Logo:
    
    def __init__(self, ai_game, x, y):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        
        image_logo = pygame.image.load('images/logo.bmp').convert_alpha()
        image_logo = pygame.transform.scale(image_logo,(self.settings.screen_width,self.settings.screen_height))
        
        # Zdefiniowanie wymiarów i właściwości przycisku
        self.image = image_logo
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
        
    def draw_logo(self):
        # Wyświetlanie ekranu początkowego, a następnie komunikatu na nim.
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
           