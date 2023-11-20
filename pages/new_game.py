import pygame
from pygame import locals

import colors
import text_utils as tu

class NewGamePage(object):
    PADDLE_SIZE = (80, 10)
    BALL_RADIUS = 10

    def __init__(self, screen_size):
        self.surface = pygame.surface.Surface(screen_size)

        self.paddle_position = (
            screen_size[0] / 2 - self.PADDLE_SIZE[0] / 2,
            screen_size[1] - self.PADDLE_SIZE[1] - tu.footer_height(),
        )
        self.ball_position = (
            screen_size[0] / 2,
            screen_size[1] - self.PADDLE_SIZE[1] - self.BALL_RADIUS - \
              tu.footer_height(),
        )

    def handle_event(self, event):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[locals.K_ESCAPE]: return 'main_menu'

        return 'new_game'

    def draw(self):
        self.surface.fill(colors.beige)

        pygame.draw.rect(
            self.surface,
            colors.black,
            locals.Rect(self.paddle_position, self.PADDLE_SIZE),
        )
        pygame.draw.circle(
            self.surface,
            colors.dark_red,
            self.ball_position,
            self.BALL_RADIUS,
        )

        # Footer
        footer_text = '<Space>: Launch, \u2190\u2192: Move, '+ \
          '<Esc>: Pause'
        self.surface.blit(
            tu.regular_text(colors.gray, footer_text),
            (20, 480 - 20 - tu.line_size()),
        )
