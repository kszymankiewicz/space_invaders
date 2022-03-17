import pygame
from pygame.sprite import Sprite


class Alien_Bullet(Sprite):
    """ Klasa przeznaczona do zarządzania pociskami wystrzeliwanymi przez alienów. """
    def __init__(self, ai_game):
        super().__init__()
        
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        self.alien = ai_game.alien
        
        # Utworzenie prostokąta pocisku w punkcie (0,0), a nastepnie zdefiniowanie dla niego polożenia. 
        self.image = pygame.image.load('images/fire.png')
        self.rect = self.image.get_rect()
        self.rect.midbottom = ai_game.alien.rect.midbottom
        
        
        # Położenie pocisku jest zdefiniowane za pomocą wartości zmiennoprzecinkowych
        self.y = float(self.rect.y)
        
    def update(self):
        """ Poruszanie pociskiem po ekranie."""
        # Uaktualnienie położenia pocisku
        self.y += self.settings.bullet_speed
        # Uaktualnie położenia prostokąta pocisku.
        self.rect.y = self.y
    
    def draw_alien_bullet(self):
        """ Wyświetlanie pocisku na ekranie."""
        self.screen.blit(self.image, self.rect)