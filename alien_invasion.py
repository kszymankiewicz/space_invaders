import sys, pygame
import random

from time import sleep
from alien_bullet import Alien_Bullet

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from logo import Logo


class AlienInvasion:
    """Ogólna klasa przeznaczona do zarządzania zasobami i sposobem działania gry."""
    
    def __init__(self):
        """Inicjalizacja gry i utworzenie jej zasobów."""
        pygame.init()
        self.settings = Settings()
        
        #self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        self.screen= pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Inwazja obcych')
        
        # Utworzenie egzemplarza przechowującego dane statystyczne dotyczące gry. 
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.aliens_bullet = pygame.sprite.Group()
        
        self._create_fleet()
        
        # Utworzenie przycisku gra
        self.play_button = Button(self, self.settings.screen_width/2, (self.settings.screen_height/2), 'PLAY')
        self.exit_button = Button(self, self.settings.screen_width/2, (self.settings.screen_height/2 + 300), 'EXIT')
        self.info_button = Button(self, self.settings.screen_width/2,self.settings.screen_height/2 + 150, 'INFO')
        self.logo = Logo(self,self.settings.screen_width/2,self.settings.screen_height/2)
        
    def run_game(self): 
        """Rozpoczęcie pętli głównej gry."""
        while True:
            # Oczekiwanie na naciśnieęcie klawisza lub przycisku myszy
            self._check_events()
            
                
            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self.aliens_bullet.update()
                
                self._update_bullets()
                self._update_aliens()
               
                
            self._update_screen()
                      
    def _check_events(self):
        """Reakcja na zdarzenia generowane przez klawiature i mysz."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() 
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)        
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _random_fire_alien(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.settings.last_alien_shot > self.settings.alien_cooldwon:
            atacking_alien = random.choice(self.aliens)
            alien_bullet = Alien_Bullet(atacking_alien)
            self.aliens_bullet.add(alien_bullet)
            self.settings.last_alien_shot = time_now
        
    
    def _check_play_button(self, mouse_pos):
        """ Rozpoczecie nowej gry po kliknięciu orzycisku Play przez użytkownika. """
        
        start_button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        
        if start_button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)
            
            # Wyzerowanie danych statystycznych.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
        
        exit_button_clicket = self.exit_button.rect.collidepoint(mouse_pos)
        if exit_button_clicket and not self.stats.game_active:
            self.stats.game_active = False
            exit()
        
        info_button_clicket = self.info_button.rect.collidepoint(mouse_pos)
        if info_button_clicket and not self.stats.game_active:
            print('Info')
                
    def _check_keydown_events(self, event):
        # Reakcja na naciśniecie guzika 
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_ESCAPE:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            exit()
            
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = False
    
    def _fire_bullet(self):
        """ Utworzenie nowego pocisku i dodanie go do grupy pocisków. """
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _fire_alien_bullet(self):
        if len(self.aliens_bullet) < self.settings.bullet_allowed:
            atacking_alien = random.choice(self.aliens)
            new_alien_bullet = Alien_Bullet(atacking_alien)
            self.aliens_bullet.add(new_alien_bullet)
            
            time_now = pygame.time.get_ticks()
           
            self.settings.last_alien_shot = time_now
            
    def _update_bullets(self):
        """ Uaktualnienie położenia pocisków i usuniencie tych niewidocznych na ekranie."""
        # Uaktualnienie położenia pocisków 
        self.bullets.update()
        
        # Usunienicie pocisków, które znajdują się poza ekranem
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # Sprawdzanie, czy którykolwiek pocisk trafił obcego
        # Jeżeli tak, usuwamy pocisk i obcego
        self._check_bullet_alien_collisions()        
        
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        
        if not self.aliens:
            # Usunięcie istniających pocisków, przyspieszenie gry i utworzenie nowej floty.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            
            # Inkrementacja numeru poziomu
            self.stats.level += 1
            self.sb.prep_level()
    
    def _update_alien_bullets(self):
        """ Uaktualnienie położenia pocisków i usuniencie tych niewidocznych na ekranie."""
        # Uaktualnienie położenia pocisków 
        self.aliens_bullet.update()
        
        # Usunienicie pocisków, które znajdują się poza ekranem
        for bullet in self.aliens_bullet.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.aliens_bullet.remove(bullet)
        # Sprawdzanie, czy którykolwiek pocisk trafił obcego
        # Jeżeli tak, usuwamy pocisk i obcego
          
    
    def _update_aliens(self):
        """ Uaktualnienie położenia wszystkich obcych we flocie. """
        self._check_fleet_edges()
        self.aliens.update()
        
        # Wykrywanie kolizji między obcym a statkiem
        if pygame.sprite.spritecollideany(self.ship,self. aliens):
            self._ship_hit()
        # Wyszukiwanie obcych docierających do dolnej krawędzi.
        self._check_aliens_bottom()
        
      
    def _create_fleet(self):
        """ Utworzenie pełnej floty obcych."""
        # Utworzenie obcego i ustalenie liczby obcych, którzy zmieszą się w rzędzie.
        # Odległość między poszczególnymi obcymi jest równa szerokości obcego.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        
        # Ustalenie ile rzędów obcych zmieści się na ekranie.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        
        # Utorzenie pelnej floty.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
    
    def _create_alien(self, alien_number, row_number):        
        # Utworzenie obcego i umieszczenie go w rzędzie.
        alien = Alien(self)
        alien_width, alien_height= alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
    
    def _check_fleet_edges(self):
        """ Odpowiednia reakcja, gdy obcy dotrze do krawędzi ekranu. """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def  _change_fleet_direction(self):
        """ Przesunieńcie całej floty w dół i zmana kierunku, w którym się przemieszcza. """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1   
                              
    
    def _ship_hit(self):
        """ Reakcja na uderzenie obcego w statek. """
        if self.stats.ship_left > 0:
            # Zmniejszenie wartości przechowywanej w ships_left.
            self.stats.ship_left -= 1
            self.sb.prep_ships()
        
            # Usunięcie zawartości list aliens i bullets
            self.aliens.empty()
            self.bullets.empty()
        
            # Utworzenie nowej floty i wyśrodkowanie statku.
            self._create_fleet()
            self.ship.center_ship()
        
            # Pauza
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
    
    def _update_screen(self):
        """"Uaktualnienia obrazów na ekranie i przejście do nowego ekranu."""
        background = pygame.image.load('images/stars.bmp')
        background = pygame.transform.scale(background,(self.settings.screen_width,self.settings.screen_height))
         # Odświeżanie ekranu w trakcie każdej iteracji pętli
        self.screen.fill(self.settings.bg_color)
        # Umieszczanie obrazka jako tło
        self.screen.blit(background, (0, 0)) 
        self.ship.blitme()
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        
        for aliens_bullet in self.aliens_bullet.sprites():
            aliens_bullet.draw_alien_bullet()
        self.aliens_bullet.draw(self.screen)
        
        # Wyświetlanie informacji o punktacji
        self.sb.show_score()
        
        # Wyświetlanie przycisku tylko wtedy, gdy gra jest nie aktywna
        if not self.stats.game_active:
            self.logo.draw_logo()
            self.play_button.draw_button()
            self.exit_button.draw_button()
            self.info_button.draw_button()  
            
        # Wyświetlanie ostatnio zmodyfikowanego ekranu.
        pygame.display.flip() 
    
    def _check_aliens_bottom(self):
        """ Sprawdzanie, czy którykolwiek obcy dotarł do dolnej krawędzi ekranu. """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Tak samo jak w przypadku zderzenia statku z obcym
                self._ship_hit()
                break
        

if __name__ == '__main__':
    # Utworzenie egzemplarza gry i jej uruchomienie
    ai = AlienInvasion()
    ai.run_game()