import math

def argmin(f, input):
    bestValSoFar = None
    bestArgSoFar = None
    count = 0
    for x in input:
        val = f(x)
        if bestValSoFar is None or  bestValSoFar > val:
            bestValSoFar = val
            bestArgSoFar = count
        count += 1
    return bestValSoFar, bestArgSoFar

def floatRange(lo, hi, stepSize):
    ret = []
    val = lo
    while True:
        ret.append(val)
        if val + stepSize < hi:
            val += stepSize
        else:
            break
    return ret

def periodPole(pole):
    polar_pole = complexPolar(pole)
    if isinstance(pole, complex) and (2*math.pi/(polar_pole[1]) - int(2*math.pi/(polar_pole[1]))) < 1e-8:
        return 2*math.pi/(polar_pole[1])
    else:
        return None

def complexPolar(p):
    if isinstance(p, complex):
        return (abs(p), math.atan2(p.imag, p.real))
    else:
        if p < 0:
            return (-p, math.pi)
        else:
            return (p, 0.0)
