import pygame
import sys
import random
from player import Player
from meteor import Meteor
from flame1 import Flame
from gold import Gold
from life import Life
from explosion import Explosion, explosions_group

# Ініціалізація Pygame та музичного модуля
pygame.init()
pygame.mixer.init()

# Налаштування екрана
window_width = 720
window_height = 1280
window = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)
font_small = pygame.font.Font(None, 26)  # Менший шрифт
font_big = pygame.font.Font(None, 60)
score = 0  # Початковий рахунок

# Групи спрайтів для метеорів та золота
meteor_group = pygame.sprite.Group()
gold_group = pygame.sprite.GroupSingle()
life_group = pygame.sprite.Group()
explosions_group = pygame.sprite.Group()



survival_timer = pygame.time.get_ticks()  # Відстеження початку гри

                                                 #НАЛАШТУВАННЯ ГРИ

# Кольори для кнопок та тексту
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)


# Таймер для повернення в меню
game_over_start_time = None  # Час початку відображення Game Over
game_over_delay = 4000       # Затримка в мілісекундах (3 секунди)

# Ігрові налаштування
background_speed = 2
stars_speed = 2.5
meteor_speed = 3
gold_speed = 3
life_speed = 3
game_state = "menu"

# Базові швидкості (для поступового збільшення)
base_background_speed = background_speed
base_stars_speed = stars_speed
base_meteor_speed = meteor_speed
base_gold_speed = gold_speed
base_life_speed = life_speed

boost_multiplier = 2  # Множник для прискорення

# Початкові позиції для фону та зірок
y1, y2 = 0, -window_height
y_stars1, y_stars2 = 0, -window_height


# Налаштування секцій для появи
section_width = window_width // 5
meteor_spawn_interval = 2000  # Інтервал для появи метеорів (мс)
gold_spawn_interval = meteor_spawn_interval // 0.2  # Золото з'являється в 2 рази частіше
last_meteor_spawn_time = pygame.time.get_ticks()
last_gold_spawn_time = pygame.time.get_ticks()



                                             #ЗАВАНТАЖЕННЯ МЕДІА
# Завантаження фону меню
menu_background = pygame.image.load("image/menu/menu.png").convert()
menu_background = pygame.transform.scale(menu_background, (window_width, window_height))
# Завантаження фону для екрану "Game Over"
game_over_background = pygame.image.load("image/menu/game_over/game_over.png").convert()
game_over_background = pygame.transform.scale(game_over_background, (window_width, window_height))  # Змінюємо розмір



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

explosion_sound = pygame.mixer.Sound("sounds/explosion_sound/explosion_sound.mp3")
explosion_sound.set_volume(0.5)

gold_pickup_sound = pygame.mixer.Sound("sounds/pickup/gold_pickup.wav")
gold_pickup_sound.set_volume(0.5)

healh_pickup_sound = pygame.mixer.Sound("sounds/pickup/healh_pickup.mp3")
#healh_pickup_sound.set_volume(0.5)


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
life_icon = pygame.transform.scale(life_icon, (60, 60))  # Зменшене зображення

# Завантаження фонів
menu_score_background = pygame.image.load("image/menu/score/menu_score_background.png").convert()
menu_score_background = pygame.transform.scale(menu_score_background, (window_width, window_height))

menu_settings_background = pygame.image.load("image/menu/settings/menu_settings_background.png").convert()
menu_settings_background = pygame.transform.scale(menu_settings_background, (window_width, window_height))

score_exit_hover = pygame.image.load("image/menu/settings/settings_exit_hover.png").convert_alpha()
score_exit_hover = pygame.transform.scale(score_exit_hover, (window_width, window_height))

# Координати кнопки виходу
exit_button_rect = pygame.Rect(215, 1090, 300, 48)

#Створення об'єкта гравця
player = Player(285, 840, "image/player/player1.png")
player.lives = 3  # Початкова кількість життів
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
#def draw_sections():
#    for i in range(1, 5):  # Лінії між секціями
#        x = i * section_width
#        pygame.draw.line(window, (255, 0, 0), (x, 0), (x, window_height), 2)

