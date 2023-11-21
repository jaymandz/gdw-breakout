import pygame
from pygame import locals

import colors
import text_utils as tu

class CreditsPage(object):
    def __init__(self, screen_size):
        self.surface = pygame.surface.Surface(screen_size)

    def load(self):
        pass

    def handle_event(self, event):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[locals.K_ESCAPE]: return 'main_menu'

        return 'credits'

    def draw(self):
        self.surface.fill(colors.beige)

        self.surface.blit(
            tu.regular_text(colors.black, 'Code'),
            (40, 40),
        )
        self.surface.blit(
            tu.regular_text(colors.black, 'Jay Mandane'),
            (360, 40),
        )
        self.surface.blit(
            tu.italic_text(colors.black, 'github.com/jaymandz'),
            (360, 40 + tu.line_size()),
        )

        self.surface.blit(
            tu.regular_text(colors.black, 'Music'),
            (40, 40 + tu.line_size() * 3),
        )
        self.surface.blit(
            tu.italic_text(colors.black, 'TBD'),
            (360, 40 + tu.line_size() * 3),
        )

        self.surface.blit(
            tu.regular_text(colors.black, 'Sound effects'),
            (40, 40 + tu.line_size() * 5),
        )
        self.surface.blit(
            tu.italic_text(colors.black, 'TBD'),
            (360, 40 + tu.line_size() * 5),
        )

        self.surface.blit(
            tu.regular_text(colors.black, 'Fonts'),
            (40, 40 + tu.line_size() * 7),
        )

        # Footer
        self.surface.blit(
            tu.regular_text(colors.gray, '<Esc>: Back'),
            (20, 480 - 20 - tu.line_size()),
        )
