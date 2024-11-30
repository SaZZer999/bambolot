import pygame

class Flame:
    def __init__(self, x, y, no_move_images, move_start_images, move_images):
        self.x = x
        self.y = y
        self.no_move_images = [pygame.image.load(img).convert_alpha() for img in no_move_images]
        self.move_start_images = [pygame.image.load(img).convert_alpha() for img in move_start_images]
        self.move_images = [pygame.image.load(img).convert_alpha() for img in move_images]
        self.current_images = self.no_move_images  # За замовчуванням - анімація стояння
        self.image_index = 0
        self.animation_speed = 0.1
        self.frame_timer = 0
        self.is_moving = False
        self.start_move = False

    def update(self, is_moving):
        self.is_moving = is_moving

        # Вибір типу анімації
        if not self.is_moving:
            self.current_images = self.no_move_images
            self.image_index = 0  # Повертаємось до першого кадру
            self.start_move = False  # Скидаємо старт руху
        elif not self.start_move:
            self.current_images = self.move_start_images
            if self.image_index >= len(self.move_start_images) - 1:  # Закінчили старт анімацію
                self.start_move = True
                self.image_index = 0
        else:
            self.current_images = self.move_images

        # Оновлення кадру
        self.frame_timer += self.animation_speed
        if self.frame_timer >= 1:
            self.frame_timer = 0
            self.image_index = (self.image_index + 1) % len(self.current_images)

    def draw(self, window):
        if self.current_images:
            image = self.current_images[int(self.image_index)]
            window.blit(image, (self.x, self.y))
