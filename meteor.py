import pygame
import random

class Meteor(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed_x, speed_y, window_height):
        super().__init__()

        # Масштабоване зображення
        self.original_image = pygame.transform.scale(image, (80, 80))  # Масштабування зображення
        self.image = self.original_image
        self.mask = pygame.mask.from_surface(self.original_image)  # Маска для перевірки зіткнень

        # Позиція та швидкість
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = speed_x  # Швидкість по горизонталі
        self.speed_y = speed_y  # Швидкість по вертикалі
        self.window_height = window_height

        # Обертання
        #self.rotation_angle = 0
        #self.rotation_direction = random.choice([-1, 1])  # Напрямок обертання (вліво або вправо)
        #self.rotation_speed = random.uniform(0.05, 0.1) * self.rotation_direction  # Швидкість обертання

    def update(self):
        # Рух метеорита
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

        # Обертання метеорита
        #self.rotation_angle += self.rotation_speed
        #self.image = pygame.transform.rotate(self.original_image, self.rotation_angle)

        # Зберігаємо положення після обертання
        #self.rect = self.image.get_rect(center=self.rect.center)

        # Оновлення маски після обертання (опціонально)
        #self.mask = pygame.mask.from_surface(self.image)

        # Видалення метеорита, якщо він виходить за межі екрана
        if self.rect.y > self.window_height:
            self.kill()

    def set_speed(self, new_speed_y):
        """Метод для динамічного оновлення вертикальної швидкості."""
        self.speed_y = new_speed_y
