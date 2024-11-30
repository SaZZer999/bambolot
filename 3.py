import pygame
import sys
import random
from player import Player
from meteor import Meteor
from flame1 import Flame
from gold import Gold
from life import Life
# Ініціалізація Pygame та музичного модуля
pygame.init()
pygame.mixer.init()

# Налаштування екрана
window_width = 720
window_height = 1280
window = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)
font_small = pygame.font.Font(None, 24)  # Менший шрифт

score = 0  # Початковий рахунок

# Групи спрайтів для метеорів та золота
meteor_group = pygame.sprite.Group()
gold_group = pygame.sprite.GroupSingle()
life_group = pygame.sprite.Group()


# Створення екземпляра життя та додавання його до групи
life = Life(100, 0)  # Початкова позиція життя (x=100, y=0)
life_group.add(life)

survival_timer = pygame.time.get_ticks()  # Відстеження початку гри

                                                 #НАЛАШТУВАННЯ ГРИ

# Кольори для кнопок та тексту
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)


# Таймер для повернення в меню
game_over_start_time = None  # Час початку відображення Game Over
game_over_delay = 3000       # Затримка в мілісекундах (3 секунди)

# Ігрові налаштування
background_speed = 2
stars_speed = 2.5
meteor_speed = 2
gold_speed = 2
game_state = "menu"


# Початкові позиції для фону та зірок
y1, y2 = 0, -window_height
y_stars1, y_stars2 = 0, -window_height


# Налаштування секцій для появи
section_width = window_width // 4
meteor_spawn_interval = 4000  # Інтервал для появи метеорів (мс)
gold_spawn_interval = meteor_spawn_interval // 2  # Золото з'являється в 2 рази частіше
last_meteor_spawn_time = pygame.time.get_ticks()
last_gold_spawn_time = pygame.time.get_ticks()



                                             #ЗАВАНТАЖЕННЯ МЕДІА
# Завантаження фону меню
menu_background = pygame.image.load("image/menu/menu.png").convert()
menu_background = pygame.transform.scale(menu_background, (window_width, window_height))


# Новий розмір для кнопок
button_width = 720
button_height = 1280

# Завантаження і масштабування зображень кнопок
buttons = {
    "play": {
        "hover": pygame.transform.scale(pygame.image.load("image/menu/play_hover.png").convert_alpha(), (button_width, button_height)),
        "rect": pygame.Rect(0, 0, button_width, button_height)  # Розташування кнопки
    },
    "score": {
        "hover": pygame.transform.scale(pygame.image.load("image/menu/score_hover.png").convert_alpha(), (button_width, button_height)),
        "rect": pygame.Rect(0, 0, button_width, button_height)  # Розташування кнопки
    },
    "settings": {
        "hover": pygame.transform.scale(pygame.image.load("image/menu/settings_hover.png").convert_alpha(), (button_width, button_height)),
        "rect": pygame.Rect(0, 0, button_width, button_height)  # Розташування кнопки
    },
    "exit": {
        "hover": pygame.transform.scale(pygame.image.load("image/menu/exit_hover.png").convert_alpha(), (button_width, button_height)),
        "rect": pygame.Rect(0, 0, button_width, button_height)  # Розташування кнопки
    },
}




# Оновлюємо розміри rect на основі реальних розмірів зображень
for button_name, button_data in buttons.items():
    hover_image = button_data["hover"]
    button_data["rect"].width = hover_image.get_width()
    button_data["rect"].height = hover_image.get_height()

for button_name, button_data in buttons.items():
    hover_image = button_data["hover"]
    # Завантаження фонової музики
