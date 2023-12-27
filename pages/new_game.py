import math

import pygame
from pygame import locals

import colors
import text_utils as tu

class NewGamePage(object):
    PADDLE_SIZE = (80, 10)
    BRICK_SIZE = (40, 16)
    BALL_RADIUS = 10

    PADDLE_SPEED_FACTOR = 0.5
    BALL_SPEED_FACTOR = 0.2

    def __init__(self, screen_size, settings):
        self.screen_size = screen_size
        self.settings = settings

        self.surface = pygame.surface.Surface(screen_size)
        self.clock = pygame.time.Clock()

        self.brick_smash_sound = pygame.mixer.Sound(
            'audio/brick-smash.ogg'
        )
        self.ball_on_paddle_sound = pygame.mixer.Sound(
            'audio/ball-on-paddle.ogg'
        )
        self.ball_launch_sound = pygame.mixer.Sound(
            'audio/ball-launch.ogg'
        )
        self.ball_on_wall_sound = pygame.mixer.Sound(
            'audio/ball-on-wall.ogg'
        )
        self.tut_tut_sound = pygame.mixer.Sound(
            'audio/tut-tut.ogg'
        )

    def _play_panned(self, sound, x):
        if not self.settings['sfx']: return
        channel = sound.play()
        if channel is not None:
            right = x / self.screen_size[0]
            left = 1.0 - right
            channel.set_volume(left, right)

    def _ball_in_play_position(self, ball_x, ball_y):
        if ball_x < self.BALL_RADIUS:
            ball_x = self.BALL_RADIUS
            self._play_panned(self.ball_on_wall_sound, ball_x)
            self.ball_velocity_x = self.BALL_SPEED_FACTOR
        elif ball_x > self.screen_size[0] - self.BALL_RADIUS:
            ball_x = self.screen_size[0] - self.BALL_RADIUS
            self._play_panned(self.ball_on_wall_sound, ball_x)
            self.ball_velocity_x = -self.BALL_SPEED_FACTOR

        if ball_y < tu.header_height() + self.BALL_RADIUS:
            self._play_panned(self.ball_on_wall_sound, ball_x)
            ball_y = tu.header_height() + self.BALL_RADIUS
            self.ball_velocity_y = self.BALL_SPEED_FACTOR
        elif ball_y > self.screen_size[1] - tu.footer_height() - \
          self.BALL_RADIUS - self.PADDLE_SIZE[1] and \
          ball_x >= self.paddle_position[0] and \
          ball_x <= self.paddle_position[0] + self.PADDLE_SIZE[0]:
            self._play_panned(self.ball_on_paddle_sound, ball_x)
            ball_y = self.screen_size[1] - tu.footer_height() - \
              self.BALL_RADIUS - self.PADDLE_SIZE[1]
            self.ball_velocity_y = -self.BALL_SPEED_FACTOR
        elif ball_y > self.screen_size[1] - tu.footer_height():
            if self.settings['sfx']: self.tut_tut_sound.play()
            self.num_lives -= 1

            self.is_ball_in_play = False
            ball_x = self.paddle_position[0] + self.PADDLE_SIZE[0] / 2
            ball_y = self.screen_size[1] - tu.footer_height() - \
              self.PADDLE_SIZE[1] - self.BALL_RADIUS
            self.ball_velocity_x = self.paddle_velocity
            self.ball_velocity_y = 0

        # Check for collision with bricks
        for b, brick in enumerate(self.bricks):
            self.bricks[b], ball_x, ball_y = self._check_brick_collision(
              brick, ball_x, ball_y)

        return ball_x, ball_y

    def _check_brick_collision(self, brick, ball_x, ball_y):
        if not self.is_ball_in_play: return brick, ball_x, ball_y
        if not brick[2]: return brick, ball_x, ball_y

        # Find a damn good bouncing/collision algorithm first!

        return brick, ball_x, ball_y

    def _get_ball_position(self, time_elapsed_ms):
        ball_x = self.ball_position[0] + self.ball_velocity_x * \
          time_elapsed_ms
        ball_y = self.ball_position[1] + self.ball_velocity_y * \
          time_elapsed_ms

        ball_x, ball_y = self._ball_in_play_position(ball_x, ball_y)
        if not self.is_ball_in_play:
            half_paddle = self.PADDLE_SIZE[0] / 2
            if ball_x < half_paddle: ball_x = half_paddle
            elif ball_x > 640 - half_paddle: ball_x = 640 - half_paddle

        return ball_x, ball_y

    def _initialize_bricks(self):
        bricks = []
        for b in range(0, self.screen_size[0], 46):
            bricks.append((colors.red, (b, tu.header_height() + 80),
              True))
            bricks.append((colors.red, (b, tu.header_height() + 100),
              True))
            bricks.append((colors.orange, (b, tu.header_height() + 120),
              True))
            bricks.append((colors.orange, (b, tu.header_height() + 140),
              True))
            bricks.append((colors.green, (b, tu.header_height() + 160),
              True))
            bricks.append((colors.green, (b, tu.header_height() + 180),
              True))
            bricks.append((colors.yellow, (b, tu.header_height() + 200),
              True))
            bricks.append((colors.yellow, (b, tu.header_height() + 220),
              True))
        return bricks

    def load(self):
        self.paddle_position = (
            self.screen_size[0] / 2 - self.PADDLE_SIZE[0] / 2,
            self.screen_size[1] - self.PADDLE_SIZE[1] - tu.footer_height(),
        )
        self.ball_position = (
            self.screen_size[0] / 2,
            self.screen_size[1] - self.PADDLE_SIZE[1] - \
              self.BALL_RADIUS - tu.footer_height(),
        )

        self.bricks = self._initialize_bricks()

        self.paddle_velocity = 0
        self.ball_velocity_x = 0
        self.ball_velocity_y = 0
        self.is_ball_in_play = False

        self.num_lives = 3
        self.score = 0

    def handle_event(self, event):
        if event.type == locals.KEYUP:
            self.paddle_velocity = 0
            if not self.is_ball_in_play: self.ball_velocity_x = 0

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[locals.K_ESCAPE]:
            return 'pause', self.settings
        elif pressed_keys[locals.K_SPACE] and not self.is_ball_in_play:
            self._play_panned(self.ball_launch_sound, self.ball_position[0])
            self.is_ball_in_play = True
            self.ball_velocity_x = self.BALL_SPEED_FACTOR
            self.ball_velocity_y = -self.BALL_SPEED_FACTOR
        elif pressed_keys[locals.K_LEFT]:
            self.paddle_velocity = -self.PADDLE_SPEED_FACTOR
            if not self.is_ball_in_play:
              self.ball_velocity_x = -self.PADDLE_SPEED_FACTOR
        elif pressed_keys[locals.K_RIGHT]:
            self.paddle_velocity = self.PADDLE_SPEED_FACTOR
            if not self.is_ball_in_play:
              self.ball_velocity_x = self.PADDLE_SPEED_FACTOR

        return 'new_game', self.settings

    def draw(self):
        time_elapsed_ms = self.clock.tick()

        paddle_x = self.paddle_position[0] + self.paddle_velocity * \
          time_elapsed_ms
        if paddle_x < 0: paddle_x = 0
        elif paddle_x > 640 - self.PADDLE_SIZE[0]:
            paddle_x = 640 - self.PADDLE_SIZE[0]

        self.paddle_position = (paddle_x, self.paddle_position[1])
        self.ball_position = self._get_ball_position(time_elapsed_ms)

        self.surface.fill(colors.beige)

        # Header
        self.surface.blit(
            tu.regular_text(colors.gray, str(self.num_lives)+' lives'),
            (20, 20),
        )

        score_surface = tu.regular_text(colors.gray, str(self.score))
        self.surface.blit(
            score_surface,
            (self.screen_size[0]/2 - score_surface.get_size()[0]/2, 20),
        )

        # Draw bricks
        for brick in self.bricks:
            if brick[2]: pygame.draw.rect(self.surface, brick[0],
              locals.Rect(brick[1], self.BRICK_SIZE))

        # Draw paddle
        pygame.draw.rect(
            self.surface,
            colors.black,
            locals.Rect(self.paddle_position, self.PADDLE_SIZE),
        )

        # Draw ball
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
