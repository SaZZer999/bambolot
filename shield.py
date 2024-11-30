import pygame

# Параметри гри
speed = 4
pygame.init()
screen = pygame.display.set_mode((720, 1280))  # Приклад розміру вікна
window_height = 1280
window_width  =720
# Створення групи для щитів
shield_group = pygame.sprite.Group()

class Shield(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Завантаження зображення щита
        self.image = pygame.image.load("image/shield/shield.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.window_height = window_height
        self.window_width = window_width

    def update(self):
        # Рух щита вниз
        self.rect.y += self.speed

        # Якщо щит вийшов за межі вікна, видаляємо його
        if self.rect.top > window_height:
            self.kill()

# Створення екземпляра щита і додавання його в групу
# Наприклад, додаємо щит у позицію (100, 0)
shield = Shield(100, 0)
shield_group.add(shield)
