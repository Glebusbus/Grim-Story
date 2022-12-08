
from mobs_func import *

Strong = Stats(('Сила', 8),('Скорость', 4),('Защита', 8),('Внимание', 10))
GL = pg.image.load('Sprites/mobs/Пр_ЭЛ.png').convert_alpha()
Elser = Cycle((random_walk, 0), (stay, 0))
Golem = mob('Природный элементаль', ['Силы Света', 'Голем'], GL, 100, 100, Strong, [], None, [], ['Нежить', 'Силы тьмы'], [], Elser)
