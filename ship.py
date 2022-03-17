import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    
    def __init__(self, ai_game):
        """Inicjalizacja statku kosmicznego i jego położenie poczatkowe"""
        super().__init__()
        
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        
        # Wczytanie obrazu statku kosmicznego i pobranie jego prostokąta
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        
        # Każdy nowy statek pojawia się na dole ekranu 
        self.rect.midbottom = self.screen_rect.midbottom
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        # Opcje wskazujące na poruszanie się statku.
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        
    def update(self):
        """ Uaktualnienie położenia statku na podstawie opcji wskazującej na jego ruch"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed 
        if self.moving_up and self.rect.top > 200:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed     
            
        self.rect.x = self.x
        self.rect.y = self.y   
            
        
    def blitme(self):
        """ Wyświetlanie statku kosmiczengo w jego aktualnym położeniu"""
        self.screen.blit(self.image, self.rect)
        
    def center_ship(self):
        """ Umieszczenie statku na środku przy dolnej krawędzi ekranu. """
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)