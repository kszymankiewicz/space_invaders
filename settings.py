import pygame

class Settings:
    
    def __init__(self):
        """Inicjalizacja ustawień gry."""
       
        # Ustawienia ekranu.
        self.screen_width = 1500
        self.screen_height = 700
        self.background = pygame.image.load('images/stars.bmp')
        self.background = pygame.transform.scale(self.background,(self.screen_width, self.screen_height))
        self.bg_color = (230, 230, 230)
        
        # Ustawienia statku.
        self.ship_limit = 3
        
        # Ustawienia dotyczące pocisku.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 0, 0)
        self.bullet_allowed = 3
    
        # Ustawienia dotyczące obcego.
        self.fleet_drop_speed = 10
        
        # Łatwa zmiana szybkości gry.
        self.speedup_scale = 1.5
        
        # Łatwa zmiana libczy pkt przyznawanych za strzelanie obcego
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()
        
        # Punktacja
        self.alien_points = 50
        # Fire alien cooldwon in miliesecond
        self.alien_cooldwon = 1000
        self.last_alien_shot = pygame.time.get_ticks()
        
    def initialize_dynamic_settings(self):
        """ Inicjalizacja ustawień, które ulegają zmianie w trakcie gry. """
        self.ship_speed = 8.0
        self.bullet_speed = 10.0
        self.alien_speed = 2.0
            
        # Wartość fleet_directions w prawo wynosi 1 natomiast w lewo -1. 
        self.fleet_direction = 1 
        
    def increase_speed(self):
        """ Zmiana ustawień dotyczących szybkości. """
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)