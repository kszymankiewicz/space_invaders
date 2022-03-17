class GameStats:
    
    def __init__(self, ai_game):
        """ Inicjalizacja danych statystycznych."""
        self.settings = ai_game.settings 
        self.reset_stats()
        # Uruchamianie gr w stanie nie aktywnym
        self.game_active = False
        
        self.high_score = 0
        
        
    def reset_stats(self):
        """ Inicjalzacja danych statystycznych, które mogą zmieniać się w trakcie gry. """
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1