import pygame
import random

class Life(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x=0, speed_y=5, window_height=600):
        super().__init__()  # Без аргументів, оскільки ми не додаємо до груп при ініціалізації

        # Завантаження та масштабування зображення життя
        self.original_image = pygame.image.load("image/life/life.png").convert_alpha()
        desired_width = 100
        desired_height = 100
        self.original_image = pygame.transform.scale(self.original_image, (desired_width, desired_height))
        self.image = self.original_image
        self.mask = pygame.mask.from_surface(self.original_image)

        # Позиція та швидкість
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.window_height = window_height

    def update(self):
        # Рух об'єкта
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

        # Якщо об'єкт вийшов за межі екрана, видаляємо його
        if self.rect.top > self.window_height:
            self.kill()

    def set_speed(self, new_speed_y):
        """Метод для динамічного оновлення вертикальної швидкості."""
        self.speed_y = new_speed_y
