import pygame
import random
import time
import sys
from pygame.locals import *

fps = 30
window_w, window_h = 800, 600       # Устанавливаем размер окна
block = 20       # Определяем базовый элемент блок размером 20Х20 пикселей, считаем, что это 1 квадратик
field_w = 20     # Определяем ширину игрового поля, оно равняется fields_w*block 
field_h = 25     # Аналогично предыдущей строке, только для высоты
side_move_time, down_move_time = 0.1, 0.1 # Параметры, которые определяют время перемещения объектов при сажатии клавиши
                            ## "Стрелка вниз" -- down_move_time, "стрелка влево или вправо" -- side_move_time
game_screen_Hpos = int((window_w -field_w*block)/2)    # Определяет размещение игрового поля по центру экрана
game_screen_Vpos = window_h - (field_h * block)        # Вертикальное смещение игрового поля

colors = ((0, 0, 225), (0, 225, 0), (225, 0, 0), (225, 225, 0))              # Синий, зеленый, красный, желтый
lightcolors = ((30, 30, 255), (50, 255, 50), (255, 30, 30), (255, 255, 30))  # Светло-синий, светло-зеленый, светло-красный, светло-желтый, создание "структуры" фигуры

white, gray, black  = (255, 255, 255), (185, 185, 185), (0, 0, 0)
board_color, background_color, txt_color, title_color, info_color = white, black, white, colors[3], colors[2]

figure_w, figure_h = 5, 5        # Определяем ширину и высоту фигур в блоках, они размером 5Х5
        
empty = 'o'
# Задаем отрисовку всех фигур, каждая задается, как элемент словаря, для удобства указаны буквы "соответствия типу фигуры" o- пусто x- занято фигурой
figures = {'S': [['ooooo',
                  'ooooo',
                  'ooxxo',
                  'oxxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'ooxxo',
                  'oooxo',
                  'ooooo']],
           'Z': [['ooooo',
                  'ooooo',
                  'oxxoo',
                  'ooxxo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'oxxoo',
                  'oxooo',
                  'ooooo']],
           'L': [['ooooo',
                  'oxooo',
                  'oxxxo',
                  'ooooo',
                  'ooooo'],
                 ['ooooo',
                  'ooxxo',
                  'ooxoo',
                  'ooxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'oxxxo',
                  'oooxo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'ooxoo',
                  'oxxoo',
                  'ooooo']],
           'J': [['ooooo',
                  'oooxo',
                  'oxxxo',
                  'ooooo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'ooxoo',
                  'ooxxo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'oxxxo',
                  'oxooo',
                  'ooooo'],
                 ['ooooo',
                  'oxxoo',
                  'ooxoo',
                  'ooxoo',
                  'ooooo']],
           'I': [['ooxoo',
                  'ooxoo',
                  'ooxoo',
                  'ooxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'xxxxo',
                  'ooooo',
                  'ooooo']],
           'O': [['ooooo',
                  'ooooo',
                  'oxxoo',
                  'oxxoo',
                  'ooooo']],
           'T': [['ooooo',
                  'ooxoo',
                  'oxxxo',
                  'ooooo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'ooxxo',
                  'ooxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'oxxxo',
                  'ooxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'oxxoo',
                  'ooxoo',
                  'ooooo']]}


fps_clock = pygame.time.Clock() # Указываем с какой частотой отрисовки кадров запускать игру
display = pygame.display.set_mode((window_w, window_h)) # Устанавливаем игровое окно
basic_font = pygame.font.SysFont('arial', 20) # Устанавливаем базовый шрифт и его размер
big_font = pygame.font.SysFont('arial', 45) # Устанавливаем шрифт и размер для больших текстов

