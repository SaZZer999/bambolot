import pygame
import random


class Gold(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed_x, speed_y, window_height):
        super().__init__()

        # Змінення розміру золота
        desired_width = 100  # Встановлюємо ширину зображення
        desired_height = 100  # Встановлюємо висоту зображення
        self.original_image = pygame.transform.scale(image, (
        desired_width, desired_height))  # Зберігаємо оригінальне зображення для обертання

        self.image = self.original_image  # Початкове зображення для відображення
        self.rect = self.image.get_rect(center=(x, y))  # Встановлюємо прямокутник об'єкта
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.rotation_angle = 0  # Початковий кут обертання

    # Випадковий вибір напрямку і швидкості обертання
        self.rotation_direction = random.choice([-1, 1])  # -1 для вліво, 1 для вправо
        self.rotation_speed = random.uniform(0.1, 0.05) * self.rotation_direction
        self.window_height = window_height

    def update(self):
        # Рух золота вниз
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

        # Обертання золота
        self.rotation_angle += self.rotation_speed
        self.image = pygame.transform.rotate(self.original_image, self.rotation_angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Перевірка, чи вийшоло золото за межі екрана
        if self.rect.y > self.window_height:
            self.kill()  # Видаляємо метеорит, якщо він вийшов за межі екрана
