import sys
sys.path.append('.')

import pygame
from pygame import locals

from pages import credits as credits_module
from pages import game as game_module
from pages import main_menu as main_menu_module

pygame.init()

SCREEN_SIZE = (640, 480)

screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

pages = {
    'credits': credits_module.CreditsPage(SCREEN_SIZE),
    'game': game_module.GamePage(SCREEN_SIZE),
    'main_menu': main_menu_module.MainMenuPage(SCREEN_SIZE),
}

curr_page_key = 'main_menu'

pygame.display.set_caption('Breakout, by jaymandz')

while True:
    for event in pygame.event.get():
        curr_page_key = pages[curr_page_key].handle_event(event)
        if event.type == locals.QUIT: sys.exit()

    pages[curr_page_key].draw()
    screen.blit(pages[curr_page_key].surface, (0, 0))

    pygame.display.update()
