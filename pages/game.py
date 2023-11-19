import pygame
from pygame import locals

class GamePage(object):
    PADDLE_SIZE = (80, 10)
    BALL_RADIUS = 10

    def __init__(self, screen_size, font):
        self.surface = pygame.surface.Surface(screen_size)
        self.font = font

        self.paddle_position = (
            screen_size[0] / 2 - self.PADDLE_SIZE[0] / 2,
            screen_size[1] - self.PADDLE_SIZE[1],
        )
        self.ball_position = (
            screen_size[0] / 2,
            screen_size[1] - self.PADDLE_SIZE[1] - self.BALL_RADIUS,
        )

    def handle_event(self, event):
        return 'game'

    def draw(self):
        self.surface.fill((245, 245, 220))

        pygame.draw.rect(
            self.surface,
            (153, 153, 153),
            locals.Rect(self.paddle_position, self.PADDLE_SIZE),
        )
        pygame.draw.circle(
            self.surface,
            (255, 0, 0),
            self.ball_position,
            self.BALL_RADIUS,
        )
