import pygame
import sys

# Инициализация Pygame
pygame.init()

# Глобальные переменные
window_width = 800
window_height = 600
background_image_path = 'background.jpg'  # изображение должно быть в том же каталоге, что и код на питоне

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, filename, hero_x=100, hero_y=250):
        super().__init__()
        self.image = pygame.image.load(filename)  # загрузка героя из файла
        self.rect = self.image.get_rect()
        self.rect.x = hero_x
        self.rect.y = hero_y
        self.speed = 5  # скорость движения игрока
        self.x_speed = 0  # скорость по оси X
        self.y_speed = 0  # скорость по оси Y

    def update(self):
        # Обновление позиции игрока на основе скорости
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        # Ограничение по границам окна
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > window_width:
            self.rect.right = window_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > window_height:
            self.rect.bottom = window_height

# Класс стрелы
class Arrow(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.image.load('Arrow.png')  # Укажите путь к изображению стрелы
        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center  # Начальная позиция стрелы - центр игрока
        self.speed = 10  # скорость стрелы

    def update(self):
        self.rect.x += self.speed  # Двигаем стрелу вправо
        if self.rect.x > window_width:  # Удаляем стрелу, если она выходит за границы
            self.kill()

# Класс дополнительного спрайта
class Enemy(pygame.sprite.Sprite):
    def __init__(self, filename, hero_x, hero_y):
        super().__init__()
        self.image = pygame.image.load(filename)  # загрузка врага из файла
        self.rect = self.image.get_rect()
        self.rect.x = hero_x
        self.rect.y = hero_y
        self.speed = 2  # скорость врага

    def update(self):
        self.rect.x -= self.speed  # Двигаем врага влево
        if self.rect.x < 0:  # Если выходит за границы, удаляем
            self.kill()

# Функция для управления движением игрока
def handle_keys(player):
    keys = pygame.key.get_pressed()
    player.x_speed = 0
    player.y_speed = 0
    if keys[pygame.K_LEFT]:
        player.x_speed = -player.speed
    if keys[pygame.K_RIGHT]:
        player.x_speed = player.speed
    if keys[pygame.K_UP]:
        player.y_speed = -player.speed
    if keys[pygame.K_DOWN]:
        player.y_speed = player.speed

# Создание окна
window = pygame.display.set_mode([window_width, window_height])
pygame.display.set_caption("Игра v1.0")

# Загрузка фонового изображения и масштабирование
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(background_image, (window_width, window_height))

# Создание экземпляров игрока и врагов
player_image_path = 'Player.png'  # Укажите путь к изображению игрока
player = Player(player_image_path)

enemy_image_path = 'Enemy.png'  # Укажите путь к изображению врага
enemy1 = Enemy(enemy_image_path, 800, 200)  # Создаем первого врага
enemy2 = Enemy(enemy_image_path, 800, 400)  # Создаем второго врага

# Группа спрайтов
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy1)
all_sprites.add(enemy2)

# Переменные для движения фона
shift_background = 0  # сдвиг фона
arrows = pygame.sprite.Group()  # Группа для стрел

# Главный игровой цикл
# Главный игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Проверка нажатия на крестик
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # При нажатии пробела
                arrow = Arrow(player)  # Создаем стрелу
                arrows.add(arrow)  # Добавляем стрелу в группу стрел
                all_sprites.add(arrow)  # Добавляем стрелу в группу спрайтов

    # Обработка клавиш
    handle_keys(player)

    # Обновление спрайтов
    all_sprites.update()
    arrows.update()  # Обновление стрел

    # Проверка на коллизии между стрелами и врагами
    for arrow in arrows:
        hits = pygame.sprite.spritecollide(arrow, all_sprites, False)
        for hit in hits:
            if isinstance(hit, Enemy):  # Если столкновение со спрайтом врага
                arrow.kill()  # Удаляем стрелу
                hit.kill()  # Удаляем врага

    # Обновление сдвига фона
    shift_background = (shift_background - player.x_speed) % window_width

    # Отрисовка фона
    window.blit(background_image, (shift_background, 0))  # основной фон
    if shift_background != 0:
        window.blit(background_image, (shift_background - window_width, 0))  # фон слева от сдвига

    # Отрисовка всех спрайтов
    all_sprites.draw(window)

    # Обновление экрана
    pygame.display.update()  # обновление содержимого окна
    pygame.time.delay(20)  # небольшая задержка для управления FPS

pygame.quit()  # закрыть окно
sys.exit()
