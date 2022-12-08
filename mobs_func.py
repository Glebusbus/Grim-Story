
from func import *

def walk(ert, matrix, mobs, things, p_things, b, xyz, option):
    x, y, z = xyz
    xk, yk = option
    if 0<=x+xk<=b-1 and 0<=y+yk<=b-1:
        if not(ert[x + xk, y + yk, z].real):
            if ert[x + xk, y + yk, z - 1].real and not mobs.get((x + xk, y + yk, z), False):

                mobs[x + xk, y + yk, z] = mobs.pop(xyz)
                return True
            elif ert[x + xk, y + yk, z - 2].real and not mobs.get((x + xk, y + yk, z-1), False):

                mobs[x + xk, y + yk, z - 1] = mobs.pop(xyz)
                return True
        elif not(ert[x + xk, y + yk, z + 1].real) and not mobs.get((x + xk, y + yk, z+1), False):

            mobs[x + xk, y + yk, z + 1] = mobs.pop(xyz)
            return True
    return False



def random_walk(ert, matrix, mobs, things,  p_things, b, xyz, option):
    xk, yk = random.randint(-1, 1), random.randint(-1, 1)
    return walk(ert, matrix, mobs, things,  p_things, b, xyz, (xk, yk))

def stay(ert, matrix, mobs, things, p_things, b, xyz, option):
    return True


def take(ert, matrix, mobs, things,  p_things, b, xyz, option):
    if things.get(xyz, False):
        mobs[xyz].inventory.append(things[xyz])
        del things[xyz]
    return True

def sbros(ert, matrix, mobs, things,  p_things, b, xyz, option):
    xs, ys, zs = xyz
    sh = int(len(mobs[xyz].inventory) ** 0.5) + 1
    for x in range(-sh//2, sh//2+1):
        for y in range(-sh//2, sh//2+1):
            zh = Z_get(ert, xs+x, ys+y )
            if not things.get((xs+x, ys+y, zh), False):
                if len(mobs[xyz].inventory) >=1:
                    things[xs+x, ys+y, zh] = mobs[xyz].inventory.pop(0)
                else:
                    return True
    return True



