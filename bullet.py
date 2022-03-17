import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """ Klasa przeznaczona do zarządzania pociskami wystrzeliwanymi przez statek. """
    
    def __init__(self, ai_game):
        """ Utworzenie obiektu pocisku w aktualnym położeniu statku. """
        super().__init__() 
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        
        # Utworzenie prostokąta pocisku w punkcie (0,0), a nastepnie zdefiniowanie dla niego polożenia. 
        self.image = pygame.image.load('images/firebolt.png')
        self.rect = self.image.get_rect()
        self.rect.midtop = ai_game.ship.rect.midtop
        
        # Położenie pocisku jest zdefiniowane za pomocą wartości zmiennoprzecinkowych
        self.y = float(self.rect.y)
        
        
    def update(self):
        """ Poruszanie pociskiem po ekranie."""
        # Uaktualnienie położenia pocisku
        self.y -= self.settings.bullet_speed
        # Uaktualnie położenia prostokąta pocisku.
        self.rect.y = self.y
        
    def draw_bullet(self):
        """ Wyświetlanie pocisku na ekranie."""
        self.screen.blit(self.image, self.rect)
    
