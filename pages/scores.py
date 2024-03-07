import json
from math import ceil

import pygame
from pygame import locals

import colors, text_utils as tu
from asset_utils import path

class ScoresPage(object):
    ITEMS_PER_PAGE = 12

    def __init__(self, screen_size, settings):
        self.settings = settings
        self.surface = pygame.surface.Surface(screen_size)

        self.menu_key_press_sound = pygame.mixer.Sound(
            path('audio/menu-key-press.ogg')
        )
    
    def _render_score(self, i, score):
        n = score['name']
        s = score['score']

        self.surface.blit(
            tu.regular_text(colors.black, '{}: {}'.format(n, s)),
            (40, tu.header_height() + tu.line_size(1.5) * i + 1),
        )

    def load(self):
        with open('./scores.json', 'r') as sf:
            self.scores = json.load(sf)
            sf.close()

        self.scores.sort(reverse=True, key=lambda s: s['score'])
        self.curr_page_index = 0

    def handle_event(self, event):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[locals.K_ESCAPE]:
            if self.settings['sfx_on']: self.menu_key_press_sound.play()
            return 'main_menu', self.settings
        elif pressed_keys[locals.K_LEFT]:
            if self.curr_page_index > 0: self.curr_page_index -= 1
        elif pressed_keys[locals.K_RIGHT]:
            max_index = ceil(len(self.scores) / self.ITEMS_PER_PAGE) - 1
            if self.curr_page_index < max_index: self.curr_page_index += 1

        return 'scores', self.settings
    
    def draw(self):
        self.surface.fill(colors.beige)

        start_index = self.curr_page_index * self.ITEMS_PER_PAGE
        end_index = start_index + self.ITEMS_PER_PAGE

        for i, s in enumerate(self.scores[start_index:end_index]):
            self._render_score(i, s)

        footer_text = '<Esc>: Back, \u2190: Previous, \u2192: Next'
        self.surface.blit(
            tu.regular_text(colors.gray, footer_text),
            (20, 480 - 20 - tu.line_size()),
        )