import pygame
from pygame import locals

import colors
import text_utils as tu

class CreditsPage(object):
    def __init__(self, screen_size, settings):
        self.settings = settings
        self.surface = pygame.surface.Surface(screen_size)

    def load(self):
        pass

    def handle_event(self, event):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[locals.K_ESCAPE]: return 'main_menu', self.settings

        return 'credits', self.settings

    def draw(self):
        self.surface.fill(colors.beige)

        self.surface.blit(
            tu.bold_text(colors.black, 'Code'),
            (40, 40),
        )
        self.surface.blit(
            tu.regular_text(colors.black, 'Jay Mandane'),
            (50, 40 + tu.line_size()),
        )
        self.surface.blit(
            tu.regular_text(colors.black, 'https://github.com/jaymandz'),
            (50, 40 + tu.line_size() * 2),
        )

        self.surface.blit(
            tu.bold_text(colors.black, 'Music'),
            (40, 40 + tu.line_size() * 4),
        )
        self.surface.blit(
            tu.italic_text(colors.black, 'Andrey Avkhimovich - Like A Cake'),
            (50, 40 + tu.line_size() * 5),
        )
        self.surface.blit(
            tu.regular_text(colors.black, 'https://www.jamendo.com/track/1199570/like-a-cake'),
            (50, 40 + tu.line_size() * 6),
        )

        self.surface.blit(
            tu.bold_text(colors.black, 'Sound effects'),
            (40, 40 + tu.line_size() * 8),
        )
        self.surface.blit(
            tu.italic_text(colors.black, 'Ball bounce on paddle'),
            (50, 40 + tu.line_size() * 9),
        )
        self.surface.blit(
            tu.regular_text(colors.black, 'https://freesound.org/people/DanielRousseau/sounds/366780'),
            (50, 40 + tu.line_size() * 10),
        )

        self.surface.blit(
            tu.bold_text(colors.black, 'Fonts'),
            (40, 40 + tu.line_size() * 12),
        )

        # Footer
        self.surface.blit(
            tu.regular_text(colors.gray, '<Esc>: Back'),
            (20, 480 - 20 - tu.line_size()),
        )
