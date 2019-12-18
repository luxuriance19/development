"""
Class and some supporting functions for representing and manipulating system functions. 
"""

import math
import lib601.poly as poly
import lib601.util as util


class SystemFunction:
    """
    Represent a system function as a ratio of polynomials in R
    """
    def __init__(self, numeratorPoly, denominatorPoly):
        self.numerator = numeratorPoly
        self.denominator = denominatorPoly

    def poles(self):
        reverDe = self.denominator.coeffs[:]
        reverDe.reverse()
        new_poly = poly.Polynomial(reverDe)
        return new_poly.roots()

    def poleMagnitudes(self):
        poles = self.poles()
        return list(map(abs, poles))

    def dominantPole(self):
        poles = self.poles()
        dominantPole = util.argmax(poles, abs)
        return dominantPole


    def __str__(self):
        return 'SF(' + self.numerator.__str__('R') + \
               '/' + self.denominator.__str__('R') + ')'

    __repr__ = __str__


def Cascade(sf1, sf2):
    d1 = sf1.denominator
    n1 = sf1.numerator
    d2 = sf2.denominator
    n2 = sf2.numerator
    casD = d1*d2
    casN = n1*n2
    return SystemFunction(casN, casD)


def FeedbackSubtract(sf1, sf2=None):
    # n1d2/(d1d2+n1n2)
    numerator = sf1.numerator*sf2.denominator
    denominator = sf1.numerator*sf2.numerator+sf1.denominator*sf2.denominator
    return SystemFunction(numerator, denominator)


if __name__== "__main__":
    polys = poly.Polynomial([64,16*8,63])
    print polys.roots()
