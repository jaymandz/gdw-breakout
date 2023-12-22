import sys

import pygame
from pygame import locals

import colors
import text_utils as tu

class MainMenuPage(object):
    def __init__(self, screen_size):
        self.surface = pygame.surface.Surface(screen_size)
        self.num_items = 5
        self.curr_item_index = 0

    def _item_color(self, index):
        if index == self.curr_item_index: return colors.dark_red
        else: return colors.black

    def load(self):
        self.curr_item_index = 0

    def handle_event(self, event):
        ni = self.num_items

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[locals.K_DOWN]:
            self.curr_item_index = (self.curr_item_index + 1) % ni
        elif pressed_keys[locals.K_UP]:
            self.curr_item_index = (self.curr_item_index - 1) % ni
        elif pressed_keys[locals.K_RETURN]:
            if self.curr_item_index == 0: return 'new_game'
            #elif self.curr_item_index == 1: return 'settings'
            #elif self.curr_item_index == 2: return 'controls'
            elif self.curr_item_index == 3: return 'credits'
            elif self.curr_item_index == 4: sys.exit()
        elif pressed_keys[locals.K_ESCAPE]: sys.exit()

        return 'main_menu'

    def draw(self):
        self.surface.fill(colors.beige)

        self.surface.blit(
            tu.regular_text(self._item_color(0), 'New game'),
            (40, 40),
        )
        self.surface.blit(
            tu.regular_text(self._item_color(1), 'Settings'),
            (40, 40 + tu.line_size(1.5)),
        )
        self.surface.blit(
            tu.regular_text(self._item_color(2), 'Controls'),
            (40, 40 + tu.line_size(1.5) * 2),
        )
        self.surface.blit(
            tu.regular_text(self._item_color(3), 'Credits'),
            (40, 40 + tu.line_size(1.5) * 3),
        )
        self.surface.blit(
            tu.regular_text(self._item_color(4), 'Exit'),
            (40, 40 + tu.line_size(1.5) * 4),
        )

        # Footer
        footer_text = '\u2191\u2193: Highlight, <Enter>: Select, '+ \
          '<Esc>: Exit'
        self.surface.blit(
            tu.regular_text(colors.gray, footer_text),
            (20, 480 - 20 - tu.line_size()),
        )
