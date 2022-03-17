import pygame.font
import pygame


class Button():
    
    def __init__(self, ai_game, x, y, msg):
        """ Inizcjalizacja atrybutów przycisk. """
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        image_button = pygame.image.load('images/button.png').convert_alpha()
        image_button2 = pygame.image.load('images/button2.png').convert_alpha()
        # Zdefiniowanie wymiarów i właściwości przycisku
        self.image = image_button
        self.image2 =  image_button2
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
        #self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        
        # Utworzenie prostokąta przycisku i wyśrodkowanie go.
        #self.rect = pygame.Rect(0, 0, self.width, self.height)
        #self.rect.center = self.screen_rect.center
        
        # Komunikat wyświetlany przez przycisk trzeba przygotować jednokrotnie
        self._prep_msg(msg)
        
    def _prep_msg(self, msg):
        """ Umeszczanie komunikatu w wygenerowanym obrazie i wyśrodkowanie tekstu na przycisku. """
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button(self):
        # Wyświetlanie pustego przycisku, a następnie komunikatu na nim.
        self.screen.blit(self.image, (self.rect.x, self.rect.y ))
        self.screen.blit(self.msg_image, self.msg_image_rect)
    
    def draw_button2(self):
        # Wyświetlanie pustego przycisku, a następnie komunikatu na nim.
        self.button_color = self.draw_button2