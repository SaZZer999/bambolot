class PickupAnimation(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.frames = []  # Кадри анімації
        self.frames.append(pygame.transform.scale(image, (50, 50)))  # Початковий розмір
        self.frames.append(pygame.transform.scale(image, (40, 40)))  # Зменшений розмір
        self.frames.append(pygame.transform.scale(image, (30, 30)))  # Ще менший
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 5
        self.counter = 0

    def update(self):
        self.counter += 1
        if self.counter >= self.animation_speed:
            self.counter = 0
            self.index += 1
            if self.index < len(self.frames):
                self.image = self.frames[self.index]
            else:
                self.kill()  # Видалення після завершення анімації
