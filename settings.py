import pygame
import sys
from submenu import SubMenu

class SettingsMenu(SubMenu):
    def __init__(self, window):
        buttons = {
            "back": {
                "normal": pygame.transform.scale(pygame.image.load("image/menu/back.png").convert_alpha(), (200, 80)),
                "hover": pygame.transform.scale(pygame.image.load("image/menu/back_hover.png").convert_alpha(), (200, 80)),
                "rect": pygame.Rect(50, 600, 200, 80)
            }
        }
        super().__init__(window, "image/menu/settings_background.png", buttons)

    def draw_settings(self):
        font = pygame.font.Font(None, 60)
        text = font.render("Налаштування:", True, (255, 255, 255))
        self.window.blit(text, (100, 100))
        # Додати логіку налаштувань
