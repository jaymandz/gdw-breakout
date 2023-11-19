import pygame

import colors
import text_utils as tu

class MainMenuPage(object):
    def __init__(self, screen_size):
        self.surface = pygame.surface.Surface(screen_size)
        self.current_item = 'new_game'

    def _item_color(self, item):
        if item == self.current_item: return colors.dark_red
        else: return colors.black

    def handle_event(self, event):
        return 'main_menu'

    def draw(self):
        self.surface.fill(colors.beige)

        self.surface.blit(
            tu.regular_text(self._item_color('new_game'), 'New game'),
            (40, 40),
        )
        self.surface.blit(
            tu.regular_text(self._item_color('credits'), 'Credits'),
            (40, 40 + tu.line_size(1.5)),
        )
        self.surface.blit(
            tu.regular_text(self._item_color('exit'), 'Exit'),
            (40, 40 + tu.line_size(1.5) * 2),
        )


