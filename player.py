import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x, self.y = x, y
        self.lives = 3  # Початкова кількість життів
        self.is_boosting = False

    def move_left(self):
        self.x -= 8
        self.rect.x = self.x

    def move_right(self):
        self.x += 8
        self.rect.x = self.x

    def move_up(self):
        self.y -= 5
        self.rect.y = self.y

    def move_down(self):
        self.y += 5
        self.rect.y = self.y

    def draw(self, window):
        window.blit(self.image, self.rect)

    def add_life(self):
        self.lives += 1  # Додати життя

    def lose_life(self):
        self.lives -= 1  # Зменшити життя
        if self.lives <= 0:
            print("Гра закінчена!")
            pygame.quit()
            exit()
