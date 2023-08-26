import pygame
from world.world import World
from creatures.creature import Creature
from resources.resources import Resource

class Game:
    def __init__(self, settings):
        """
        Initialisiert das Spiel basierend auf den Einstellungen aus dem Startmenü.
        """
        pygame.init()
        
        self.settings = settings
        self.size = settings.get("map_size", 100)
        self.num_resources = settings.get("number_of_resources", 100)
        self.num_creatures = settings.get("number_of_creatures", 10)
        
        self.width, self.height = 1000, 1000
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        pygame.display.set_caption('Creature Simulation')
        
        self.world = World(size=self.size, num_resources=self.num_resources, num_creatures=self.num_creatures)

    def run(self):
        """
        Hauptspiel-Schleife.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.world.update()
            
            self.screen.fill((255, 255, 255))
            self.world.draw(self.screen)
            
            pygame.display.flip()
        
        pygame.quit()

# Diese Funktion kann von main.py aufgerufen werden, um das Spiel zu starten.
def start_game(settings):
    game = Game(settings)
    game.run()