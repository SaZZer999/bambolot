import pygame

class Menu:
    def __init__(self, window, background):
        self.window = window
        self.background = background
    def draw(self):
        self.window.blit(self.background, (0, 0))  # Малюємо фон

    def handle_events(self, event):
        pass  # Основне меню обробляє свої події в іншому місці