# Функція створення метеорів
def create_meteors():
    global meteor_speed
    possible_sections = [0, 1, 2, 3, 4]  # Усі секції
    # Визначаємо максимальну кількість метеоритів залежно від очок
    if score < 100:
        max_meteors = 1
    elif score < 200:
        max_meteors = 2
    elif score < 350:
        max_meteors = 3
    else:
        max_meteors = 4  # Після 350 очок максимум 4 метеорити

    # Випадковий вибір секцій для метеоритів, залишаючи одну вільну
    selected_sections = random.sample(possible_sections, max_meteors)

    for section in selected_sections:
        meteor_image = random.choice(meteor_images)
        x = section * section_width + section_width // 2 - meteor_image.get_width() // 2  # Центрування
        x += 50
        y = -100  # Початкова координата Y (над екраном)

        # Перевірка, щоб метеорит не з'явився там, де є золото
        if gold_group.sprite and gold_group.sprite.rect.collidepoint(x, y):
            continue  # Пропустити секцію, якщо золото є на цих координатах

        # Створення об'єкта метеорита
        meteor = Meteor(meteor_image, x, y, 0, meteor_speed, window_height)
        meteor.speed = meteor_speed  # Встановлення швидкості метеорита
        meteor_group.add(meteor)



# Функція створення золота
def create_gold():
    global gold_speed
    possible_sections = [0, 1, 2, 3, 4]  # Усі секції
    section = random.choice(possible_sections)

    # Перевірка, щоб золото не з'явилося на тих самих координатах, що й метеорит
    if any(meteor.rect.collidepoint(section * section_width + section_width // 2, -100) for meteor in meteor_group):
        return  # Не створюємо золото, якщо координати співпадають з метеоритом

    x = section * section_width + section_width // 2 - gold_image.get_width() // 2  # Центрування
    y = -100
    x += 350

    # Перевірка, щоб золото не співпало за координатами з метеоритом
    if any(meteor.rect.collidepoint(x, y) for meteor in meteor_group):
        return  # Не створюємо золото, якщо координати співпадають

    gold = Gold(gold_image, x, y, 0, gold_speed, window_height)
    gold.speed = gold_speed  # Встановлюємо швидкість золота
    gold_group.add(gold)

# Функція створення життя
def create_life(score):
    global life_speed
    # Список очок, при яких життя має з'явитися
    life_spawn_points = [95, 195, 345]

    # Перевірка: створюємо життя лише якщо є відповідна кількість очок і немає іншого життя на екрані
    if score in life_spawn_points and len(life_group) < 1:
        section = random.randint(0, 4)  # Рандомний вибір секції
        x = section * section_width + section_width // 2 - 40  # Центруємо у секції (ширина картинки ~80px)
        y = -100  # Початкове розташування вище екрана

        # Перевірка, щоб життя не співпало за координатами з метеоритом або золотом
        collision_found = False
        for meteor in meteor_group:
            if meteor.rect.collidepoint(x, y):  # Життя не може бути в одній точці з метеоритом
                collision_found = True
                break
        for gold in gold_group:
            if gold.rect.collidepoint(x, y):  # Життя не може бути в одній точці із золотом
                collision_found = True
                break

        if not collision_found:  # Якщо не знайдено колізій, додаємо життя
            life = Life(x, y, speed_y=life_speed, window_height=window_height)
            life_group.add(life)

#Метод для динамічного оновлення вертикальної швидкості."""
def set_speed(self, new_speed_y):
    self.speed_y = new_speed_y
    print(f"Life object speed updated to: {new_speed_y}")  # Додано для перевірки

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

#Функція для відображення екрана рекордів
def draw_records():
    global window

    # Відображення фону
    window.blit(menu_score_background, (0, 0))

    # Отримуємо координати миші
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Перевіряємо, чи мишка наведена на кнопку "Exit"
    if exit_button_rect.collidepoint(mouse_x, mouse_y):
        window.blit(score_exit_hover, (0, 0))  # Відображаємо підсвітку кнопки

#Функція для обробки подій на екрані рекордів
def handle_records_events():
    global game_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:  # Клік миші
            mouse_x, mouse_y = pygame.mouse.get_pos()
            print(f"Mouse clicked at: {mouse_x}, {mouse_y}")  # Діагностика кліку

            # Перевіряємо, чи мишка натиснута на кнопку виходу
            if exit_button_rect.collidepoint(mouse_x, mouse_y):
                print("Exit button clicked!")  # Діагностика для перевірки кнопки
                game_state = "menu"  # Змінюємо стан гри
                pygame.display.flip()  # Миттєве оновлення екрана
                print(f"Game state changed to: {game_state}")  # Перевірка стану
                return  # Припиняємо обробку подій, щоб уникнути дублювання



# Основний цикл
def main():
    global game_state, last_meteor_spawn_time, last_gold_spawn_time
    global meteor_speed, background_speed, stars_speed, gold_speed, score
    global last_speed_increase_time, survival_timer

    # Ініціалізація таймерів
    last_meteor_spawn_time = pygame.time.get_ticks()
    last_gold_spawn_time = pygame.time.get_ticks()
    last_speed_increase_time = pygame.time.get_ticks()

    while True:
        if game_state == "menu":
            draw_menu()
            handle_menu_events()  # Викликаємо функцію без аргументів
        elif game_state == "playing":
            update_game_logic()
            draw_game()
            create_life(score)
        elif game_state == "records":
            draw_records()
            handle_records_events()  # Викликаємо функцію для обробки подій рекордів
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
def handle_menu_events():
    global game_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
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
    global meteor_speed, background_speed, stars_speed, gold_speed, life_speed, score
    global last_speed_increase_time, survival_timer
    global base_background_speed, base_stars_speed, base_meteor_speed, base_gold_speed, base_life_speed

    current_time = pygame.time.get_ticks()
    # Клавіші для руху гравця
    keys = pygame.key.get_pressed()
    is_moving = keys[pygame.K_UP]

    if game_state == "game_over":
        return  # Якщо гра закінчена, нічого не оновлюється

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
    player.y = max(700, min(player.y, 1050 - player.image.get_height()))


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
        gold_pickup_sound.play()




    # Створення нових об'єктів
    if current_time - last_meteor_spawn_time > meteor_spawn_interval:
        create_meteors()
        last_meteor_spawn_time = current_time

    if current_time - last_gold_spawn_time > gold_spawn_interval and not gold_group.sprite:
        create_gold()
        last_gold_spawn_time = current_time

    # Рандомне створення об'єктів життя
    #if random.randint(1, 500) == 1:  # Імовірність 1%
    #    create_life()

    # Поступове збільшення швидкостей
    if current_time - last_speed_increase_time > 5000:
        base_background_speed += 0.0002
        base_stars_speed += 0.0008
        base_meteor_speed += 0.0035
        base_gold_speed += 0.0035
        base_life_speed += 0.0035
        last_speed_increase_time = current_time
        print(f"Life speed updated: {life_speed}")

    # Застосування швидкостей з урахуванням прискорення
    if player.is_boosting:
        background_speed = base_background_speed * boost_multiplier
        stars_speed = base_stars_speed * boost_multiplier
        meteor_speed = base_meteor_speed * boost_multiplier
        gold_speed = base_gold_speed * boost_multiplier
        life_speed = base_life_speed * boost_multiplier
    else:
        background_speed = base_background_speed
        stars_speed = base_stars_speed
        meteor_speed = base_meteor_speed
        gold_speed = base_gold_speed
        life_speed = base_life_speed

    # Оновлення швидкості всіх існуючих метеоритів
    for meteor in meteor_group:
        meteor.set_speed(meteor_speed)

    # Оновлення швидкості всіх існуючих золотих монет
    for gold in gold_group:
        gold.set_speed(gold_speed)

    # Оновлення швидкості всіх існуючих життів
    for life in life_group:
        life.set_speed(life_speed)  # Оновлюємо швидкість

    # Оновлення метеоритів і золота
    meteor_group.update()
    gold_group.update()
    life_group.update()
    explosions_group.update()

    # Перевірка колізій
    collided_meteor = pygame.sprite.spritecollide(player, meteor_group, True, pygame.sprite.collide_mask)
    if collided_meteor:  # Якщо є зіткнення
        for meteor in collided_meteor:
            # Визначаємо координати метеорита, що зіштовхнувся
            meteor_x, meteor_y = meteor.rect.center

            # Створюємо вибух у точці метеорита, передаючи його швидкість
            explosion_sound.play()
            explosion = Explosion(meteor_x, meteor_y, speed_y=meteor.speed_y)
            explosions_group.add(explosion)

        # Віднімаємо життя гравця
        player.lives -= 1
        print(f"Залишилось життів: {player.lives}")

        # Якщо життя закінчилися, переходимо до стану "game_over"
        if player.lives < 1:
            game_over()

    for meteor in meteor_group:
        meteor.rect.y += meteor_speed  # Використовуй глобальну змінну швидкості


    for gold in gold_group:
        gold.rect.y += gold_speed  # Використовуй глобальну змінну швидкості
    # Перевірка зіткнень гравця з життям
    if player.lives < 3:  # Перевірка, чи кількість життів не перевищує 3
        if pygame.sprite.spritecollide(player, life_group, True):  # True видаляє об'єкт після зіткнення

            player.lives += 1  # Додаємо життя
            print(f"Життя: {player.lives}")
            healh_pickup_sound.play()



# Малювання іконок життя у верхньому лівому куті
def draw_lives():
    for i in range(player.lives):  # Малюємо по кількості життів
        window.blit(life_icon, (40 + i * 50, 170))  # Відступ 35 пікселів між іконками

# Основна функція малювання
def draw_game():
    draw_background()
    life_group.draw(window)
    #draw_sections()
    for flame in flames:
        flame.draw(window)
    player.draw(window)
    meteor_group.draw(window)
    gold_group.draw(window)
    explosions_group.draw(window)
    draw_text(f"Очки: {score}", font, WHITE, window, 355, 200)
    draw_lives()  # Виклик функції для малювання іконок життя

# Малювання меню
def draw_menu():
    window.blit(menu_background, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    for button_name, button_data in buttons.items():
        active_zone = hover_zones[button_name]
        if active_zone.collidepoint(mouse_pos):
            window.blit(button_data["hover"], button_data["rect"].topleft)

# Малювання рекордів
# def draw_records():
    #     window.fill(GRAY)
#    draw_text("Рекорди55", font, WHITE, window, window_width // 2, 150)

# Функція game over
def game_over():
    global game_state, score, meteor_speed, lives , window
    global background_speed, stars_speed, base_meteor_speed, gold_speed,life_speed
    # Скидаємо швидкості до початкових значень
    background_speed = 2
    stars_speed = 2.5
    meteor_speed = 3
    gold_speed = 3
    life_speed = 3
    game_state = "game_over"

    # Відображаємо картинку Game Over на екрані
    window.blit(game_over_background, (0, 0))

    # Відображаємо текст
    draw_text(f"Ваш результат: {score}", font, WHITE, window, window_width // 2, window_height // 2 + 200)
    draw_text("Game Over", font_big, WHITE, window, window_width // 2, window_height // 2 + 100)
    draw_text("Повернення в меню...", font_small, WHITE, window, window_width // 2, window_height // 2 + 340)

    pygame.display.flip()

    # Неблокуюча затримка через таймер
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 2000:  # 2 секунди
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    # При закінченні гри
    score = 0  # Скидання очок
    meteor_group.empty()  # Очищення метеоритів
    gold_group.empty()  # Очищення золота
    life_group.empty()  # Очищення групи життя
    explosions_group.empty()

    # Скидаємо швидкості до початкових значень
    background_speed = 2
    stars_speed = 2.5
    meteor_speed = 3
    gold_speed = 3
    life_speed = 3
    game_state = "menu"  # Повернення в меню
    # Скидаємо кількість життів (припускаємо, що ви використовуєте змінну lives для життів)
    player.lives = 3  # Встановлюємо початкову кількість життів

    print(
        f"After reset: score={score}, meteor_speed={meteor_speed}, background_speed={background_speed}, stars_speed={stars_speed}, player_lives={player.lives}")
if __name__ == "__main__":
    main()