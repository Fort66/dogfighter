# import pygame
# import math
# import os
# pi = math.pi

# class Map:
#     def __init__(self, radius, grid_size):
#         self.radius = radius
#         self.grid_size = grid_size
        
# #Создает вершины для каждого гекса
#     def hexVertices(self, x_init, y_init, shiftX, shiftY):
#         self.x_init = x_init
#         self.y_init = y_init
#         self.shiftX = shiftX
#         self.shiftY = shiftY
#         self.vertices = []
#         for i in range(0,6):
#             self.vertices.append((self.radius * math.cos(i * pi / 3) + self.x_init + self.shiftX,
#                                   self.radius * math.sin(i * pi / 3) + self.y_init + self.shiftY))
#         return self.vertices

# #Создать перекрестия для центрирования (ВРЕМЕННО)   
#     def centerCross(self, startX, startY, endX, endY):
#         self.startX = startX
#         self.startY = startY
#         self.endX = endX
#         self.endY = endY
#         pygame.draw.line(wn, BLACK, (self.startX, self.startY), (self.endX, self.endY)) 

# #Создает всю сетку (вызывает hexVertices)
#     def hexCoord(self):
#         x_shift = [3*radius/2 ,3*radius/2 ,0,
#                    -3*radius/2, -3*radius/2, 0]
#         y_shift = [math.sqrt(3)*radius/2,-math.sqrt(3)*radius/2,-math.sqrt(3)*radius,
#                    -math.sqrt(3)*radius/2,math.sqrt(3)*radius/2,math.sqrt(3)*radius]
#         x_init = wn_width/2 - ((grid_size-1)*3/2)*radius
#         y_init = (wn_height + math.sqrt(3) * (grid_size-1) * radius) / 2
#         for k in range(1,grid_size+1):
#             shiftX = 0; shiftY = 0; n = 0    
#             while n < 6:
#                 for i in range(0,grid_size - k):
#                     vertices = m.hexVertices(x_init, y_init, shiftX, shiftY)
#                     pygame.draw.polygon(wn,RED,(vertices))
#                     pygame.draw.polygon(wn,BLACK,(vertices),width=1)
#                     pygame.draw.circle(wn,BLACK,(x_init+shiftX,y_init+shiftY),radius/10)
#                     shiftX += x_shift[n]
#                     shiftY += y_shift[n]
#                 n += 1
#             x_init += 3/2*radius; y_init -= math.sqrt(3)*radius/2
#         vertices = m.hexVertices(wn_width/2, wn_height/2, 0, 0)
#         pygame.draw.polygon(wn,RED,(vertices))
#         pygame.draw.polygon(wn,BLACK,(vertices),width=1) 
#         pygame.draw.circle(wn,BLACK,(wn_width/2,wn_height/2),radius/10)

# class CharacterMove:
#     def __init__(self):
#         pass
        
#     def move(self, position):
#         self.position = position
#         pygame.draw.circle(wn, YELLOW, self.position, radius/2)
#         pygame.display.update()

# pygame.init()
# clock = pygame.time.Clock()
# #ЦВЕТА
# BLACK = (0,0,0); BLUE = (0,0,255); RED=(255,0,0); WHITE=(255,255,255); YELLOW=(255,255,0)

# #РАЗМЕРЫ
# grid_size = 6; radius = 25; wn_width = 600; wn_height = 600; step_size = radius/grid_size

# #Инициализация класса Map
# m = Map(radius, grid_size)
# #ОСНОВНОЙ ИГРОВОЙ ЦИКЛ    
# wn=pygame.display.set_mode((wn_width,wn_height))
# wn.fill(BLUE)

# ######Первоначальная конструкция перед основным циклом
# m.centerCross(0, wn_height/2, wn_width, wn_height/2)
# m.centerCross(wn_width/2, 0, wn_width/2, wn_height)
# m.hexCoord()
# CharacterMove().move((wn_width/2,wn_height/2))
# ######

# pygame.display.update()

# state = True
# while state:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             state = False
   
#     #ВЫЗОВ ПЕРЕКРЕСТИЯ
#     m.centerCross(0, wn_height/2, wn_width, wn_height/2)
#     m.centerCross(wn_width/2, 0, wn_width/2, wn_height)
    
#     #СОЗДАЕТ ГЕКСАГОНАЛЬНУЮ СЕТКУ
#     m.hexCoord()   
    
#     #позиция игрока
#     if event.type == pygame.MOUSEBUTTONDOWN:
#         position = pygame.mouse.get_pos()
#         CharacterMove().move(position)
#  #   pygame.display.update()
#     clock.tick(30)
# pygame.quit()
# quit()


# import pygame
# import gif_pygame
# import sys

# screen = pygame.display.set_mode((512, 512))
# clock = pygame.Clock()

# # Loading from a file. You can specify the number of loops, but by default it is infinite
# animation_gif = gif_pygame.load("images/supawork3.gif")
# animation_gif = gif_pygame.transform.scale_by(animation_gif, .4, new_gif=True)



# # for surface in animation_gif.get_surfaces():
# #     surface = gif_pygame.transform.scale_by(surface, .4)
# rect = animation_gif.get_rect(center=(256, 256))


# # Creating an animation from a list of surfaces
# s1 = pygame.Surface((20, 0))
# s2 = pygame.Surface((20, 0))
# s3 = pygame.Surface((20, 0))
# s1.fill((255, 0, 0))
# s2.fill((0, 255, 0))
# s3.fill((0, 0, 255))

# # For every list, first index must be the surface and second must be the duration in seconds. You can specify the number of loops, but by default it is infinite
# animation_surfs = gif_pygame.GIFPygame([[s1, 1], [s2, 1], [s3, 0.5]])

# Main loop
# while True:
#     clock.tick(60)

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

#     screen.fill((0, 0, 0))

#     # This module provides 2 methods for rendering the animation.

#     # Method 1: using .render() | Animates and renders into the screen inside the function itself. You must pass down the surface to blit to and the location
#     animation_gif.render(screen, rect)

#     # Method 2: using .blit_ready() | Animates the animation and returns the current frame. This was meant to be used alongside pygame.Surface().blit()
#     # screen.blit(animation_surfs.blit_ready(), (70, 70))

#     pygame.display.flip()



import pygame as pg
# import pygame_widgets as pw
from pygame_widgets.button import Button
import sys

from Buttons.class_ButtonText import ButtonText
from Buttons.class_ButtonImage import ButtonImage

screen = pg.display.set_mode((512, 512))
clock = pg.time.Clock()


def test(*args, **kwargs):
    if args:
        print(args)
    if kwargs:
        for key, value in kwargs.items():
            print(key, value)
    if not args and not kwargs:
        print('None')

btn = ButtonText(
        surface=screen,
        pos=(256, 256),
        size=(200, 50),
        # bg_color='red',
        # text='Начать игру',
        on_click=lambda: test(1, 2, 3, 4, 5, name='John', age=25),
        rounding=20

)

# btn = ButtonImage(
#     pos=(256, 256),
#     size=(200, 50),
#     text='Начать игру',
    
# )


# btn = Button(
#     win=screen,
#     x=256,
#     y=256,
#     width=200,
#     height=50,
#     text='Начать игру',
#     inactiveColour='SteelBlue',
#     hoverColour='RoyalBlue',
#     shadowColour='grey',
#     pressedColour='dark'
# )


while True:
    clock.tick(60)
    screen.fill('SkyBlue')

    # events = pg.event.get()
    for event in pg.event.get():
        # btn.handleEvent(event)
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            sys.exit()


    btn.update()
    # pw.update(pg.event.get())
    pg.display.update()