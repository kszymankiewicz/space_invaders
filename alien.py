import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    
    def __init__(self, ai_game):
        """ Klasa przedstawiająca pojedyńczego obcego we flocie. """
        # Inicjacja obcego i umieszczenie go w położeniu początkowym.
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # Wczytywanie obrazu obcego i zdefiniowanie jego atrybutu rect.
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()
        
        # Umieszczanie nowego obcego w pobliżu lewego górnego rogu ekranu.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # Przechowywanie dokładnego poziomego położenia obcego
        self.x = float(self.rect.x)
        
    def check_edges(self):
        """ Zwraca wartość True, jeśli obcy znajduje się przy krawędzi ekranu. """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
    
    def update(self):
        """ Przesunieńcie obcego w prawo. """
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x