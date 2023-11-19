import pygame

import colors

class MainMenuPage(object):
    def __init__(self, screen_size):
        self.surface = pygame.surface.Surface(screen_size)

    def handle_event(self, event):
        return 'main_menu'

    def draw(self):
        self.surface.fill(colors.beige)


