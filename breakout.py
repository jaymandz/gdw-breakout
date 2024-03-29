import json, os, sys

sys.path.append('.')

import pygame
from pygame import locals

from asset_utils import path
from pages import credits as credits_module
from pages import new_game as new_game_module
from pages import main_menu as main_menu_module
from pages import scores as scores_module
from pages import settings as settings_module

pygame.init()

SCREEN_SIZE = (640, 480)

screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

if not os.path.isfile('./scores.json'):
    with open('./scores.json', 'w') as sf:
        json.dump([], sf)
        sf.close()

if not os.path.isfile('./settings.json'):
    with open('./settings.json', 'w') as sf:
        data = { 'music_on': True, 'music_volume': 10, 'sfx_on': True }
        json.dump(data, sf)
        sf.close()

scores_file = open('./scores.json', 'r')
scores = json.load(scores_file)
scores_file.close()

settings_file = open('./settings.json', 'r')
settings = json.load(settings_file)
settings_file.close()

pages = {
    'credits': credits_module.CreditsPage(SCREEN_SIZE, settings),
    'new_game': new_game_module.NewGamePage(SCREEN_SIZE, settings),
    'main_menu': main_menu_module.MainMenuPage(SCREEN_SIZE, settings),
    'scores': scores_module.ScoresPage(SCREEN_SIZE, settings),
    'settings': settings_module.SettingsPage(SCREEN_SIZE, settings),
}

curr_page_key = 'main_menu'

pygame.display.set_caption('Breakout, by jaymandz')

pygame.mixer.music.set_endevent(locals.USEREVENT + 1)

pygame.mixer.music.load(path('audio/Andrey Avkhimovich - Like A Cake.mp3'))
pygame.mixer.music.set_volume(settings['music_volume'] * 0.1)

if settings['music_on']: pygame.mixer.music.play()

while True:
    for event in pygame.event.get():
        new_page_key, settings = pages[curr_page_key].handle_event(event)
        if new_page_key != curr_page_key:
            pages[new_page_key].load()
            curr_page_key = new_page_key

        if event.type == locals.QUIT:
            settings_file = open('./settings.json', 'w')
            json.dump(settings, settings_file)
            settings_file.close()
            sys.exit()
        elif event.type == locals.USEREVENT + 1:
            if settings['music_on']: pygame.mixer.music.play()

    pages[curr_page_key].draw()
    screen.blit(pages[curr_page_key].surface, (0, 0))

    pygame.display.update()
