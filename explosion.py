import pygame
import os

# Група для всіх вибухів
explosions_group = pygame.sprite.Group()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_y=0):
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
        self.animation_speed = 4  # Швидкість анімації
        self.counter = 0
        self.speed_y = speed_y  # Швидкість руху вибуху (вертикальна)

    def update(self):
        """Оновлює стан анімації вибуху та переміщує вибух."""
        # Анімація вибуху
        self.counter += 1
        if self.counter >= self.animation_speed:
            self.counter = 0
            self.index += 1
            if self.index < len(self.frames):
                self.image = self.frames[self.index]
            else:
                self.kill()  # Видалення вибуху після завершення анімації

        # Рух вибуху вниз із тією ж швидкістю, що й метеорит
        self.rect.y += self.speed_y
