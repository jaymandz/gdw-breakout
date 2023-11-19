import pygame

class CreditsPage(object):
    def __init__(self, screen_size, fonts):
        self.surface = pygame.surface.Surface(screen_size)
        self.fonts = fonts

    def _regular_text(self, text):
        return self.fonts['regular'].render(text, True, (0, 0, 0))

    def _italic_text(self, text):
        return self.fonts['italic'].render(text, True, (0, 0, 0))

    def handle_event(self, event):
        return 'credits'

    def draw(self):
        self.surface.fill((245, 245, 220))

        self.surface.blit(self._regular_text('Code'), (40, 40))
        self.surface.blit(self._regular_text('Jay Mandane'), (360, 40))
        self.surface.blit(
            self._italic_text('github.com/jaymandz'),
            (360, 40 + self.fonts['italic'].get_linesize()),
        )

        self.surface.blit(
            self._regular_text('Music'),
            (40, 40 + self.fonts['regular'].get_linesize() * 3),
        )
        self.surface.blit(
            self._italic_text('TBD'),
            (360, 40 + self.fonts['italic'].get_linesize() * 3),
        )

        self.surface.blit(
            self._regular_text('Sound effects'),
            (40, 40 + self.fonts['regular'].get_linesize() * 5),
        )
        self.surface.blit(
            self._italic_text('TBD'),
            (360, 40 + self.fonts['italic'].get_linesize() * 5),
        )

        self.surface.blit(
            self._regular_text('Fonts'),
            (40, 40 + self.fonts['regular'].get_linesize() * 7),
        )
