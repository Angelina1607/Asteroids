import pygame
import time

pygame.init()

# Глобальные переменные
window_width = 800
window_height = 600
fon = 'background.jpg'  # изображение должно быть в том же каталоге, что и код на питоне

# Запуск
window = pygame.display.set_mode([window_width, window_height])  # создание окна
pygame.display.set_caption("Игра v1.0")  # установка надписи окна программы

speed = 0  # текущая скорость перемещения
sdvig_fona = 0  # сдвиг фона

img1 = pygame.image.load(fon)  # загрузка фона игры из файла
back_fon = pygame.transform.scale(img1, (window_width, window_height))  # размеры картинки back - те же, что и у окна

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # пришло ли событие нажатия на крестик
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speed = 5  # движение влево
            if event.key == pygame.K_RIGHT:
                speed = -5  # движение вправо
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                speed = 0  # останавливаем движение при отпускании клавиши

    sdvig_fona = (sdvig_fona + speed) % window_width
    window.blit(back_fon, (sdvig_fona, 0))
    if sdvig_fona != 0:
        window.blit(back_fon, (sdvig_fona - window_width, 0))  # рисуем такой же фон слева от сдвига

    pygame.display.update()  # обновление содержимого окна
    time.sleep(0.02)

pygame.quit()  # закрыть окно крестиком
