import pygame
from pygame import locals

import colors
import text_utils as tu

class PausePage(object):
    def __init__(self, screen_size):
        self.surface = pygame.surface.Surface(screen_size)
        self.num_items = 2
        self.curr_item_index = 0

    def _item_color(self, index):
        if index == self.curr_item_index: return colors.dark_red
        else: return colors.black

    def load(self):
        self.curr_item_index = 0

    def handle_event(self, event):
        ni = self.num_items

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[locals.K_ESCAPE]:
            return 'new_game'
        elif pressed_keys[locals.K_UP]:
            self.curr_item_index = (self.curr_item_index - 1) % ni
        elif pressed_keys[locals.K_DOWN]:
            self.curr_item_index = (self.curr_item_index + 1) % ni
        elif pressed_keys[locals.K_RETURN]:
            if self.curr_item_index == 0: return 'new_game'
            elif self.curr_item_index == 1: return 'main_menu'

        return 'pause'

    def draw(self):
        self.surface.fill(colors.beige)

        self.surface.blit(
            tu.regular_text(self._item_color(0), 'Resume'),
            (40, 40),
        )

        self.surface.blit(
            tu.regular_text(self._item_color(1), 'Main menu'),
            (40, 40 + tu.line_size(1.5)),
        )
