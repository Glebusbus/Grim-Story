
from clases import *
import pygame as pg
from pygame.locals import *

flags = FULLSCREEN | DOUBLEBUF
sc = pg.display.set_mode((0, 0), flags, 16)
LD_ = pg.image.load('Sprites/блоки/лёд.png').convert_alpha()
LD_.set_alpha(150)
LD =  block(True, LD_, [], 'Лёд', False, False, 24, False)

ST_ = pg.image.load('Sprites/блоки/база.png').convert_alpha()
ST = block(True, ST_, ['Камень'], 'Камень', False, False)
Z_ = pg.image.load('Sprites/блоки/земля.png').convert_alpha()
Z = block(True, Z_, ['Земля'], 'Земля', False, False)
SZ_ = pg.image.load('Sprites/блоки/снег.png').convert_alpha()
SZ = block(True, SZ_, ['Земля'], 'Снег', False, False, 2)
SS_ = pg.image.load('Sprites/блоки/снег_камень.png').convert_alpha()
SS = block(True, SS_, ['Камень'], 'Снегокамень', False, False, 2)
ZT_ = pg.image.load('Sprites/блоки/Заросший камень.png').convert_alpha()
ZT = block(True, ZT_, ['Камень'], 'Заросший камень', False, False)
TZ_ = pg.image.load('Sprites/блоки/трава.png').convert_alpha()
TZ = block(True, TZ_, ['Земля'], 'Дёрн', False, False)
PZ_= pg.image.load('Sprites/блоки/подзол.png').convert_alpha()
PZ = block(True, PZ_, ['Земля'], 'Подзол', False, False)
SVZ_ = pg.image.load('Sprites/блоки/савана.png').convert_alpha()
SVZ = block(True, SVZ_, ['Земля'], 'Саван', False, False)
PT_ = pg.image.load('Sprites/блоки/песочный камень.png')
PT = block(True, PT_, ['Песок', 'Песок'], 'Пескамень', False, False)
PS_ = pg.image.load('Sprites/блоки/песок.png').convert_alpha()
PS = block(True, PS_, ['Песок', 'Песок'], 'Песок', False, False, 2)
PK_ = pg.image.load('Sprites/блоки/песчаник.png').convert_alpha()
PK = block(True, PK_, ['Песок', 'Песок'], 'Песчаник', False, False)
DR_ = pg.image.load('Sprites/блоки/ствол.png').convert_alpha()
DR = block(True, DR_, ['Древесина', 'Древесина', 'Древесина'], 'Дeрево', False, False)
LS_ = pg.image.load('Sprites/блоки/листва.png').convert_alpha()
LS = block(True, LS_, [], 'Листвва', False, True)
WT_ = pg.image.load('Sprites/блоки/вода.png').convert_alpha()
WT_.set_alpha(75)
WT = block(True, WT_, ['Вода'], 'Вода', True, True, 16, False)
RI_ = pg.image.load('Sprites/блоки/булыжник.png').convert_alpha()
RI = block(True, RI_, ['Камень', 'Камень'], 'Руина', False, False)
VH = block(False, 0, 0, 'Воздух', True, False, 0, False)
SST_= pg.image.load('Sprites/блоки/сава-камень.png').convert_alpha()
SST = block(True, SST_, ['Камень'], 'Савано-камень', False, False)
TST_ = pg.image.load('Sprites/блоки/под_камень.png')
TST = block(True, TST_, ['Камень'], 'Тундровый камень', False, False)
GR_ = pg.image.load('Sprites/блоки/галька.png').convert_alpha()
GR = block(True, GR_, ['Галька'], 'Галька', False, False, 3)
KG_ =  pg.image.load('Sprites/блоки/к_глина.png').convert_alpha()
KRG_ =  pg.image.load('Sprites/блоки/кр_глина.png').convert_alpha()
JG_ =  pg.image.load('Sprites/блоки/ж_глина.png').convert_alpha()
SG_ =  pg.image.load('Sprites/блоки/ср_глина.png').convert_alpha()
BG_ =  pg.image.load('Sprites/блоки/с_глина.png').convert_alpha()
KG = block(True, KG_, ['Глина'], 'Глина', False, False)
KRG = block(True, KRG_, ['Глина'], 'Глина', False, False)
JG = block(True, JG_, ['Глина'], 'Глина', False, False)
BG = block(True, BG_, ['Глина'], 'Глина', False, False)
SG = block(True, SG_, ['Глина'], 'Глина', False, False)

blocks = [ST, Z, TZ, PS, PK, DR, LS, WT, RI, VH]
Lug = Biome('Луг', lambda t, l, g: True, [ST, ST, Z], PS, WT, TZ)
Pust = Biome('Пустыня', lambda t, l, g: (t >= 5 and l <= 26), [ST, ST, PK], PS, WT, PS)
Sneg = Biome('Заснежина', lambda t, l, g: (t <= -5 and l <= 26), [ST, ST, Z], GR, LD, SZ)
Savan = Biome('Савана', lambda t, l, g: (3 <= t < 5 and l <= 26), [ST, ST, Z], PK, WT, SVZ)
SVGors = Biome('Савано-горы', lambda t, l, g: (3 <= t < 5 and l >= 27), [ST], PK, WT, SST)
GGors = Biome('Месса', lambda t, l, g: (t >= 5 and l >= 27), [BG, SG, JG, KRG, KG, KRG, JG, SG, BG, SG, JG, KRG], KG, WT, KG)
Gors = Biome('Зелёные-горы', lambda t, l, g: (-3<t<3 and l >= 27), [ST], ZT, WT, ZT)
SGors = Biome('Снежные-горы', lambda t, l, g: (t <= -5 and l >= 27), [ST], SZ, LD, SS)
Tundra = Biome('Тундра', lambda t, l, g: (-5 < t <= -3 and l <= 26), [ST, ST, Z], GR, LD, PZ)
TGors = Biome('Тундра-горы', lambda t, l, g: (-5 < t <= -3 and l >= 27), [ST], GR, LD, TST)

Normy = [TGors, Tundra, SGors, Gors, Savan, GGors, SVGors, Sneg, Pust]





