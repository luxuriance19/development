from lib601 import sm

class NN:
    def __init__(self):
        self.n = 0
    def get(self):
        self.n += 1
        return str(self.n)

    def reset(self):
        self.n = 0

class NS(NN):
    def get(self, s):
        return s + NN.get(self)

def add(a, b):
    print a, b
    if b == 0:
        return a
    else:
        return add(a, b-1)+1

def sub(a,b):
    if b == 0:
        return a
    else:
        return sub(a, b-1) - 1

def slowMod(a, b):
    if a >= b:
        return slowMod(a-b, b)
    elif a >= 0:
        return a

# print(add(3,5))
# print sub(3, 10)
# print slowMod(23, 13)
class CountingStateMachine(sm.SM):
    def __init_(self):
        self.startState = 0
    def getOutput(self, state, inp):
        return state + 1
    def getNextValue(self, state, inp):
        return (state+1, self.getOutput(state, inp))

class AlternateZeros(CountingStateMachine):
    def getOutput(self, state, inp):
        if not state % 2:
            return inp
        else:
            return 0

a = CountingStateMachine()
a.getNextValue(0, 1)

if __name__=="__main__":
    foo = NS()
    print foo.get('a')
    print foo.get('b')
    print foo.get('c')
