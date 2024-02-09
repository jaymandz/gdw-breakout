import pygame
from pygame import locals

import colors
import text_utils as tu

class CreditsPage(object):
    def __init__(self, screen_size, settings):
        self.settings = settings

        self.surface = pygame.surface.Surface(screen_size)
        self.page1_surface = pygame.surface.Surface(screen_size)
        self.page2_surface = pygame.surface.Surface(screen_size)

    def load(self):
        self.current_page = 1

    def handle_event(self, event):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[locals.K_ESCAPE]: return 'main_menu', self.settings
        elif pressed_keys[locals.K_LEFT] and self.current_page == 2:
            self.current_page = 1
        elif pressed_keys[locals.K_RIGHT] and self.current_page == 1:
            self.current_page = 2

        return 'credits', self.settings

    def draw(self):
        self.page1_surface.fill(colors.beige)
        self.page2_surface.fill(colors.beige)

        self.page1_surface.blit(
            tu.bold_text(colors.black, 'Code'),
            (40, 40),
        )
        self.page1_surface.blit(
            tu.regular_text(colors.black, 'Jay Mandane'),
            (50, 40 + tu.line_size()),
        )
        self.page1_surface.blit(
            tu.regular_text(colors.black, 'https://github.com/jaymandz'),
            (50, 40 + tu.line_size() * 2),
        )

        self.page1_surface.blit(
            tu.bold_text(colors.black, 'Music'),
            (40, 40 + tu.line_size() * 4),
        )
        self.page1_surface.blit(
            tu.italic_text(colors.black, 'Andrey Avkhimovich - Like A Cake'),
            (50, 40 + tu.line_size() * 5),
        )
        self.page1_surface.blit(
            tu.regular_text(colors.black, 'https://www.jamendo.com/track/1199570/like-a-cake'),
            (50, 40 + tu.line_size() * 6),
        )

        self.page1_surface.blit(
            tu.bold_text(colors.black, 'Sound effects'),
            (40, 40 + tu.line_size() * 8),
        )
        self.page1_surface.blit(
            tu.italic_text(colors.black, 'Ball bounce on paddle'),
            (50, 40 + tu.line_size() * 9),
        )
        self.page1_surface.blit(
            tu.regular_text(colors.black, 'https://freesound.org/people/DanielRousseau/sounds/366780/'),
            (50, 40 + tu.line_size() * 10),
        )
        self.page1_surface.blit(
            tu.italic_text(colors.black, 'Bell sound on ball speed increase'),
            (50, 40 + tu.line_size() * 11),
        )
        self.page1_surface.blit(
            tu.regular_text(colors.black, 'https://freesound.org/people/cdrk/sounds/495484/'),
            (50, 40 + tu.line_size() * 12),
        )
        self.page1_surface.blit(
            tu.italic_text(colors.black, 'Sound when paddle shrinks'),
            (50, 40 + tu.line_size() * 13),
        )
        self.page1_surface.blit(
            tu.regular_text(colors.black, 'https://freesound.org/people/OTBTechno/sounds/136772/'),
            (50, 40 + tu.line_size() * 14),
        )
        self.page1_surface.blit(
            tu.italic_text(colors.black, 'Rewind sound on game reset'),
            (50, 40 + tu.line_size() * 15),
        )
        self.page1_surface.blit(
            tu.regular_text(colors.black, 'https://freesound.org/people/crunchymaniac/sounds/687272/'),
            (50, 40 + tu.line_size() * 16),
        )

        self.page2_surface.blit(
            tu.bold_text(colors.black, 'Fonts'),
            (40, 40),
        )
        self.page2_surface.blit(
            tu.italic_text(colors.black, 'Monaspace Neon'),
            (50, 40 + tu.line_size()),
        )
        self.page2_surface.blit(
            tu.regular_text(colors.black, 'https://monaspace.githubnext.com/'),
            (50, 40 + tu.line_size() * 2),
        )

        # Footer
        footer_text = '<Esc>: Back, \u2190: Previous, \u2192: Next'
        self.page1_surface.blit(
            tu.regular_text(colors.gray, footer_text),
            (20, 480 - 20 - tu.line_size()),
        )
        self.page2_surface.blit(
            tu.regular_text(colors.gray, footer_text),
            (20, 480 - 20 - tu.line_size()),
        )

        if self.current_page == 1:
            self.surface.blit(self.page1_surface, (0, 0))
        elif self.current_page == 2:
            self.surface.blit(self.page2_surface, (0, 0))
