import pygame
import random



class Gold(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed_x, speed_y, window_height):
        super().__init__()

        # Масштабування зображення золота
        desired_width = 90
        desired_height = 90
        self.original_image = pygame.transform.scale(image, (desired_width, desired_height))
        self.image = self.original_image
        self.mask = pygame.mask.from_surface(self.original_image)

        # Позиція та швидкість
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.window_height = window_height

    def update(self):
        # Рух золота
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

        # Оновлення маски для обертання (опціонально)
        self.mask = pygame.mask.from_surface(self.image)

        # Видалення золота, якщо воно виходить за межі екрана
        if self.rect.y > self.window_height:
            self.kill()

    def set_speed(self, new_speed_y):
        """Метод для динамічного оновлення вертикальної швидкості."""
        self.speed_y = new_speed_y