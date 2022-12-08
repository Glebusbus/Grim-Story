import pygame as pg
import random
from collections import deque
class block:
    def __init__(self, real, png, give, name, can_walk, crisha, hod=2, vis=True):
        self.png = png
        self.give = give
        self.can_walk = can_walk
        self.crisha = crisha
        self.name = name
        self.real = real
        self.hod = hod
        self.vis = vis
        self.metka = False


    def paint(self, x, y, z, sc):
        sc.blit(self.png, ((x * 40) - (z * 10), (y * 40) - (z * 10)))

    def optimaised(self):
        try:
            self.png = pg.image.load(self.png).convert_alpha()
            self.give = self.give.split()
        except Exception:
            pass

    def reform_p(self, x, y, z):
        return p_block(self.real, self.png, self.give, self.name, self.can_walk, self.crisha, (x, y, z))

    def reform_f(self, b):
        return f_block(self.real, self.png, self.give, self.name, self.can_walk, self.crisha, b)

    def __str__(self):
        return self.name[0:1]

class Stats:
    def __init__(self, *args):
        self.stat = {}
        for i in args:
            self.stat[i[0]] = i[1]

    def test(self, *args):

        for i in args:
            if self.stat.get(i[0], False):
                if self.stat[i[0]] < i[1]:
                    return False
            else:
                return False
        return True

    def get_st(self, b):
        try:
            return self.stat[b]
        except Exception:
            return 0






class Telo:
    def __init__(self, Mx_hp, Hp, D_hp, T, sostav):
        self.Mx_hp = Mx_hp
        self.Hp = Hp
        self.D_hp = D_hp
        self.T = T
        if len(sostav) == 0:
            self.s = False
        else:
            self.s = True
            self.sostav = sostav

    def d_self(self):
        for i, j in enumerate(self.sostav):
            if j.Hp <= 0:
                self.Hp -= j.D_HP
                del self.sostav[i]

    def damage(self, d):
        if self.s:
            random.choice(self.sostav).damage(max(d - self.T, 0))
            self.d_self()
            self.Hp -= max(d - self.T, 0)
        else:
            self.Hp -= max(d - self.T, 0)

class Cycle:
    def __init__(self, *args, now=0):
        self.now = now
        self.lst = list(args)
        self.ln = len(self.lst)
        
    def get(self):
        c = self.lst[self.now]
        self.now += 1
        if self.now == self.ln:
            self.now = 0
        return c
    def append(self, a):
        self.lst.append(a)

class entity:
    def __init__(self, name, KeyWords, png):
        self.name = name
        self.png = png
        self.KeyWords = KeyWords



class mob(entity):
    def __init__(self, name, KeyWords, png, Hp, Mx_Hp, stats, use, in_hand, inventory, Hates, abilitis, els):
        super().__init__(name, KeyWords,  png)
        self.Hp = Hp
        self.Mx_Hp = Mx_Hp
        self.stats = stats
        self.use = use
        self.in_hand = in_hand
        self.inventory = inventory
        self.Hates = Hates
        self.abilitis = abilitis
        self.els = els
        self.pricas = deque()
        self.agr = False

class Thing(entity):
    def __init__(self, name, KeyWords, png, inv):
        super().__init__(name, KeyWords, png)
        self.inv = inv








class p_block(block):
    def __init__(self, real, png, give, name, can_walk, crisha, father):
        super().__init__(real, png, give, name, can_walk, crisha)
        self.father = father

    def give_blocks(self, ert):
        return ert[self.father]


class f_block(block):
    def __init__(self, real, png, give, name, can_walk, crisha, sons):
        super().__init__(real, png, give, name, can_walk, crisha)
        self.sons = sons

    def give_blocks(self, ert):
        return self.sons

class Biome:
    def __init__(self, name, lamb, blo, bereg, voda, verh):
        self.lamb = lamb
        self.blo = blo
        self.name = name
        self.bereg = bereg
        self.voda = voda
        self.verh = verh
        self.ln = len(blo)

    def __str__(self):
        return self.name

class Claster:
    def __init__(self, name, biomes, temp, land, gor, elser):
        self.name = name
        self.biomes = biomes
        self.temp = temp
        self.land = land
        self.gor = gor
        self.elser = elser

    def give_blocks(self, x, y):
        t = self.temp[x, y]
        l = self.land[x, y]
        g = self.gor[x, y]
        for bio in self.biomes:
            if bio.lamb(t, l, g):
                return bio.blo, bio.bereg, bio.voda, bio.verh, bio
        return self.elser.blo, self.elser.bereg, self.elser.voda, self.elser.verh, self.elser





class Weapon:
    def __init__(self, name, png, damage, energy, shtraf, abil):
        self.name = name
        self.png = png
        self.damage = damage
        self.energy = energy
        self.shtaf = shtraf
        self.abil = abil

class Blij(Weapon):
    def __init__(self, name, png, damage, energy, shtraf, abil, block):
        super.__init__(name, png, damage, energy, shtraf, abil)
        self.block = block

class Dal(Weapon):
    def __init__(self, name, png, damage, energy, shtraf, abil, rang):
        super.__init__(name, png, damage, energy, shtraf, abil)
        self.rang = rang


