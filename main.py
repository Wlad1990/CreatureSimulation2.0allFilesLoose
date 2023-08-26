import pygame
import pygame.font
from ui.game_init import start_game
from world.world import World

load_resources_from_csv('path_to_your_resources.csv')

# Initialize pygame
pygame.init()

# Constants
WIDTH = 1000
HEIGHT = 1000
BACKGROUND_COLOR = (50, 50, 50)
SLIDER_BG_COLOR = (150, 150, 150)
BUTTON_COLOR = (100, 100, 255)
TEXT_COLOR = (255, 255, 255)
FONT = pygame.font.SysFont('Arial', 25)

class Slider:
    def __init__(self, x, y, width, max_value, label):
        self.x = x
        self.y = y
        self.width = width
        self.max_value = max_value
        self.current_value = 0
        self.label = label
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + 20:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x, _ = pygame.mouse.get_pos()
            self.current_value = (mouse_x - self.x) / self.width * self.max_value

    def draw(self, screen):
        # Draw the slider background
        pygame.draw.rect(screen, SLIDER_BG_COLOR, (self.x, self.y, self.width, 20))
        # Draw the active slider value
        pygame.draw.rect(screen, BUTTON_COLOR, (self.x, self.y, self.current_value / self.max_value * self.width, 20))
        text = FONT.render(f'{self.label}: {int(self.current_value)}', True, TEXT_COLOR)
        screen.blit(text, (self.x - 250, self.y - 30))  # Adjusted text position

# Start Menu
def start_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Start Menu')
    
    creature_slider = Slider(500, 370, 400, 10000, 'Number of Creatures')
    map_size_slider = Slider(500, 470, 400, 300, 'Map Size (km x km)')
    resources_slider = Slider(500, 570, 400, 5000, 'Number of Resources')
    wildlife_slider = Slider(500, 670, 400, 2000, 'Number of Wildlife')
    tribe_count_slider = Slider(500, 770, 400, 20, 'Number of Tribes')
    tribe_size_slider = Slider(500, 870, 400, 500, 'Average Tribe Size')
    
    sliders = [creature_slider, map_size_slider, resources_slider, wildlife_slider, tribe_count_slider, tribe_size_slider]

    # Welt-Instanz erstellen
    world = World()

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        
        # Draw the world preview
        world_surface = pygame.Surface((WIDTH, HEIGHT))
        world.draw(world_surface)
        screen.blit(pygame.transform.scale(world_surface, (500, 500)), (50, 50))
    
    # Button zum Neugenerieren der Welt
    regenerate_button_rect = pygame.Rect(WIDTH // 2 - 300, HEIGHT - 100, 200, 40)
    
    # Radio buttons for generation type
    generation_type = "creatures"
    button_creatures_rect = pygame.Rect(250, 270, 20, 20)
    button_tribes_rect = pygame.Rect(550, 270, 20, 20)
    
    # Start button
    start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 40)  # Adjusted position
    
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        
        # Weltvorschau
        world_surface = pygame.Surface((WIDTH, HEIGHT))
        world.draw(world_surface)  # Zeichnet die Welt auf der Oberfläche
        screen.blit(pygame.transform.scale(world_surface, (500, 500)), (50, 50))  # Verkleinerte Vorschau
        
        # Button zum Neugenerieren der Welt
        pygame.draw.rect(screen, BUTTON_COLOR, regenerate_button_rect)
        screen.blit(FONT.render('Regenerate', True, TEXT_COLOR), (WIDTH // 2 - 280, HEIGHT - 95))
        
        # Display radio buttons and labels
        pygame.draw.circle(screen, BACKGROUND_COLOR, button_creatures_rect.center, 10)
        pygame.draw.circle(screen, BACKGROUND_COLOR, button_tribes_rect.center, 10)
        if generation_type == "creatures":
            pygame.draw.circle(screen, BUTTON_COLOR, button_creatures_rect.center, 7)
        else:
            pygame.draw.circle(screen, BUTTON_COLOR, button_tribes_rect.center, 7)
        screen.blit(FONT.render('Generate individual creatures', True, TEXT_COLOR), (280, 260))
        screen.blit(FONT.render('Generate tribes', True, TEXT_COLOR), (580, 260))
        
        # Display start button
        pygame.draw.rect(screen, BUTTON_COLOR, start_button_rect)
        screen.blit(FONT.render('Start', True, TEXT_COLOR), (WIDTH // 2 - 40, HEIGHT - 95))
        
        # Sliders
        for slider in sliders:
            if slider == tribe_count_slider or slider == tribe_size_slider:
                if generation_type == "tribes":
                    slider.draw(screen)
            else:
                slider.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            for slider in sliders:
                slider.handle_event(event)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            for slider in sliders:
                slider.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Regenerate world preview on button click
                if regenerate_button_rect.collidepoint(mouse_x, mouse_y):
                    world = World() # Recreate world instance
                # Überprüft, ob der "Regenerate"-Button geklickt wurde
                if regenerate_button_rect.collidepoint(mouse_x, mouse_y):
                    world = World()  # Erstellt eine neue Welt-Instanz
                elif button_creatures_rect.collidepoint(mouse_x, mouse_y):
                    generation_type = "creatures"
                elif button_tribes_rect.collidepoint(mouse_x, mouse_y):
                    generation_type = "tribes"
                elif start_button_rect.collidepoint(mouse_x, mouse_y):
                    # Return user-selected settings when Start button is pressed
                    settings = {
                        "number_of_creatures": creature_slider.current_value,
                        "map_size": map_size_slider.current_value,
                        "number_of_resources": resources_slider.current_value,
                        "number_of_wildlife": wildlife_slider.current_value,
                        "number_of_tribes": tribe_count_slider.current_value if generation_type == "tribes" else 0,
                        "average_tribe_size": tribe_size_slider.current_value if generation_type == "tribes" else 0,
                        "generation_type": generation_type
                    }
                    return settings
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    user_settings = start_menu()
    start_game(user_settings)