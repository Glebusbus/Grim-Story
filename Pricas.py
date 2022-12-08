from mobs_const import *

def Find_resurs(ert, matrix, mobs, things, p_things, b, xyz, option):
    st = xyz
    for th, co in option[:-1]:

        for j in range(co):
            way = find_thing(st, matrix, p_things, b, th)
            if way:
                xpr, ypr, z = st
                for x, y, z in way[1:]:
                    mobs[xyz].pricas.append((walk, (x - xpr, y - ypr)))
                    xpr, ypr = x, y
                mobs[xyz].pricas.append((take, 0))
                del p_things[way[-1]]
                st = way[-1]
            else:
                break
        xpr, ypr, z = st
        xk, yk = option[-1]
        way = A_star((xpr, ypr, Z_get(ert, xpr, ypr)), (xk, yk, Z_get(ert, xk, yk)), matrix, b, evrei_manhent)
        if way:

            for x, y, z in way[1:]:
                mobs[xyz].pricas.append((walk, (x - xpr, y - ypr)))
                xpr, ypr = x, y
            mobs[xyz].pricas.append((sbros, 0))


