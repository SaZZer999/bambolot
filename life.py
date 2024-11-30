import pygame

# Параметри гри
life_speed = 4  # Швидкість руху життя
window_width, window_height = 720, 1280  # Розмір вікна

class Life(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Завантаження зображення життя
        self.image = pygame.image.load("image/life/life.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        # Рух життя вниз
        self.rect.y += life_speed

        # Якщо об'єкт вийшов за межі екрана, видаляємо його
        if self.rect.top > window_height:
            self.kill()
