import pygame
from pygame import locals

import colors, text_utils as tu
from asset_utils import path

class SettingsPage(object):
    def __init__(self, screen_size, settings):
        self.settings = settings
        self.surface = pygame.surface.Surface(screen_size)
        self.num_items = 3

        self.menu_key_press_sound = pygame.mixer.Sound(
            path('audio/menu-key-press.ogg')
        )

    def _item_color(self, index):
        if index == self.curr_item_index: return colors.dark_red
        else: return colors.black

    def _toggle_settings(self):
        if self.curr_item_index == 0:
            if self.settings['music_on']: pygame.mixer.music.stop()
            else: pygame.mixer.music.play()
            self.settings['music_on'] = not self.settings['music_on']
        elif self.curr_item_index == 2:
            self.settings['sfx_on'] = not self.settings['sfx_on']

    def _decrease_setting_value(self):
        if self.curr_item_index == 1:
            if self.settings['music_volume'] == 1: return
            self.settings['music_volume'] -= 1

            music_volume = self.settings['music_volume']
            pygame.mixer.music.set_volume(music_volume * 0.1)

    def _increase_setting_value(self):
        if self.curr_item_index == 1:
            if self.settings['music_volume'] == 10: return
            self.settings['music_volume'] += 1

            music_volume = self.settings['music_volume']
            pygame.mixer.music.set_volume(music_volume * 0.1)

    def load(self):
        self.curr_item_index = 0

    def handle_event(self, event):
        ni = self.num_items

        if event.type == locals.KEYUP:
            if event.key == locals.K_SPACE: self._toggle_settings()

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[locals.K_DOWN]:
            self.curr_item_index = (self.curr_item_index + 1) % ni
            self.menu_key_press_sound.play()
        elif pressed_keys[locals.K_UP]:
            self.curr_item_index = (self.curr_item_index - 1) % ni
            self.menu_key_press_sound.play()
        elif pressed_keys[locals.K_LEFT]:
            self._decrease_setting_value()
        elif pressed_keys[locals.K_RIGHT]:
            self._increase_setting_value()
        elif pressed_keys[locals.K_ESCAPE]:
            self.menu_key_press_sound.play()
            return 'main_menu', self.settings

        return 'settings', self.settings

    def draw(self):
        self.surface.fill(colors.beige)

        music_text = ' [{}]  Music'.format(
            'x' if self.settings['music_on'] else ' '
        )
        self.surface.blit(
            tu.regular_text(self._item_color(0), music_text),
            (40, 40),
        )

        music_volume = self.settings['music_volume']
        music_volume_text = '\u2039[{}]\u203a Music volume'.format(
            'x' if music_volume == 10 else music_volume
        )
        self.surface.blit(
            tu.regular_text(self._item_color(1), music_volume_text),
            (40, 40 + tu.line_size(1.5)),
        )

        effects_text = ' [{}]  Sound effects'.format(
            'x' if self.settings['sfx_on'] else ' '
        )
        self.surface.blit(
            tu.regular_text(self._item_color(2), effects_text),
            (40, 40 + tu.line_size(1.5) * 2),
        )

        footer_text = '\u2191\u2193: Highlight, <Space>: Toggle, '+ \
          '\u2190\u2192: Sub/Add, <Esc>: Back'
        self.surface.blit(
            tu.regular_text(colors.gray, footer_text),
            (20, 480 - 20 - tu.line_size()),
        )