def txtObjects(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

def quitGame():
    for event in pygame.event.get(QUIT): # Проверка всех событий, приводящих к выходу из игры
        stop_game() 
    for event in pygame.event.get(KEYUP): 
        if event.key == K_ESCAPE: # Проверяем нажатие клавишы, если нажали эскейп, то выходим из игры
            stop_game() 
        pygame.event.post(event)  # Отправляем наше событие программе

def checkKeys():
    quitGame()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None

def showText(text):
    titleSurf, titleRect = txtObjects(text, big_font, title_color)
    titleRect.center = (int(window_w / 2) , int(window_h / 2) )
    display.blit(titleSurf, titleRect)
   
    pressKeySurf, pressKeyRect = txtObjects('Нажмите любую клавишу для продолжения', basic_font, title_color)
    pressKeyRect.center = (int(window_w / 2), int(window_h / 2) + 100)
    display.blit(pressKeySurf, pressKeyRect)

    while checkKeys() == None:
        pygame.display.update()
        fps_clock.tick()

def stop_game():
    pygame.quit()
    sys.exit()

def create_field():
    # Создаем пустое игровое поле
    field = []
    for i in range(field_w):
        # Создаем поле: для каждого столбца, шириной в клетку поля добавляем по строчке высотой в клетку поля
        field.append([empty] * field_h) # empty - это наш элемент o, который был объявлен ранее
            
    return field

def infield(x, y):
    return x >= 0 and x < field_w and y < field_h

def checkPos(field, fig, adjX=0, adjY=0):
    # Проверяем, находится ли фигура в границах игрового поля, не сталкиваясь с другими фигурами
    for x in range(figure_w): # Для каждого квадратика в ширине фигуры
        for y in range(figure_h): # Для каждого квадратика в высоте фигуры 
            if figures[fig['shape']][fig['rotation']][y][x] == empty: # Проверка квадратик в отрисовке фигуры пустой, если да, то смотрим следующий
                continue
            if not infield(x + fig['x'] + adjX, y + fig['y'] + adjY): # Проверка присутствия фигуры внутри игрового поля, если вышли за границы, то такая позиция недоступна
                return False
            if field[x + fig['x'] + adjX][y + fig['y'] + adjY] != empty: # Если то поле, куда хотим встать не пустое, т.е. не содержит символ o, то позиция недоступна
                return False
    return True

def isCompleted(field, y):
    # Проверяем наличие полностью заполненных рядов
    for x in range(field_w):
        if field[x][y] == empty: # Если где-то пусто, то ряд "y" не заполнен
            return False
    return True


def clearCompleted(field):
    # Удаление заполенных рядов и сдвиг верхних рядов вниз
    removed_lines = 0
    y = field_h - 1 # Последнее поле
    while y >= 0:
        if isCompleted(field, y): # Проверяем заполнен ли последний ряд
           for pushDownY in range(y, 0, -1): # Смотрим с последнего ряда до первого (с индексом 0 он)
                for x in range(field_w):
                    field[x][pushDownY] = field[x][pushDownY-1] # Заменяем ряды, путем смещения их вниз на 1
           for x in range(field_w):
                field[x][0] = empty # Заполняем самый верхний ряд пустотой
           removed_lines += 100 # Увеличиваем наши баллы на 100
        else:
            break
    return removed_lines

def drawTitle():
    titleSurf = big_font.render('Тетрис', True, title_color)
    titleRect = titleSurf.get_rect() # Прямоугольник, ограничивающий текст
    titleRect.topleft = (window_w /2 - int(titleSurf.get_width()/2), 30) # Указываем позицию заголовка
    display.blit(titleSurf, titleRect) # Добавляем наш текст на окно с размерами прямоугольника
    

def drawInfo(points, level):

    pointsSurf = basic_font.render(f'Очки: {points}', True, txt_color)  # Указывается поверхность, на которой будет текст, второй параметр - сглаживание, третий - цвет текста
    pointsRect = pointsSurf.get_rect()
    pointsRect.topleft = (50, 180)       # Координаты информации о баллах
    display.blit(pointsSurf, pointsRect) # Привязываем поверхность к нашему окну с ограничивающим прямоуголником pointsRect

    levelSurf = basic_font.render(f'Уровень: {level}', True, txt_color)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (50, 200)
    display.blit(levelSurf, levelRect)

    pausebSurf = basic_font.render('Пауза: пробел', True, info_color)
    pausebRect = pausebSurf.get_rect()
    pausebRect.topleft = (50, 220)
    display.blit(pausebSurf, pausebRect)
    
    escbSurf = basic_font.render('Выход: Esc', True, info_color)
    escbRect = escbSurf.get_rect()
    escbRect.topleft = (50, 240)
    display.blit(escbSurf, escbRect)