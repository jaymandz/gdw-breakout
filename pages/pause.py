import pygame
from pygame import locals

import colors
import text_utils as tu

class PausePage(object):
    def __init__(self, screen_size, settings):
        self.screen_size = screen_size
        self.settings = settings

        self.surface = pygame.surface.Surface(screen_size)
        self.num_items = 2
        self.curr_item_index = 0

    def _item_color(self, index):
        if index == self.curr_item_index: return colors.dark_red
        else: return colors.black

    def load(self):
        self.curr_item_index = 0

    def handle_event(self, event):
        settings = self.settings
        ni = self.num_items

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[locals.K_ESCAPE]:
            return 'new_game', settings
        elif pressed_keys[locals.K_UP]:
            self.curr_item_index = (self.curr_item_index - 1) % ni
        elif pressed_keys[locals.K_DOWN]:
            self.curr_item_index = (self.curr_item_index + 1) % ni
        elif pressed_keys[locals.K_RETURN]:
            if self.curr_item_index == 0: return 'new_game', settings
            elif self.curr_item_index == 1: return 'main_menu', settings

        return 'pause', settings

    def draw(self):
        self.surface.fill(colors.beige)

        sentence_surface = tu.regular_text(
            colors.blue,
            'The game is paused.'
        )
        self.surface.blit(
            sentence_surface,
            (self.screen_size[0]/2 - sentence_surface.get_size()[0]/2, 20),
        )

        self.surface.blit(
            tu.regular_text(self._item_color(0), 'Resume'),
            (40, tu.header_height()),
        )

        self.surface.blit(
            tu.regular_text(self._item_color(1), 'Main menu'),
            (40, tu.header_height() + tu.line_size(1.5)),
        )

        footer_text = '\u2191\u2193: Highlight, <Enter>: Select, '+ \
          '<Esc>: Resume'
        self.surface.blit(
            tu.regular_text(colors.gray, footer_text),
            (20, 480 - 20 - tu.line_size()),
        )