pygame.mixer.music.load("sounds/music/background.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)

# Завантаження фонових зображень
background1 = pygame.image.load("image/background/background11.png").convert()
background2 = pygame.image.load("image/background/background22.png").convert()
stars = pygame.image.load("image/background/stars.png").convert_alpha()
stars.set_alpha(235)
meteor_images = [
    pygame.image.load("image/enemi/meteor1.png").convert_alpha(),
    pygame.image.load("image/enemi/meteor2.png").convert_alpha(),
    pygame.image.load("image/enemi/meteor3.png").convert_alpha(),
    pygame.image.load("image/enemi/meteor4.png").convert_alpha()
]
gold_image = pygame.image.load("image/enemi/gold.png").convert_alpha()

# Зображення для полум'я
flame_no_move_images = [
    r"C:\Users\maksy\PycharmProjects\Game\image\flame\no_move\flame.png",
    r"C:\Users\maksy\PycharmProjects\Game\image\flame\no_move\flame1.png",
    r"C:\Users\maksy\PycharmProjects\Game\image\flame\no_move\flame2.png",
    r"C:\Users\maksy\PycharmProjects\Game\image\flame\no_move\flame3.png"
]
flame_move_start_images = [
    r"C:\Users\maksy\PycharmProjects\Game\image\flame\move_start\flame4.png",
    r"C:\Users\maksy\PycharmProjects\Game\image\flame\move_start\flame5.png",
    r"C:\Users\maksy\PycharmProjects\Game\image\flame\move_start\flame6.png"
]
flame_move_images = [
    r"C:\Users\maksy\PycharmProjects\Game\image\flame\move\flame7.png",
    r"C:\Users\maksy\PycharmProjects\Game\image\flame\move\flame8.png",
    r"C:\Users\maksy\PycharmProjects\Game\image\flame\move\flame9.png",
    r"C:\Users\maksy\PycharmProjects\Game\image\flame\move\flame10.png"
]

# Завантаження зображень
life_icon = pygame.image.load("image/life/life.png").convert_alpha()
life_icon = pygame.transform.scale(life_icon, (30, 30))  # Зменшене зображення

# Групи спрайтів для метеорів та золота
meteor_group = pygame.sprite.Group()
gold_group = pygame.sprite.GroupSingle()#Створення об'єкта гравця
player = Player(285, 840, "image/player/player1.png")
# Полум’я позаду гравця
flames = [
    Flame(player.x + 15, player.y + player.image.get_height() - 75, flame_no_move_images, flame_move_start_images, flame_move_images),
    Flame(player.x + player.image.get_width() - 35, player.y + player.image.get_height() - 75, flame_no_move_images, flame_move_start_images, flame_move_images)
    ]
# Квадрат зони активності для підсвічування
hover_zones = {
    "play": pygame.Rect(215, 590, 300, 48),      # Активна зона для кнопки "play"
    "score": pygame.Rect(215, 668, 300, 48),   # Активна зона для кнопки "score"
    "settings": pygame.Rect(215, 745, 300, 48),# Активна зона для кнопки "settings"
    "exit": pygame.Rect(215, 820, 300, 48),    # Активна зона для кнопки "exit"
}



                                                   #ФУНКЦІЇ

# Лінії між секціями
def draw_sections():
    for i in range(1, 4):  # Лінії між секціями
        x = i * section_width
        pygame.draw.line(window, (255, 0, 0), (x, 0), (x, window_height), 2)

# Функція створення метеорів
def create_meteors():
    global meteor_speed
    possible_sections = [0, 1, 2, 3]  # Усі секції
    num_sections = random.randint(1, 2)  # Випадкове число секцій (1 або 2)
    selected_sections = random.sample(possible_sections, num_sections)

    for section in selected_sections:
        meteor_image = random.choice(meteor_images)
        x = section * section_width + section_width // 2 - meteor_image.get_width() // 2  # Центрування
        x += 50
        y = -100

        # Перевірка, щоб метеорит не з'явився на тих самих координатах, що й золото
        if gold_group.sprite and gold_group.sprite.rect.collidepoint(x, y):
            continue  # Пропускаємо створення метеорита на цій секції

        meteor = Meteor(meteor_image, x, y, 0, meteor_speed, window_height)
        meteor.speed = meteor_speed  # Встановлюємо швидкість метеорита
        meteor_group.add(meteor)


# Функція створення золота
def create_gold():
    global gold_speed
    possible_sections = [0, 1, 2, 3]  # Усі секції
    section = random.choice(possible_sections)

    # Перевірка, щоб золото не з'явилося на тих самих координатах, що й метеорит
    if any(meteor.rect.collidepoint(section * section_width + section_width // 2, -100) for meteor in meteor_group):
        return  # Не створюємо золото, якщо координати співпадають з метеоритом

    x = section * section_width + section_width // 2 - gold_image.get_width() // 2  # Центрування
    y = -100

    # Перевірка, щоб золото не співпало за координатами з метеоритом
    if any(meteor.rect.collidepoint(x, y) for meteor in meteor_group):
        return  # Не створюємо золото, якщо координати співпадають

    gold = Gold(gold_image, x, y, 0, gold_speed, window_height)
    gold.speed = gold_speed  # Встановлюємо швидкість золота
    gold_group.add(gold)


        # Функція створення фону
def draw_background():
    global y1, y2, y_stars1, y_stars2
    y1 += background_speed
    y2 += background_speed
    y_stars1 += stars_speed
    y_stars2 += stars_speed

        # Рух фону
    if y1 >= window_height:
        y1 = -window_height
    if y2 >= window_height:
        y2 = -window_height
    if y_stars1 >= window_height:
        y_stars1 = -window_height
    if y_stars2 >= window_height:
        y_stars2 = -window_height
    window.blit(background1, (0, y1))
    window.blit(background2, (0, y2))
    window.blit(stars, (0, y_stars1))
    window.blit(stars, (0, y_stars2))

# Функція створення тексту
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Функція для перевірки перетину
def is_overlapping(rect, groups):
    for group in groups:
        for sprite in group:
            if rect.colliderect(sprite.rect):
                return True
    return False


# Ініціалізація таймерів
last_speed_increase_time = pygame.time.get_ticks()
survival_timer = pygame.time.get_ticks()




# Основний цикл
def main():
    global game_state, last_meteor_spawn_time, last_gold_spawn_time
    global meteor_speed, background_speed, stars_speed, gold_speed, score
    global last_speed_increase_time, survival_timer

    while True:
        handle_events()      # Обробка подій
        update_game_state()  # Оновлення стану гри
        if game_state == "menu":
            draw_menu()
        elif game_state == "playing":
            update_game_logic()
            draw_game()
        elif game_state == "records":
            draw_records()
        elif game_state == "game_over":
            draw_game_over()

        pygame.display.flip()
        clock.tick(60)

# Оновлення стану гри
def update_game_state():
    global game_state, game_over_start_time

    if game_state == "game_over":
        if game_over_start_time is None:  # Ініціалізуємо таймер при вході в Game Over
            game_over_start_time = pygame.time.get_ticks()

        # Перевіряємо, чи минула затримка
        if pygame.time.get_ticks() - game_over_start_time > game_over_delay:
            game_state = "menu"
            game_over_start_time = None  # Скидаємо таймер

# Обробка подій
def handle_events():
    global game_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_state == "menu":
            handle_menu_events(event)
        elif game_state == "game_over":
            handle_game_over_events(event)

# Обробка подій для Game Over
def handle_game_over_events(event):
    global game_state
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_m:  # Натиснення 'M' для повернення в меню
            game_state = "menu"
        elif event.key == pygame.K_q:  # Натиснення 'Q' для виходу з гри
            pygame.quit()
            sys.exit()

# Обробка подій меню
def handle_menu_events(event):
    global game_state
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos
        for button_name, button_data in buttons.items():
            if hover_zones[button_name].collidepoint(mouse_pos):
                if button_name == "play":
                    game_state = "playing"
                elif button_name == "score":
                    game_state = "records"
                elif button_name == "settings":
                    game_state = "settings"
                elif button_name == "exit":
                    pygame.quit()
                    sys.exit()

# Оновлення логіки гри
def update_game_logic():
    global game_state, last_meteor_spawn_time, last_gold_spawn_time
    global meteor_speed, background_speed, stars_speed, gold_speed, score
    global last_speed_increase_time, survival_timer

    # Клавіші для руху гравця
    keys = pygame.key.get_pressed()
    is_moving = keys[pygame.K_UP]

    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()
    if keys[pygame.K_DOWN]:
        player.move_down()
    if keys[pygame.K_UP]:
        player.move_up()
        player.is_boosting = True  # Активувати прискорення
    else:
        player.is_boosting = False  # Відключити прискорення


    # Оновлення полум'я
    for flame in flames:
        if flames.index(flame) == 0:  # Перший вогонь
            flame.x = player.x + 10
            flame.y = player.y + player.image.get_height() - 50
        else:  # Другий вогонь
            flame.x = player.x + player.image.get_width() -200
            flame.y = player.y + player.image.get_height() - 50
        flame.update(is_moving)

    # Обмеження руху гравця в межах екрану
    player.x = max(30, min(player.x, window_width - 30 - player.image.get_width()))
    player.y = max(650, min(player.y, 1100 - player.image.get_height()))


    # Оновлення очок
    current_time = pygame.time.get_ticks()
    if current_time - survival_timer > 1000:  # Щосекунди додаємо очки
        score += 1
        survival_timer = current_time
        if keys[pygame.K_UP]:
            score += 1

    # Додаємо очки за зібране золото
    if pygame.sprite.spritecollide(player, gold_group, True, pygame.sprite.collide_mask):
        score += 10


    # Створення нових об'єктів
    if current_time - last_meteor_spawn_time > meteor_spawn_interval:
        create_meteors()
        last_meteor_spawn_time = current_time

    if current_time - last_gold_spawn_time > gold_spawn_interval and not gold_group.sprite:
        create_gold()
        last_gold_spawn_time = current_time

    # Рандомне появлення життя
    if random.randint(1, 100) == 0.1:  # Імовірність 1%
        x = random.randint(0, window_width - 50)  # Рандомне розташування по x
        life = Life(x, 0)
        life_group.add(life)

    # Поступове збільшення швидкості
    if current_time - last_speed_increase_time > 5000:
        meteor_speed += 0.0035
        background_speed += 0.0002
        stars_speed += 0.0008
        gold_speed += 0.0035
        last_speed_increase_time = current_time
    if player.is_boosting:
        background_speed = 4  # Прискорити фон
        stars_speed = 5  # Прискорити зірки
        meteor_speed = 8  # Прискорити метеори
        gold_speed = 8  # Прискорити золото
    else:
        background_speed = 2  # Повернути звичайну швидкість фону
        stars_speed = 2.5
        meteor_speed = 2
        gold_speed = 2

    # Оновлення швидкості всіх існуючих метеоритів і золота
    # Оновлення швидкості всіх існуючих метеоритів і золота
    for meteor in meteor_group:
        meteor.set_speed(meteor_speed)  # Оновлюємо швидкість всіх метеоритів
    for gold in gold_group:
        gold.speed = gold_speed  # Постійно синхронізуємо швидкість золота із глобальною змінною

    # Оновлення метеоритів і золота
    meteor_group.update()
    gold_group.update()
    life_group.update()


    # Перевірка колізій
    if pygame.sprite.spritecollide(player, meteor_group, True, pygame.sprite.collide_mask):
        game_over()
    for meteor in meteor_group:
        meteor.rect.y += meteor_speed  # Використовуй глобальну змінну швидкості
    for gold in gold_group:
        gold.rect.y += gold_speed  # Використовуй глобальну змінну швидкості
    if pygame.sprite.spritecollide(player, life_group, True):  # True видаляє об'єкт життя після зіткнення
        player.lives += 1
        print(f"Життя: {player.lives}")


# Малювання гри
def draw_game():
    draw_background()
    draw_sections()
    for flame in flames:
        flame.draw(window)
    player.draw(window)
    life_group.draw(window)
    meteor_group.draw(window)
    gold_group.draw(window)
    draw_text(f"Очки: {score}", font, WHITE, window, 150, 200)

for i in range(player.lives):
    window.blit(life_icon, (100, 300))  # Іконки відображаються у верхньому лівому куті

# Малювання меню
def draw_menu():
    window.blit(menu_background, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    for button_name, button_data in buttons.items():
        active_zone = hover_zones[button_name]
        if active_zone.collidepoint(mouse_pos):
            window.blit(button_data["hover"], button_data["rect"].topleft)

# Малювання рекордів
def draw_records():
    window.fill(GRAY)
    draw_text("Рекорди", font, WHITE, window, window_width // 2, 150)

# Малювання Game Over
def draw_game_over():
    window.fill(GRAY)
    draw_text("Game Over", font, WHITE, window, window_width // 2, window_height // 2)
    draw_text(f"Ваш результат: {score}", font, WHITE, window, window_width // 2, window_height // 2 + 50)
    draw_text("Повернення в меню...", font_small, WHITE, window, window_width // 2, window_height // 2 + 100)


# Функція game over
def game_over():
    global game_state, score
    window.fill(GRAY)
    draw_text(f"Ваш результат: {score}", font, WHITE, window, window_width // 2, window_height // 2 + 50)
    draw_text("Game Over", font, WHITE, window, window_width // 2, window_height // 2)
    pygame.display.flip()

    # Неблокуюча затримка через таймер
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 2000:  # 2 секунди
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    score = 0  # Скидання очок
    game_state = "menu"
    meteor_group.empty()  # Очищення метеоритів
    gold_group.empty()

if __name__ == "__main__":
    main()