import operator
import lib601.util as util

#-----------------------------------------------------------------------------

class DDist:
    """
    Discrete distribution represented as a dictionary.  Can be
    sparse, in the sense that elements that are not explicitly
    contained in the dictionary are assumed to have zero probability.
    """
    def __init__(self, dictionary):
        self.d = dictionary
        """ Dictionary whose keys are elements of the domain and values
        are their probabilities. """

    def dictCopy(self):
        """
        @returns: A copy of the dictionary for this distribution.
        """
        return self.d.copy()

    def prob(self, elt):
        """
        @param elt: an element of the domain of this distribution
        (does not need to be explicitly represented in the dictionary;
        in fact, for any element not in the dictionary, we return
        probability 0 without error.)
        @returns: the probability associated with C{elt}
        """
        if self.d.has_key(elt):
            return self.d[elt]
        else:
            return 0

    def support(self):
        """
        @returns: A list (in arbitrary order) of the elements of this
        distribution with non-zero probabability.
        """
        return [k for k in self.d.keys() if self.prob(k) > 0]

    def __repr__(self):
        if len(self.d.items()) == 0:
            return "Empty DDist"
        else:
            dictRepr = reduce(operator.add,
                              [util.prettyString(k)+": "+\
                               util.prettyString(p)+", " \
                               for (k, p) in self.d.items()])
            return "DDist(" + dictRepr[:-2] + ")"
    __str__ = __repr__

#-----------------------------------------------------------------------------

def incrDictEntry(d, k, v):
    """
    If dictionary C{d} has key C{k}, then increment C{d[k]} by C{v}.
    Else set C{d[k] = v}.
    
    @param d: dictionary
    @param k: legal dictionary key (doesn't have to be in C{d})
    @param v: numeric value
    """
    if d.has_key(k):
        d[k] += v
    else:
        d[k] = v


#-----------------------------------------------------------------------------

def squareDist(lo,hi, loLimit=None, hiLimit=None):
    probDic = {}
    prob = 1.0 / (hi-lo)
    for value in range(lo, hi, 1):
        if loLimit and value < loLimit:
            probDic[loLimit] = probDic.get(loLimit, 0)+prob
        elif hiLimit and value > hiLimit:
            probDic[hiLimit] = probDic.get(hiLimit, 0)+prob
        else:
            probDic[value] = probDic.get(value, 0) + prob
    return DDist(probDic)

# print(squareDist(2, 5, 0, 10))
# print(squareDist(2, 5, 4, 10))
# print(squareDist(2, 5, 3, 10))
# print(squareDist(2, 15, 6, 10))

def triangleDist(peak, halfWidth, loLimit=None, hiLimit=None):
    prob = 1./halfWidth # math deductive
    lo = peak - halfWidth + 1
    hi = peak + halfWidth
    probDic = {}
    for value in range(lo, hi, 1):
        portion = (halfWidth - abs(peak - value))*1./halfWidth
        this_prob = prob * portion
        if loLimit and value < loLimit:
            probDic[loLimit] = probDic.get(loLimit, 0.) + this_prob
        elif hiLimit and value > hiLimit:
            probDic[hiLimit] = probDic.get(hiLimit, 0.) + this_prob
        else:
            probDic[value] = probDic.get(value, 0.) + this_prob
    return DDist(probDic)

print(triangleDist(5, 3, 0, 10))
print(triangleDist(5, 3, 4, 10))
print(triangleDist(5, 3, 5, 10))
print(triangleDist(5, 3, 6, 10))

class MixtureDist:
    def __init__(self, d1, d2, p):
        # your code here
        probDic = {}
        vals = set(d1.support())
        vals.update(set(d2.support()))
        for value in vals:
            probDic[value] = p*d1.prob(value)+(1.-p)*d2.prob(value)
        self.d = DDist(probDic)

    def prob(self, elt):
        # your code here
        return self.d.prob(elt)

    def support(self):
        # your code here
        return self.d.support()

    def __str__(self):
        result = 'MixtureDist({'
        elts = self.support()
        for x in elts[:-1]:
            result += str(x) + ' : ' + str(self.prob(x)) + ', '
        result += str(elts[-1]) + ' : ' + str(self.prob(elts[-1])) + '})'
        return result
    
    __repr__ = __str__

print(MixtureDist(squareDist(2, 6), squareDist(4, 8), 0.5))








#-----------------------------------------------------------------------------
# If you want to plot your distributions for debugging, put this file
# in a directory that contains lib601, and where that lib601 contains
# sig.pyc.  Uncomment all of the following.  Then you can plot a
# distribution with something like:
# plotIntDist(MixtureDist(squareDist(2, 6), squareDist(4, 8), 0.5), 10)

import lib601.sig as sig

class IntDistSignal(sig.Signal):
    def __init__(self, d):
        self.dist = d
    def sample(self, n):
        return self.dist.prob(n)
def plotIntDist(d, n):
    IntDistSignal(d).plot(end = n, yOrigin = 0)

plotIntDist(MixtureDist(squareDist(2, 6), squareDist(4, 8), 0.5), 10)

