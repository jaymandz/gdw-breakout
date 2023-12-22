import pygame
from pygame import locals

import colors, text_utils as tu

class SettingsPage(object):
    def __init__(self, screen_size):
        self.surface = pygame.surface.Surface(screen_size)

    def load(self):
        pass

    def handle_event(self, event):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[locals.K_ESCAPE]:
            return 'main_menu'

        return 'settings'

    def draw(self):
        self.surface.fill(colors.beige)

        self.surface.blit(
            tu.regular_text(colors.black, '[ ] Music'),
            (40, 40),
        )

        self.surface.blit(
            tu.regular_text(colors.black, '[ ] Effects'),
            (40, 40 + tu.line_size(1.5)),
        )

        footer_text = '\u2191\u2193: Highlight, <Space>: Toggle, '+ \
          '<Esc>: Back'
        self.surface.blit(
            tu.regular_text(colors.gray, footer_text),
            (20, 480 - 20 - tu.line_size()),
        )
