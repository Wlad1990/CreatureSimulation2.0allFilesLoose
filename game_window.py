import pygame
import pygame_gui

class GameWindow:
    def __init__(self):
        pygame.init()
        self.window_surface = pygame.display.set_mode((800, 600))
        self.manager = pygame_gui.UIManager((800, 600))

        self.api_key_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 275), (100, 50)), manager=self.manager)
        self.start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 350), (100, 50)), text='Start', manager=self.manager)

        self.clock = pygame.time.Clock()

    def update(self):
        is_running = True

        while is_running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                self.manager.process_events(event)

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.start_button:
                            api_key = self.api_key_input.get_text()
                            print(f"Start button pressed. API Key: {api_key}")
                            # Now you can use the API key to create creatures and start the game
                            # You would probably want to clear the screen and draw the game map and creatures here

            self.manager.update(time_delta)

            self.window_surface.fill((0, 0, 0))
            self.manager.draw_ui(self.window_surface)

            pygame.display.update()

        pygame.quit()