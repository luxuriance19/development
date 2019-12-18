#### 4.3.3

import lib601.sm as sm

def accumulator(init):
    # y[n] = x[n] + y[n-1]
    return sm.FeedbackAdd(sm.Gain(1), sm.R(init))

def accumulatorDelay(init):
    return sm.Cascade(accumulator(init), sm.R(init))

def accumulatorDelayScaled(s, init):
    return sm.Cascade(accumulatorDelay(init), sm.Gain(s))


### 4.3.5
# To check the designLab
def controller(k):
    ## return v, k*error
    return sm.Gain(k)

def plant(T, initD):
    return sm.FeedbackAdd(sm.Gain(-T), sm.R(initD))

def wallFinderSystem(T, initD, k):
    return sm.Cascade(controller(k), plant(T, initD))


'''
We have defined a special class of state machines, called LTISM , that can be used to
easily implement any machine in this class. The initializer is
LTISM(dCoeffs, cCoeffs, previousInputs, previousOutputs)
where dCoeffs
is a list of the coefficients
through , x, in that order.

cCoeffs is a list of the coefficients
 through y
, in that order.

previousInputs is a list of

through
, in that order.

previousOutputs is a list of

through
, in that order.
'''
def dotProd(a, b):
    if len(a) == 0 or len(b) == 0: return 0
    if len(a) != len(b):
        print 'dotPord mismatch error' + str(len(a)) + '!=' + str(len(b))
    return sum([ai*bi for (ai, bi) in zip(a, b)])

class LTISM(sm.SM):
    def __init__(self, dCoeffs, cCoeffs, previousInputs=[], previousOutputs=[]):
        self.cCoeffs = cCoeffs
        self.dCoeffs = dCoeffs
        self.cMaxR = len(cCoeffs)
        self.dMaxR = len(dCoeffs)-1
        # State is last j input values and last k output values
        self.startState = (previousInputs, previousOutputs)

    def getNextValues(self, state, input):
        (inputs, outputs) = state
        inputs = [input] + inputs
        output = dotProd(self.dCoeffs, inputs[:self.dMaxR+1])+\
                 dotProd(self.cCoeffs, outputs[:self.cMaxR])
        outputs = [output]+outputs
        nextState = (inputs[:-1], outputs[:-1])
        return (nextState, output)

m = LTISM([1,2], [1], [3], [4])
print m.transduce([1,2,3,4,5])

##### 4.4.3  transducedSignal
import lib601.sig as sig
import lib601.poly as poly
from swLab04SignalDefinitions import *

def samplesInRange(sig, lo, hi):
    return [sig.sample(i) for i in range(lo, hi)]

class TransducedSignal(sig.Signal):
    def __init__(self, s, m):
        self.s = s
        self.m = m
        self.storeOutput = []

    def sample(self, n):
        if n < 0:
            return 0
        else:
            if n >= len(self.storeOutput):
                Updated = self.m.transduce(samplesInRange(self.s, 0, n+1))
                # print(Updated)
                self.storeOutput = Updated
            # print("length", len(self.storeOutput))
            return self.storeOutput[n]

siga = [100 if i in [0, 20, 50] else 0 for i in range(61)]
print siga
p = poly.Polynomial(siga[::-1])
import lib601.sig
inputSig = polyR(UnitSampleSignal(),p)
inputSig1 = sig.polyR(UnitSampleSignal(), p)
print samplesInRange(inputSig, 0, 61)
print samplesInRange(inputSig1, 0, 61)
sm = LTISM([1], [0.99], [], [0])
newSig = TransducedSignal(inputSig, sm)
for i in range(0, 61, 10):
    print newSig.sample(i)

### quiz
class Triangle(Signal):
    def __init__(self, h):
        self.h = h
    def sample(self, n):
        if -self.h < n < self.n:
            return self.h - abs(n)
        return 0

'''
trapezoid : the signal is equal to
0 for n <= 0
1 for n=1
2 for 2<=n<=6
1 for n=7
0 for n>= 8

ConstantSignal , UnitSampleSignal , CosineSignal , StepSignal , SummedSignal ,
ScaledSignal , R , Rn
'''
trapezoid = SummedSignal(Rn(Triangle(4),4),-1*Rn(Triangle(2),4))
trapezoid1 = Rn(SummedSignal(Triangle(4), -1*Triangle(2)), 4)

# trapezoid = SummedSignal(SummedSignal(Rn(Triangle(2),2),
# Rn(Triangle(2),4)),
# Rn(Triangle(2),6))
# Another way of doing it.
#trapezoid = polyR(Triangle(2), poly.Polynomial([1, 0, 1, 0, 1, 0, 0]))



