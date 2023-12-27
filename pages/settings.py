import pygame
from pygame import locals

import colors, text_utils as tu

class SettingsPage(object):
    def __init__(self, screen_size, settings):
        self.settings = settings
        self.surface = pygame.surface.Surface(screen_size)
        self.num_items = 2

    def _item_color(self, index):
        if index == self.curr_item_index: return colors.dark_red
        else: return colors.black

    def _toggle_settings(self):
        if self.curr_item_index == 0:
            if self.settings['music']: pygame.mixer.music.stop()
            else: pygame.mixer.music.play()
            self.settings['music'] = not self.settings['music']
        elif self.curr_item_index == 1:
            self.settings['sfx'] = not self.settings['sfx']

    def load(self):
        self.curr_item_index = 0

    def handle_event(self, event):
        ni = self.num_items

        if event.type == locals.KEYUP:
            if event.key == locals.K_SPACE: self._toggle_settings()

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[locals.K_DOWN]:
            self.curr_item_index = (self.curr_item_index + 1) % ni
        elif pressed_keys[locals.K_UP]:
            self.curr_item_index = (self.curr_item_index - 1) % ni
        elif pressed_keys[locals.K_ESCAPE]:
            return 'main_menu', self.settings

        return 'settings', self.settings

    def draw(self):
        self.surface.fill(colors.beige)

        music_text = '[{}] Music'.format(
            'x' if self.settings['music'] else ' '
        )
        self.surface.blit(
            tu.regular_text(self._item_color(0), music_text),
            (40, 40),
        )

        effects_text = '[{}] Sound effects'.format(
            'x' if self.settings['sfx'] else ' '
        )
        self.surface.blit(
            tu.regular_text(self._item_color(1), effects_text),
            (40, 40 + tu.line_size(1.5)),
        )

        footer_text = '\u2191\u2193: Highlight, <Space>: Toggle, '+ \
          '<Esc>: Back'
        self.surface.blit(
            tu.regular_text(colors.gray, footer_text),
            (20, 480 - 20 - tu.line_size()),
        )
