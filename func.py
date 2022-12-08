import numba

import heapq as hq
import numpy as np
import pickle as pc
from const import *


@numba.njit(fastmath=True)
def glad(n, b, r):
    fs = n
    for x in range(b):
        for y in range(b):
            summ = 0
            k = 0
            for xx in range(-r, r + 1):
                for yy in range(-r, r + 1):
                    if 0 <= xx + x <= b - 1 and 0 <= yy + y <= b - 1:
                        summ += fs[x + xx, y + yy]
                        k += 1
            n[x, y] = summ // k
    return n


@numba.njit(fastmath=True)
def octava(b, v, d=1):
    first = np.full((b, b), 0)
    for x in range(0, b, v):
        for y in range(0, b, v):
            tt = random.randint(-d, d)
            for xx in range(0, v):
                for yy in range(0, v):
                    first[xx + x, y + yy] += tt
    return first


@numba.njit(fastmath=True)
def perlin_voice(b, v, r, d=1):
    first = np.full((b, b), v)
    for i in range(1, b):
        if b % i == 0:
            first = first + octava(b, i, d)

    return glad(first, b, r)


@numba.njit(fastmath=True)
def land_shaft(b):
    land = np.full((b, b), 23)
    gor = perlin_voice(b, 0, 3)
    for i in range(1, b):
        if b % i == 0:
            for x in range(0, b, i):
                for y in range(0, b, i):
                    if gor[x + i // 2, y + i // 2] > 3:
                        tt = random.randint(0, 4)
                    else:
                        tt = random.randint(-1, 1)
                    for xx in range(0, i):
                        for yy in range(0, i):
                            land[xx + x, y + yy] += tt
    land = glad(land, b, 2)

    return land, gor


def new_world(b):
    matrix = np.full((b, b, b), 0)
    ert = np.full((b, b, b), VH)
    biome_map = np.full((b, b), Lug)
    temp = perlin_voice(b, 0, 8, 3)

    land, gor = land_shaft(b)
    biome_claster = {}
    for i in Normy:
        biome_claster[i.name] = []
    biome_claster['Луг'] = []
    proces = 0
    Clasic = Claster('Normal World', Normy, temp, land, gor, Lug)
    for x in range(b):
        for y in range(b):
            proces += 1
            blok, bereg, vd, vh, nm = Clasic.give_blocks(x, y)
            biome_map[x, y] = nm

            biome_claster[nm.name].append((x, y))
            t = land[x, y]

            sloi = nm.ln
            if t >= 23:
                for i, bl in enumerate(blok):
                    for z in range(t // sloi * i, t // sloi * (i + 1)):
                        ert[x, y, z] = bl
                        matrix[x, y, z] = bl.hod
                for z in range(t // sloi * (i + 1), t + 1):
                    matrix[x, y, z] = blok[-1].hod
                    ert[x, y, z] = blok[-1]
                ert[x, y, t] = vh
                matrix[x, y, t] = vh.hod


            elif t <= 20:
                for i, bl in enumerate(blok):
                    for z in range(t // sloi * i, t // sloi * (i + 1)):
                        ert[x, y, z] = bl
                        matrix[x, y, z] = bl.hod
                for z in range(t // sloi * (i + 1), t+1):
                    matrix[x, y, z] = blok[-1].hod
                    ert[x, y, z] = blok[-1]
                ert[x, y, t] = bereg
                matrix[x, y, t] = bereg.hod
                for z in range(t+1, 22):
                    ert[x, y, z] = vd
                    matrix[x, y, z] = vd.hod


            else:
                for i, bl in enumerate(blok):
                    for z in range(t // sloi * i, t // sloi * (i + 1)):
                        ert[x, y, z] = bl
                        matrix[x, y, z] = bl.hod
                for z in range(t // sloi * (i + 1), t + 1):
                    ert[x, y, z] = blok[-1]
                    matrix[x, y, z] = blok[-1].hod
                ert[x, y, t] = vh
                matrix[x, y, t] = vh.hod
                for xx, yy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                    if 0 <= xx + x <= b - 1 and 0 <= y + yy <= b - 1:
                        if land[xx + x, yy + y] <= 20:
                            ert[x, y, t] = bereg
                            matrix[x, y, t] = bereg.hod
                            break

    return ert, matrix, biome_map, biome_claster, Clasic




def rotated(d):
    t = random.randint(1, 4)
    for i in range(len(d)):
        d[i] = np.rot90(d[i], t)
    return d


def Z_get(ert, x, y):
    for z in range(58, 0, -1):
        if ert[x, y, z].real:
            return z + 1
    return z

def Z_get_vis(ert, x, y):
    for z in range(58, 0, -1):
        if ert[x, y, z].real and ert[x, y, z].vis:
            return z + 1
    return z

@numba.njit(fastmath=True)
def Z_get_m(matrix, x, y):
    for z in range(58, 0, -1):
        if matrix[x, y, z] != 0:
            return z + 1
    return 0





def check_m(ert, start, shir, proc, block, b):
    xk, yk, zk = shir
    xs, ys, zs = start
    c = 0
    if not(0<=xs+xk<=b-1 and 0<=ys+yk<=b-1 and 0<=zs+zk<=b-1):
        return False
    for x in range(xs, xs+xk):
        for y in range(ys, ys+yk):
            if not(ert[x, y, zs].real) and ert[x, y, zs-1].real and ert[x, y, zs-1] in block:
                c += 1
    return c/(yk*xk)>=proc







def structur(ert, matrix, start, stk, shir):
    xk, yk, zk = shir
    stk = rotated(stk)
    xs, ys, zs = start
    for x in range(xk):
        for y in range(yk):
            for z in range(zk):
                if stk[z, y, x].real:
                    stk[z, y, x].optimaised()
                    stk[z, y, x].vis = True
                    ert[x+xs, y+ys, z+zs] = stk[z, y, x]
                    matrix[x+xs, y+ys, z+zs] = stk[z, y, x].hod
    return ert, matrix

def set_Biome(ert, matrix, claster, blocks, b, stc, n, proc):
    zk = len(stc)
    yk = len(stc[0])
    xk = len(stc[0][0])
    shir = (xk, yk, zk)
    k = 0
    s = 0
    while n:
        xu, yu = random.choice(claster)
        xu-=xk//2
        yu-=yk//2
        zu = Z_get_vis(ert, xu, yu)
        if check_m(ert, (xu, yu, zu), shir, proc, blocks, b):
            ert, matrix = structur(ert, matrix, (xu, yu, zu), rotated(stc), shir)
            n -= 1
            s = 0
            k+=1
        else:
            s+=1
            if s>= 10000:
                n = 0
                s = 0
    print(k, 'поставленно')

    return ert, matrix








@numba.njit(fastmath=True)
def evrei_manhent(a, b):
    return (abs(a[0] - b[0])+abs(a[1] - b[1])+abs(a[2] - b[2]))






@numba.njit(fastmath=True)
def A_star(start, goal, matrix, b, evr):
    ot = []
    ways = dict()
    ways[start] = 0
    visit = dict()
    visit[start] = (-9, -9, -9)
    que = list()
    que.append((0, start))
    checks = list()
    checks.append((1, 1, 1))
    cho = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

    while que:
        cur_cost, cur_node = hq.heappop(que)
        if cur_node == goal:

            that = goal
            while that != (-9, -9, -9):
                ot.append(that)
                that = visit[that]

            ot.reverse()
            return ot
        xn, yn, zn = cur_node
        checks.clear()
        for xt, yt in cho:
            if 1 <= xn <= b - 2 and 1 <= yn <= b - 2 and 1 <= zn <= b - 2:
                if matrix[xn + xt, yn + yt, zn] == 0:
                    if matrix[xn + xt, yn + yt, zn - 1] != 0:
                        neight_node = xn + xt, yn + yt, zn
                        neight_cost = matrix[xn + xt, yn + yt, zn - 1]
                        new_cost = ways[cur_node] + neight_cost
                        if neight_node not in ways or new_cost < ways[neight_node]:
                            tr = 0
                            if (xt == -1 or xt == 1) and (yt == -1 or yt == 1):
                                tr = 1
                            prioritet = new_cost + evr(neight_node, goal) + tr
                            hq.heappush(que, (prioritet, neight_node))
                            ways[neight_node] = new_cost
                            visit[neight_node] = cur_node
                    elif matrix[xn + xt, yn + yt, zn - 2] != 0:
                        neight_node = xn + xt, yn + yt, zn - 1
                        neight_cost = matrix[xn + xt, yn + yt, zn - 2]
                        new_cost = ways[cur_node] + neight_cost
                        if neight_node not in ways or new_cost < ways[neight_node]:
                            tr = 0
                            if (xt == -1 or xt == 1) and (yt == -1 or yt == 1):
                                tr = 1
                            prioritet = new_cost + evr(neight_node, goal) + tr
                            hq.heappush(que, (prioritet, neight_node))
                            ways[neight_node] = new_cost
                            visit[neight_node] = cur_node
                elif matrix[xn + xt, yn + yt, zn + 1] == 0:
                    neight_node = xn + xt, yn + yt, zn + 1
                    neight_cost = matrix[xn + xt, yn + yt, zn]
                    new_cost = ways[cur_node] + neight_cost
                    if neight_node not in ways or new_cost < ways[neight_node]:
                        tr = 0
                        if (xt == -1 or xt == 1) and (yt == -1 or yt == 1):
                            tr = 1
                        prioritet = new_cost + evr(neight_node, goal) + tr
                        hq.heappush(que, (prioritet, neight_node))
                        ways[neight_node] = new_cost
                        visit[neight_node] = cur_node
    return ot


def razlif(ert, matr, xyz, b):
    if ert[xyz].name == 'Вода':
        x, y, z = xyz
        if ert[x, y, z-1].real:
            cho = [(1, 0), (0, 1), (0, -1), (-1, 0)]
            random.shuffle(cho)
            if ert[x, y, z-1].name == 'Вода':
                if ert[x, y, z-1].hod < ert[xyz].hod:
                    ert[xyz].hod -= 1
                    matr[xyz] = ert[xyz].hod
                    ert[x, y, z-1].hod += 1
                    matr[x, y, z-1] = ert[x, y, z-1].hod
                    return ert
            if ert[xyz].hod > 2:
                for xx, yy in cho:
                    if 0<=x+xx<=b-1 and 0<=y+yy<=b-1:
                        if not(ert[x+xx, y+yy, z].real):
                            ert[xyz].hod //=2
                            ert[x + xx, y + yy, z] = ert[xyz]
                            matr[x + xx, y + yy, z] = ert[xyz].hod
                            matr[xyz] = ert[xyz].hod
            else:
                for xx, yy in cho:
                    if 0<=x+xx<=b-1 and 0<=y+yy<=b-1:
                        if not(ert[x+xx, y+yy, z].real):
                            ert[x + xx, y + yy, z], ert[xyz] = ert[xyz], VH
                            matr[xyz] = 0
                            matr[x + xx, y + yy, z] = ert[x + xx, y + yy, z].hod

        else:
            ert[xyz], ert[x, y, z-1] = VH, ert[xyz]
            matr[xyz] = 0
            matr[x, y, z-1] = ert[x, y, z-1].hod


    return ert, matr








@numba.njit(fastmath=True)
def Deickstar(start, goal, matrix, b, check):
    ot = []
    ways = dict()
    ways[start] = 0
    visit = dict()
    visit[start] = (-9, -9, -9)
    que = list()
    que.append((0, start))
    checks = list()
    checks.append((1, 1, 1))
    cho = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

    while que:
        cur_cost, cur_node = hq.heappop(que)
        if check(cur_node, goal, matrix):

            that = cur_node
            while that != (-9, -9, -9):
                ot.append(that)
                that = visit[that]

            ot.reverse()
            return ot
        xn, yn, zn = cur_node
        checks.clear()
        for xt, yt in cho:
            if 1 <= xn <= b - 2 and 1 <= yn <= b - 2 and 1 <= zn <= b - 2:
                if matrix[xn + xt, yn + yt, zn] == 0:
                    if matrix[xn + xt, yn + yt, zn - 1] != 0:
                        neight_node = xn + xt, yn + yt, zn
                        neight_cost = matrix[xn + xt, yn + yt, zn - 1]
                        new_cost = ways[cur_node] + neight_cost
                        if neight_node not in ways or new_cost < ways[neight_node]:
                            tr = 0
                            if (xt == -1 or xt == 1) and (yt == -1 or yt == 1):
                                tr = 1

                            hq.heappush(que, (new_cost + tr, neight_node))
                            ways[neight_node] = new_cost
                            visit[neight_node] = cur_node
                    elif matrix[xn + xt, yn + yt, zn - 2] != 0:
                        neight_node = xn + xt, yn + yt, zn - 1
                        neight_cost = matrix[xn + xt, yn + yt, zn - 2]
                        new_cost = ways[cur_node] + neight_cost
                        if neight_node not in ways or new_cost < ways[neight_node]:
                            tr = 0
                            if (xt == -1 or xt == 1) and (yt == -1 or yt == 1):
                                tr = 1

                            hq.heappush(que, (new_cost + tr, neight_node))
                            ways[neight_node] = new_cost
                            visit[neight_node] = cur_node
                elif matrix[xn + xt, yn + yt, zn + 1] == 0:
                    neight_node = xn + xt, yn + yt, zn + 1
                    neight_cost = matrix[xn + xt, yn + yt, zn]
                    new_cost = ways[cur_node] + neight_cost
                    if neight_node not in ways or new_cost < ways[neight_node]:
                        tr = 0
                        if (xt == -1 or xt == 1) and (yt == -1 or yt == 1):
                            tr = 1

                        hq.heappush(que, (new_cost + tr, neight_node))
                        ways[neight_node] = new_cost
                        visit[neight_node] = cur_node
    return ot

def find_thing(start, matrix, things, b, th):
    ot = []
    ways = dict()
    ways[start] = 0
    visit = dict()
    visit[start] = (-9, -9, -9)
    que = list()
    que.append((0, start))
    checks = list()
    checks.append((1, 1, 1))
    cho = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

    while que:
        cur_cost, cur_node = hq.heappop(que)
        if things.get(cur_node, 2) == th:

            that = cur_node
            while that != (-9, -9, -9):
                ot.append(that)
                that = visit[that]

            ot.reverse()
            return ot
        xn, yn, zn = cur_node
        checks.clear()
        for xt, yt in cho:
            if 1 <= xn <= b - 2 and 1 <= yn <= b - 2 and 1 <= zn <= b - 2:
                if matrix[xn + xt, yn + yt, zn] == 0:
                    if matrix[xn + xt, yn + yt, zn - 1] != 0:
                        neight_node = xn + xt, yn + yt, zn
                        neight_cost = matrix[xn + xt, yn + yt, zn - 1]
                        new_cost = ways[cur_node] + neight_cost
                        if neight_node not in ways or new_cost < ways[neight_node]:
                            tr = 0
                            if (xt == -1 or xt == 1) and (yt == -1 or yt == 1):
                                tr = 1

                            hq.heappush(que, (new_cost + tr, neight_node))
                            ways[neight_node] = new_cost
                            visit[neight_node] = cur_node
                    elif matrix[xn + xt, yn + yt, zn - 2] != 0:
                        neight_node = xn + xt, yn + yt, zn - 1
                        neight_cost = matrix[xn + xt, yn + yt, zn - 2]
                        new_cost = ways[cur_node] + neight_cost
                        if neight_node not in ways or new_cost < ways[neight_node]:
                            tr = 0
                            if (xt == -1 or xt == 1) and (yt == -1 or yt == 1):
                                tr = 1

                            hq.heappush(que, (new_cost + tr, neight_node))
                            ways[neight_node] = new_cost
                            visit[neight_node] = cur_node
                elif matrix[xn + xt, yn + yt, zn + 1] == 0:
                    neight_node = xn + xt, yn + yt, zn + 1
                    neight_cost = matrix[xn + xt, yn + yt, zn]
                    new_cost = ways[cur_node] + neight_cost
                    if neight_node not in ways or new_cost < ways[neight_node]:
                        tr = 0
                        if (xt == -1 or xt == 1) and (yt == -1 or yt == 1):
                            tr = 1

                        hq.heappush(que, (new_cost + tr, neight_node))
                        ways[neight_node] = new_cost
                        visit[neight_node] = cur_node
    return ot


@numba.njit(fastmath=True)
def check_flag(cur, goal, matrix):
    return cur == goal


def save(name, g):
    t = 'Saves/' + name
    with open(t, 'wb') as f:
        pc.dump(g, f)


def load(name):
    t = 'Saves/' + name
    with open(t, 'rb') as f:
        return pc.load(f)

def STR_to_Thing(name, Keys=[]):
    KeyWords = ['Предметы']
    for i in Keys:
        KeyWords.append(i)
    return Thing(name, KeyWords, pg.image.load('Sprites/things/'+name+'.png'), name)

