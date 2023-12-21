import os, sys

sys.path.append('.')

import pygame
from pygame import locals

from pages import credits as credits_module
from pages import new_game as new_game_module
from pages import main_menu as main_menu_module
from pages import pause as pause_module

pygame.init()

SCREEN_SIZE = (640, 480)

screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

pages = {
    'credits': credits_module.CreditsPage(SCREEN_SIZE),
    'new_game': new_game_module.NewGamePage(SCREEN_SIZE),
    'main_menu': main_menu_module.MainMenuPage(SCREEN_SIZE),
    'pause': pause_module.PausePage(SCREEN_SIZE),
}

curr_page_key = 'main_menu'

pygame.display.set_caption('Breakout, by jaymandz')

pygame.mixer.music.set_endevent(locals.USEREVENT + 1)

pygame.mixer.music.load('audio/Andrey Avkhimovich - Like A Cake.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()

while True:
    for event in pygame.event.get():
        new_page_key = pages[curr_page_key].handle_event(event)
        if new_page_key != curr_page_key:
            pages[new_page_key].load()
            curr_page_key = new_page_key
        if event.type == locals.QUIT: sys.exit()
        elif event.type == locals.USEREVENT + 1: pygame.mixer.music.play()

    pages[curr_page_key].draw()
    screen.blit(pages[curr_page_key].surface, (0, 0))

    pygame.display.update()
