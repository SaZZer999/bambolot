import pygame
from menu import Menu

class SubMenu(Menu):
    def __init__(self, window, background_image, exit_hover_image, exit_button_rect):
        super().__init__(window, background_image)
        self.exit_hover = pygame.image.load(exit_hover_image).convert_alpha()
        self.exit_rect = exit_button_rect  # Прямокутник для натискання

    def draw(self):
        super().draw()  # Малюємо фон
        mouse_pos = pygame.mouse.get_pos()
        if self.exit_rect.collidepoint(mouse_pos):  # Якщо курсор над кнопкою виходу
            self.window.blit(self.exit_hover, self.exit_rect.topleft)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.exit_rect.collidepoint(event.pos):  # Перевірка натискання на кнопку виходу
                return "exit"  # Повертаємо "exit" як сигнал для повернення до головного меню
        return None
