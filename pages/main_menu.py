import pygame

class MainMenuPage(object):
    def __init__(self, screen_size, font):
        self.surface = pygame.surface.Surface(screen_size)
        self.font = font

    def handle_event(self, event):
        return 'main_menu'

    def draw(self):
        self.surface.fill((245, 245, 220))
