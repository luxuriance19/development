'''3-1-1'''

from lib601 import sm

def run(self, n=100):
    return self.transduce([None]*n)

class Delay(sm.SM):
    def __init__(self, v0):
        self.startState = v0

    def getNextValues(self, state, inp):
        # Output is old state
        return (inp, state)

class Increment(sm.SM):
    startState = 0
    def __init__(self, incr):
        self.incr = incr

    def getNextValues(self, state, inp):
        # print(type(inp))
        # print type(self.incr)
        if isinstance(inp, type(2)):
            return (state, inp + self.incr)  # need safe add
        else:
            return (state, self.incr)

sm1 = Delay(1)
sm2 = Delay(2)
c = sm.Cascade(sm1, sm2)
print c.transduce([3,5,7,9])

sm1 = Delay(1)
sm2 = Increment(3)
c = sm.Cascade(sm1, sm2)
print c.transduce([3,5,7,9])

'''3-1-2'''
class Cascade(sm.SM):
    def __init__(self, sm1, sm2):
        self.startState = (sm1.startState, sm2.startState)
        self.sm1 = sm1
        self.sm2 = sm2

    def getNextValues(self, state, inp):
        s1, s2 = state if state else self.startState
        _s1, o1 = self.sm1.getNextValues(s1, inp)
        _s2, o2 = self.sm2.getNextValues(_s1, o1)
        return ((_s1, _s2), o2)

# test
sm1 = Delay(1)
sm2 = Delay(2)
c = Cascade(sm1, sm2)
print c.transduce([3,5,7,9], verbose=True)

'''3-1-3'''
class PureFunction(sm.SM):
    def __init__(self, f):
        self.startState = 0
        self.func = f
    def getNextValues(self, state, inp):
        return (state, self.func(inp))

'''3-1-4'''
class BA1(sm.SM):
	startState = 0
	def getNextValues(self, state, inp):
		if inp != 0:
			newState = state * 1.02 + inp - 100
		else:
			newState = state * 1.02
		return (newState, newState)

class BA2(sm.SM):
	startState = 0
	def getNextValues(self, state, inp):
		newState = state * 1.01 + inp
		return (newState, newState)

## return the max number of the two balance counter

ba1 = BA1()
ba2 = BA2()
maxAccount = sm.Cascade(sm.Parallel(ba1, ba2), PureFunction(max))

print maxAccount.transduce([100,200,20,3000], verbose=True)

## deposit or withdraw >3000 choose BA1, else choose BA2
def depositB(inp):
    if abs(inp) > 3000:
        return (inp, 0)
    else:
        return (0, inp)

swithAccount = sm.Cascade(sm.Cascade(PureFunction(depositB), sm.Parallel2(ba1, ba2)), PureFunction(sum))

## all in state machine
class Switch(sm.SM):
    startState = 0
    def getNextValues(self, state, inp):
        if abs(inp) > 3000:
            return (state, (inp, 0))
        else:
            return (state, (0, inp))
# def add(balances):
# 	return sum(balances)

swithAccount1 = sm.Cascade(Switch(), sm.Cascade(sm.Parallel2(ba1, ba2), PureFunction(sum)))


print swithAccount.transduce([3000,200,1000,5000], verbose=True)
print '*'*80
print swithAccount1.transduce([3000,200,1000,5000], verbose=True)

'''3-1-5'''
# terminate the stateMachine
class SumTSM(sm.SM):
    startState = 0
    # def __init__(self):
    #     self.startState = 0
    def getNextValues(self, state, inp):
        return (state+inp, state+inp)
    def done(self, state):
        return state > 100

print SumTSM().transduce([1,10,50,40,20])


### repeat times
fourTimes = sm.Repeat(SumTSM(), 4)

print fourTimes.transduce(range(100), verbose=True)

class ConsumeFiveValues(sm.SM):
    startState = (0, 0)
    # count, total
    def getNextValues(self, state, inp):
        (count, total) = state
        if count == 4:
            return ((count + 1, total + inp), total + inp)
        else:
            return ((count + 1, total + inp), None)

    def done(self, state):
        (count, total) = state
        return count == 5

print sm.Repeat(ConsumeFiveValues(), 3).transduce(range(100))


class CountUpTo(sm.SM):
    def __init__(self, n):
        self.n = n
        self.startState = 0

    def getNextValues(self, state, inp):
        return (state+1, state+1)

    def done(self, state):
        return state==self.n

print CountUpTo(3).run(20)


### sequence
def makeSequenceCounter(nums):
    smList = []
    for num in nums:
        smList.append(CountUpTo(num))
    return sm.Sequence(smList)

print makeSequenceCounter([2,5,3]).run(n=20)


'''3-1-6 Feedback SM'''
def makeCounter(init, step):
    return sm.Feedback(sm.Cascade(Increment(step), Delay(init)))
# feedback undefined
print makeCounter(3, 2).run(verbose=True)


negate = sm.PureFunction(lambda x:not x)
alternating = sm.Feedback(sm.Cascade(negate, sm.Delay(True)))

# print alternating.transduce(range(100),verbose=True)
print alternating.transduce(range(100))



'''3-3-1 mapList'''
def mapList(func, inps):
    return [func(x) for x in inps]

def sq(x): return x*x
print mapList(sq, [1,2,3,4])


def sumAbs(inps):
    return sum(mapList(abs, inps))
print sumAbs([1,2,-2,3])

def mapSquare(func, inps):
    return [[func(x, y) for y in inps] for x in inps]
def diff(x, y): return x - y
print mapSquare(diff, [1,2,3])

'''3.3.2 indexNestList'''
def recursiveRef(nestedList, indexL):
    if len(indexL) == 1:
        return nestedList[indexL[0]]
    else:
        return recursiveRef(nestedList[indexL[0]], indexL[1:])

def recursiveRef1(nestedList, indexL):
    if indexL:
        return recursiveRef1(nestedList[indexL[0]], indexL[1:])
    else:
        return nestedList

nested = \
[[[1, 2],

3],

[4,

[5, 6]],

7,

[8, 9, 10]]

print recursiveRef(nested, [1,1])
nested = \
[[[1, 2],

3],

[4,

[5, 6]],

7,

[8, 9, 10]]
print recursiveRef1(nested, [1,1])
print nested