
from time import time
from Pricas import *
from copy import copy
b = 96
proces = 0
tl = time()
ert, matrix, biome_map, biome_claster, Clasic = new_world(b)
print(time() - tl)
tl = time()
st = load('Пустой_Структура.bin')
new1 = st['Tree1']
new2 = st['Tree2']
new3 = st['el']
new4 = st['el2']
new5 = st['Cactus1']
new6 = st['Palma1']
new7 = st['acac1']
ert, matrix = set_Biome(ert, matrix, biome_claster['Луг'], [TZ], b, new2, 20, 0.9)
ert, matrix = set_Biome(ert, matrix, biome_claster['Луг'], [TZ], b, new1, 70, 0.9)
ert, matrix = set_Biome(ert, matrix, biome_claster['Заснежина'], [SZ, PZ], b, new3, 20, 0.9)
ert, matrix = set_Biome(ert, matrix, biome_claster['Заснежина'], [SZ, PZ], b, new4, 30, 0.9)
ert, matrix = set_Biome(ert, matrix, biome_claster['Пустыня'], [PS, PK], b, new5, 15, 0.9)
ert, matrix = set_Biome(ert, matrix, biome_claster['Пустыня'], [PS], b, new6, 10, 0.9)
ert, matrix = set_Biome(ert, matrix, biome_claster['Савана'], [SVZ, PS], b, new7, 15, 0.78)
print(time() - tl)
nower = (3, 3, Z_get(ert, 3, 3))
print('go!')
pg.init()
pg.mixer.init()
# создание окна ыгры
print('разрешение:', sc.get_size())
X_E, Y_E = sc.get_size()
tY = Y_E // 40
tX = (X_E - X_E // 4) // 40
X_M, Y_M = 0, 0
pg.display.set_caption("Grim Story")
clock = pg.time.Clock()
running = True
xp, yp, zp = 0, 0, 18
mobs = {}
things = {}

DR = STR_to_Thing('древесина')


for _ in range(20):
    x, y = random.randint(20, 30), random.randint(20, 30)
    things[x, y, Z_get(ert, x, y)] = DR
p_things = things.copy()

ggg = 5, 5, Z_get(ert, 5, 5)
mobs[ggg] = mob('Природный элементаль', ['Силы Света', 'Голем'], GL, 100, 100, Strong, [], None, [], ['Нежить', 'Силы тьмы'], [], Elser)
mobs[ggg].name = 'Природный элементаль2'
Find_resurs(ert, matrix, mobs, things, p_things,  b, ggg, [(DR, 5), (5, 5)])

ggg = 10, 5, Z_get(ert, 10, 5)


mobs[ggg] = mob('Природный элементаль', ['Силы Света', 'Голем'], GL, 100, 100, Strong, [], None, [], ['Нежить', 'Силы тьмы'], [], Elser)
Find_resurs(ert, matrix, mobs, things, p_things,  b, ggg, [(DR, 5), (10, 5)])

als = things | mobs


font = pg.font.SysFont(None, 24)

mob_timer = time()
while running:
    # ввод

    if clock.get_fps() != 0:
        shade = 1 / clock.get_fps()
    MX, MY = pg.mouse.get_pos()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_e:
                zp += 1
            if event.key == pg.K_q:
                zp -= 1
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_d:
                xp += 5
            if event.key == pg.K_a:
                xp -= 5
            if event.key == pg.K_w:
                yp -= 5
            if event.key == pg.K_s:
                yp += 5
            if event.key == pg.K_DOWN:
                Y_M += 1
            if event.key == pg.K_UP:
                Y_M -= 1
            if event.key == pg.K_RIGHT:
                X_M += 1
            if event.key == pg.K_LEFT:
                X_M -= 1
            if event.key == pg.K_SPACE:
                nower = (X_M+xp, Y_M+yp, Z_get(ert, X_M+xp, Y_M+yp))
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button ==1:
                MX, MY = pg.mouse.get_pos()
                MX = (MX)//40 + xp
                MY = (MY)//40 + yp
                ztarg = Z_get(ert, MX, MY)
                ert[MX, MY, ztarg-1] = VH
            elif event.button ==2:
                MX, MY = pg.mouse.get_pos()
                MX = (MX)//40 + xp
                MY = (MY)//40 + yp
                ztarg = Z_get(ert, MX, MY)
                ert[MX, MY, ztarg] = WT

    # обработка

    if time() - mob_timer >= 0.3:
        mob_timer = time()
        mobus = mobs.copy()
        for i in mobus:

            print(i, len(mobs[i].inventory), mobs[i].name)
            if mobs[i].pricas:
                func, op = mobs[i].pricas.popleft()

                if not(func(ert, matrix, mobs, things,  p_things, b, i, op)):
                    mobs[i].pricas.appendleft((func, op))
            else:
                func, op = mobs[i].els.get()
                func(ert, matrix, mobs, things,  p_things, b, i, op)
            als = things | mobs



    # отрисовка
    sc.fill((0, 0, 0))

    for x in range(0, tX):
        for y in range(0, tY):
            for z in range(0, 20):
                if 0 <= x + xp <= b-2 and 0 <= z + zp <= b-2 and 0 <= y + yp <= b-2:
                    if ert[x + xp, y + yp, z + zp].real and not(ert[x + xp + 1, y + yp, z + zp].vis and ert[x + xp, y + yp + 1, z + zp].vis and ert[x + xp, y + yp, z + zp + 1].vis):
                        sc.blit(ert[x + xp, y + yp, z + zp].png, ((x * 40)-(z*10), (y*40)-(z*10)))
                    elif als.get((x + xp, y + yp, z + zp), False):
                        sc.blit(als[x + xp, y + yp, z + zp].png, ((x * 40)-(z*10), (y*40)-(z*10)))

    img = font.render(str(clock.get_fps()), True, (255, 0, 0))

    sc.blit(img, (20, 20))

    pg.display.flip()
    clock.tick(1000)

pg.quit()
