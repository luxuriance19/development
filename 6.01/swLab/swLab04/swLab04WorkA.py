import lib601.poly as poly
import lib601.sig
from lib601.sig import *
from swLab04SignalDefinitions import *

## You can evaluate expressions that use any of the classes or
## functions from the sig module (Signals class, etc.).  You do not
## need to prefix them with "sig."

s = UnitSampleSignal()
s.plot(-5, 5)

def samplesInRange(signal, lo, hi):
    return [signal.sample(i) for i in range(lo,hi)]

step1 = Rn(ScaledSignal(StepSignal(),3),3)
#step1.plot(-5,5)
print samplesInRange(step1, -5, 5)
step2 = SummedSignal(Rn(step1,5),ConstantSignal(-3))
#step2.plot(-10,10)
print samplesInRange(step2, -10, 10)
stepUpDown = SummedSignal(step1,SummedSignal(Rn(step1,4),ConstantSignal(-3)))
# stepUpDown.plot(-10,10)
p = poly.Polynomial([5,0,3,0,1,0])
stepUpDownPoly = polyR(UnitSampleSignal(),p)
stepUpDownPoly1 = polyRRec(UnitSampleSignal(),p)
stepUpDownPoly.plot(0,10)
print samplesInRange(stepUpDownPoly, 0, 10)
print samplesInRange(stepUpDownPoly1, 0,10)