import json
from math import floor

import pygame
from pygame import locals

import colors
import text_utils as tu
from asset_utils import path

class NewGamePage(object):
    PADDLE_WIDTH = 180
    PADDLE_HEIGHT = 10
    BRICK_SIZE = (40, 16)
    BALL_RADIUS = 10
    BALL_SPEED_INCREMENT = 0.05
    INITIAL_BALL_SPEED_FACTOR = 0.1

    PADDLE_SPEED_FACTOR = 0.5

    def __init__(self, screen_size, settings):
        self.screen_size = screen_size
        self.settings = settings

        self.surface = pygame.surface.Surface(screen_size)
        self.clock = pygame.time.Clock()

        self.game_surface = pygame.surface.Surface(screen_size)
        self.pause_surface = pygame.surface.Surface(screen_size)
        self.game_over_surface = pygame.surface.Surface(screen_size)

        self.brick_smash_sound = pygame.mixer.Sound(
            path('audio/brick-smash.ogg')
        )
        self.ball_on_paddle_sound = pygame.mixer.Sound(
            path('audio/ball-on-paddle.ogg')
        )
        self.ball_launch_sound = pygame.mixer.Sound(
            path('audio/ball-launch.ogg')
        )
        self.ball_on_wall_sound = pygame.mixer.Sound(
            path('audio/ball-on-wall.ogg')
        )
        self.ball_speed_up_bell_sound = pygame.mixer.Sound(
            path('audio/ball-speed-up-bell.ogg')
        )
        self.tut_tut_sound = pygame.mixer.Sound(
            path('audio/tut-tut.ogg')
        )
        self.paddle_shrink_sound = pygame.mixer.Sound(
            path('audio/paddle-shrink.ogg')
        )
        self.game_reset_sound = pygame.mixer.Sound(
            path('audio/game-reset.ogg')
        )

        self.menu_key_press_sound = pygame.mixer.Sound(
            path('audio/menu-key-press.ogg')
        )

    def _play_panned(self, sound, x):
        if not self.settings['sfx_on']: return
        channel = sound.play()
        if channel is not None:
            right = x / self.screen_size[0]
            left = 1.0 - right
            channel.set_volume(left, right)

    def _ball_in_play_position(self, ball_x, ball_y):
        if ball_x < self.BALL_RADIUS:
            ball_x = self.BALL_RADIUS
            self._play_panned(self.ball_on_wall_sound, ball_x)
            self.ball_velocity_x = self.ball_speed_factor
        elif ball_x > self.screen_size[0] - self.BALL_RADIUS:
            ball_x = self.screen_size[0] - self.BALL_RADIUS
            self._play_panned(self.ball_on_wall_sound, ball_x)
            self.ball_velocity_x = -self.ball_speed_factor

        if ball_y < tu.header_height() + self.BALL_RADIUS:
            self._check_if_first_contact_with_ceiling()
            self._play_panned(self.ball_on_wall_sound, ball_x)
            ball_y = tu.header_height() + self.BALL_RADIUS
            self.ball_velocity_y = self.ball_speed_factor
        elif ball_y > self.screen_size[1] - tu.footer_height() - \
          self.BALL_RADIUS - self.paddle_size[1] and \
          ball_x >= self.paddle_position[0] and \
          ball_x <= self.paddle_position[0] + self.paddle_size[0]:
            self._play_panned(self.ball_on_paddle_sound, ball_x)
            ball_y = self.screen_size[1] - tu.footer_height() - \
              self.BALL_RADIUS - self.paddle_size[1]
            self.ball_velocity_y = -self.ball_speed_factor
        elif ball_y > self.screen_size[1] - tu.footer_height():
            if self.settings['sfx_on']: self.tut_tut_sound.play()
            self.num_lives -= 1
            ball_x, ball_y = self._rest_ball()

        if self.num_lives == 0: self._activate_game_over_mode()

        # Check for collision with bricks
        is_every_brick_hit = True
        for b, brick in enumerate(self.bricks):
            self.bricks[b], ball_x, ball_y = self._check_brick_collision(
              brick, ball_x, ball_y)
            if brick[3]: is_every_brick_hit = False

        # Check if all bricks were hit. If true, put ball at rest and
        # reset all bricks.
        if is_every_brick_hit:
            self.num_hits = 0
            self.is_contact_with_orange_blocks_made = False
            self.is_contact_with_red_blocks_made = False
            self.is_contact_with_ceiling_made = False

            self.paddle_size = (self.paddle_size[0] * 2, self.paddle_size[1])
            ball_x, ball_y = self._rest_ball()
            self.bricks = self._initialize_bricks()
            
            self.ball_speed_factor = self.INITIAL_BALL_SPEED_FACTOR
            self.speed_multiplier = 1

            self.game_reset_sound.play()

        return ball_x, ball_y

    def _add_brick_hit_and_adjust_speed(self, brick):
        is_speed_to_be_increased = False

        self.num_hits += 1
        if brick[0] == colors.orange:
            if not self.is_contact_with_orange_blocks_made:
              is_speed_to_be_increased = True
            self.is_contact_with_orange_blocks_made = True
        elif brick[0] == colors.red:
            if not self.is_contact_with_red_blocks_made:
              is_speed_to_be_increased = True
            self.is_contact_with_red_blocks_made = True
        elif self.num_hits == 4: is_speed_to_be_increased = True
        elif self.num_hits == 12: is_speed_to_be_increased = True

        if is_speed_to_be_increased:
            increment = self.BALL_SPEED_INCREMENT
            if self.ball_velocity_x < 0: self.ball_velocity_x -= increment
            elif self.ball_velocity_x > 0: self.ball_velocity_x += increment

            if self.ball_velocity_y < 0: self.ball_velocity_y -= increment
            elif self.ball_velocity_y > 0: self.ball_velocity_y += increment

            self.ball_speed_factor += increment
            self.speed_multiplier += 1

            self.ball_speed_up_bell_sound.play()

    def _check_brick_collision(self, brick, ball_x, ball_y):
        if not self.is_ball_in_play: return brick, ball_x, ball_y
        if not brick[3]: return brick, ball_x, ball_y

        is_hit = False

        # Hit from the top
        if self.ball_velocity_y > 0 and ball_x >= brick[1][0] and \
          ball_x <= brick[1][0] + self.BRICK_SIZE[0] and floor(ball_y) == \
          brick[1][1] - self.BALL_RADIUS:
            self._play_panned(self.brick_smash_sound, ball_x)
            self.score += brick[2]
            is_hit = True
            self.ball_velocity_y = -self.ball_speed_factor
        # Hit from the bottom
        elif self.ball_velocity_y < 0 and ball_x >= brick[1][0] and \
          ball_x <= brick[1][0] + self.BRICK_SIZE[0] and floor(ball_y) == \
          brick[1][1] + self.BRICK_SIZE[1] + self.BALL_RADIUS:
            self._play_panned(self.brick_smash_sound, ball_x)
            self.score += brick[2]
            is_hit = True
            self.ball_velocity_y = self.ball_speed_factor

        # Hit from the left
        elif self.ball_velocity_x > 0 and ball_y >= brick[1][1] and \
          ball_y <= brick[1][1] + self.BRICK_SIZE[1] and floor(ball_x) == \
          brick[1][0] - self.BALL_RADIUS:
            self._play_panned(self.brick_smash_sound, ball_x)
            self.score += brick[2]
            is_hit = True
            self.ball_velocity_x = -self.ball_speed_factor
        # Hit from the right
        elif self.ball_velocity_x < 0 and ball_y >= brick[1][1] and \
          ball_y <= brick[1][1] + self.BRICK_SIZE[1] and floor(ball_x) == \
          brick[1][0] + self.BRICK_SIZE[0] + self.BALL_RADIUS:
            self._play_panned(self.brick_smash_sound, ball_x)
            self.score += brick[2]
            is_hit = True
            self.ball_velocity_x = self.ball_speed_factor

        if is_hit:
            brick = (brick[0], brick[1], brick[2], False)
            self._add_brick_hit_and_adjust_speed(brick)

        return brick, ball_x, ball_y

    def _get_ball_position(self, time_elapsed_ms):
        ball_x = self.ball_position[0] + self.ball_velocity_x * \
          time_elapsed_ms
        ball_y = self.ball_position[1] + self.ball_velocity_y * \
          time_elapsed_ms

        ball_x, ball_y = self._ball_in_play_position(ball_x, ball_y)
        if not self.is_ball_in_play:
            half_paddle = self.paddle_size[0] / 2
            if ball_x < half_paddle: ball_x = half_paddle
            elif ball_x > 640 - half_paddle: ball_x = 640 - half_paddle

        return ball_x, ball_y

    def _initialize_bricks(self):
        bricks = []
        for b in range(0, self.screen_size[0], 46):
            bricks.append((colors.red, (b, tu.header_height() + 80), 7,
              True))
            bricks.append((colors.red, (b, tu.header_height() + 100), 7,
              True))
            bricks.append((colors.orange, (b, tu.header_height() + 120), 5,
              True))
            bricks.append((colors.orange, (b, tu.header_height() + 140), 5,
              True))
            bricks.append((colors.green, (b, tu.header_height() + 160), 3,
              True))
            bricks.append((colors.green, (b, tu.header_height() + 180), 3,
              True))
            bricks.append((colors.yellow, (b, tu.header_height() + 200), 1,
              True))
            bricks.append((colors.yellow, (b, tu.header_height() + 220), 1,
              True))
        return bricks

    def _speed_surface_color(self):
        if self.speed_multiplier == 1: return colors.gray
        elif self.speed_multiplier == 2: return colors.black
        elif self.speed_multiplier == 3: return colors.green
        elif self.speed_multiplier == 4: return colors.orange
        elif self.speed_multiplier == 5: return colors.red

    def _pause_item_color(self, index):
        if index == self.curr_pause_item_index: return colors.dark_red
        else: return colors.black

    def _toggle_pause_mode(self):
        if self.is_paused:
            self.ball_velocity_x = self.game_state['ball_velocity_x']
            self.ball_velocity_y = self.game_state['ball_velocity_y']
            self.is_paused = False
        else:
            self.game_state['ball_velocity_x'] = self.ball_velocity_x
            self.game_state['ball_velocity_y'] = self.ball_velocity_y
            self.ball_velocity_x = 0
            self.ball_velocity_y = 0
            self.is_paused = True
    
    def _save_score(self):
        scores = None

        with open('./scores.json', 'r') as sf:
            scores = json.load(sf)
            sf.close()

        with open('./scores.json', 'w') as sf:
            scores.append({ 'name': self.player_name, 'score': self.score })
            json.dump(scores, sf)
            sf.close()
    
    def _activate_game_over_mode(self):
        self.is_game_over = True
    
    def _append_to_player_name(self, event):
        if event.key >= locals.K_SPACE and event.key <= locals.K_z:
            self.player_name += event.unicode
        elif event.key == locals.K_BACKSPACE:
            self.player_name = self.player_name[:len(self.player_name)-1]

    def _rest_ball(self):
        self.is_ball_in_play = False
        ball_x = self.paddle_position[0] + self.paddle_size[0] / 2
        ball_y = self.screen_size[1] - tu.footer_height() - \
          self.paddle_size[1] - self.BALL_RADIUS
        self.ball_velocity_x = self.paddle_velocity
        self.ball_velocity_y = 0
        return ball_x, ball_y
    
    def _check_if_first_contact_with_ceiling(self):
        if not self.is_contact_with_ceiling_made:
            self.paddle_size = (self.PADDLE_WIDTH / 2, self.PADDLE_HEIGHT)
            self.is_contact_with_ceiling_made = True
            self.paddle_shrink_sound.play()

    def load(self):
        self.paddle_size = (self.PADDLE_WIDTH, self.PADDLE_HEIGHT)
        self.paddle_position = (
            self.screen_size[0] / 2 - self.paddle_size[0] / 2,
            self.screen_size[1] - self.paddle_size[1] - tu.footer_height(),
        )
        self.ball_position = (
            self.screen_size[0] / 2,
            self.screen_size[1] - self.paddle_size[1] - \
              self.BALL_RADIUS - tu.footer_height(),
        )

        self.bricks = self._initialize_bricks()

        self.ball_speed_factor = self.INITIAL_BALL_SPEED_FACTOR
        self.paddle_velocity = 0
        self.ball_velocity_x = 0
        self.ball_velocity_y = 0
        self.is_ball_in_play = False

        self.num_lives = 3
        self.num_hits = 0
        self.score = 0
        self.speed_multiplier = 1

        self.is_contact_with_orange_blocks_made = False
        self.is_contact_with_red_blocks_made = False
        self.is_contact_with_ceiling_made = False

        self.is_paused = False
        self.num_pause_items = 2
        self.curr_pause_item_index = 0

        self.is_game_over = False
        self.player_name = ''
        self.curr_name_index = -1

        self.game_state = {
            'ball_velocity_x': None,
            'ball_velocity_y': None,
        }

    def handle_event(self, event):
        if event.type == locals.KEYUP and not self.is_game_over:
            self.paddle_velocity = 0
            if not self.is_ball_in_play: self.ball_velocity_x = 0
        elif event.type == locals.KEYUP and self.is_game_over:
            self._append_to_player_name(event)

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[locals.K_ESCAPE] and not self.is_game_over:
            self._toggle_pause_mode()
            self.menu_key_press_sound.play()
        elif pressed_keys[locals.K_ESCAPE] and self.is_game_over:
            return 'main_menu', self.settings
        elif pressed_keys[locals.K_SPACE] and not self.is_game_over and \
          not self.is_ball_in_play:
            self._play_panned(self.ball_launch_sound, self.ball_position[0])
            self.is_ball_in_play = True
            self.ball_velocity_x = self.ball_speed_factor
            self.ball_velocity_y = -self.ball_speed_factor
        elif pressed_keys[locals.K_LEFT]:
            self.paddle_velocity = -self.PADDLE_SPEED_FACTOR
            if not self.is_ball_in_play:
              self.ball_velocity_x = -self.PADDLE_SPEED_FACTOR
        elif pressed_keys[locals.K_RIGHT]:
            self.paddle_velocity = self.PADDLE_SPEED_FACTOR
            if not self.is_ball_in_play:
              self.ball_velocity_x = self.PADDLE_SPEED_FACTOR
        elif pressed_keys[locals.K_DOWN] and self.is_paused:
            npi = self.num_pause_items
            cpii = self.curr_pause_item_index
            self.curr_pause_item_index = (cpii + 1) % npi
            self.menu_key_press_sound.play()
        elif pressed_keys[locals.K_UP] and self.is_paused:
            npi = self.num_pause_items
            cpii = self.curr_pause_item_index
            self.curr_pause_item_index = (cpii - 1) % npi
            self.menu_key_press_sound.play()
        elif pressed_keys[locals.K_RETURN] and self.is_paused:
            self.menu_key_press_sound.play()
            cpii = self.curr_pause_item_index
            if cpii == 0: self._toggle_pause_mode()
            elif cpii == 1: return 'main_menu', self.settings
        elif pressed_keys[locals.K_RETURN] and self.is_game_over:
            self._save_score()
            return 'main_menu', self.settings

        return 'new_game', self.settings

    def draw(self):
        time_elapsed_ms = self.clock.tick()

        paddle_x = self.paddle_position[0] + self.paddle_velocity * \
          time_elapsed_ms
        if paddle_x < 0: paddle_x = 0
        elif paddle_x > 640 - self.paddle_size[0]:
            paddle_x = 640 - self.paddle_size[0]

        self.paddle_position = (paddle_x, self.paddle_position[1])
        self.ball_position = self._get_ball_position(time_elapsed_ms)

        self.game_surface.fill(colors.beige)

        # Header
        self.game_surface.blit(
            tu.regular_text(colors.gray, str(self.num_lives)+' lives'),
            (20, 20),
        )

        score_surface = tu.regular_text(colors.gray, str(self.score))
        self.game_surface.blit(
            score_surface,
            (self.screen_size[0]/2 - score_surface.get_size()[0]/2, 20),
        )

        speed_surface = tu.regular_text(
            self._speed_surface_color(),
            'Speed x '+str(self.speed_multiplier),
        )
        self.game_surface.blit(
            speed_surface,
            (self.screen_size[0]-speed_surface.get_size()[0]-20, 20),
        )

        # Draw bricks
        for brick in self.bricks:
            if brick[3]: pygame.draw.rect(self.game_surface, brick[0],
              locals.Rect(brick[1], self.BRICK_SIZE))

        # Draw paddle
        pygame.draw.rect(
            self.game_surface,
            colors.black,
            locals.Rect(self.paddle_position, self.paddle_size),
        )

        # Draw ball
        pygame.draw.circle(
            self.game_surface,
            colors.dark_red,
            self.ball_position,
            self.BALL_RADIUS,
        )

        # Game surface footer
        gs_footer_text = '<Space>: Launch, \u2190\u2192: Move, '+ \
          '<Esc>: Pause'
        self.game_surface.blit(
            tu.regular_text(colors.gray, gs_footer_text),
            (20, 480 - 20 - tu.line_size()),
        )

        self.pause_surface.fill(colors.beige)

        sentence_surface = tu.regular_text(
            colors.blue,
            'The game is paused.'
        )
        self.pause_surface.blit(
            sentence_surface,
            (self.screen_size[0]/2 - sentence_surface.get_size()[0]/2, 20),
        )

        self.pause_surface.blit(
            tu.regular_text(self._pause_item_color(0), 'Resume'),
            (40, tu.header_height()),
        )

        self.pause_surface.blit(
            tu.regular_text(self._pause_item_color(1), 'Main menu'),
            (40, tu.header_height() + tu.line_size(1.5)),
        )

        ps_footer_text = '\u2191\u2193: Highlight, <Enter>: Select, '+ \
          '<Esc>: Resume'
        self.pause_surface.blit(
            tu.regular_text(colors.gray, ps_footer_text),
            (20, 480 - 20 - tu.line_size()),
        )

        self.game_over_surface.fill(colors.beige)

        self.game_over_surface.blit(
            tu.regular_text(colors.black, 'Enter your name.'),
            (20, (self.screen_size[1] / 2) - tu.footer_height() - \
              tu.line_size(1.5)),
        )
        self.game_over_surface.blit(
            tu.regular_text(colors.blue, self.player_name+'\u00bb'),
            (20, (self.screen_size[1] / 2) - tu.footer_height()),
        )

        gos_footer_text = '\u2190\u2192: Move cursor, <Enter>: Save, '+ \
          '<Esc>: Skip'
        self.game_over_surface.blit(
            tu.regular_text(colors.gray, gos_footer_text),
            (20, 480 - 20 - tu.line_size()),
        )

        if self.is_paused:
            self.surface.blit(self.pause_surface, (0, 0))
        elif self.is_game_over:
            self.surface.blit(self.game_over_surface, (0, 0))
        else:
            self.surface.blit(self.game_surface, (0, 0))
