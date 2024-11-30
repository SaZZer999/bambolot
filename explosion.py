import pygame
import os

# Група для всіх вибухів
explosions_group = pygame.sprite.Group()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Завантаження всіх кадрів анімації вибуху
        self.frames = []
        for i in range(1, 10):
            image_path = os.path.join("image", "explosion", f"explosion{i}.png")
            self.frames.append(pygame.image.load(image_path).convert_alpha())

        self.index = 0
        self.image = self.frames[self.index]  # Перший кадр анімації
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Позиція вибуху
        self.animation_speed = 5  # Швидкість анімації
        self.counter = 0

    def update(self):
        """ Оновлює стан анімації вибуху. """
        self.counter += 1
        if self.counter >= self.animation_speed:
            self.counter = 0
            self.index += 1
            if self.index < len(self.frames):
                self.image = self.frames[self.index]
            else:
                self.kill()  # Видалення вибуху після завершення анімації
