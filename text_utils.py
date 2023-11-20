import pygame

pygame.init()

fonts = {
    'regular': pygame.font.Font(
        'fonts/MonaspaceNeon-Regular.otf', 16
    ),
    'bold': pygame.font.Font(
        'fonts/MonaspaceNeon-Bold.otf', 16
    ),
    'italic': pygame.font.Font(
        'fonts/MonaspaceNeon-Italic.otf', 16
    ),
    'bold-italic': pygame.font.Font(
        'fonts/MonaspaceNeon-BoldItalic.otf', 16
    ),
}

def line_size(spacing=1.0):
    return fonts['regular'].get_linesize() * spacing

def regular_text(color, text):
    return fonts['regular'].render(text, True, color)

def italic_text(color, text):
    return fonts['italic'].render(text, True, color)

def header_height(): return line_size() + 40
def footer_height(): return line_size() + 40
