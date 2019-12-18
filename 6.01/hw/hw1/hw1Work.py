import pdb
import lib601.sm as sm
import string
import operator

class BinaryOp:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return self.opStr + '(' + \
               str(self.left) + ', ' +\
               str(self.right) + ')'

    __repr__ = __str__

    def eval(self, env):
        lhs = self.left.eval(env)
        rhs = self.right.eval(env)
        if isNum(lhs) and isNum(rhs):
            return self.op(lhs, rhs)
        else:
            # this is different with the line with the assign eval(), with eval() one we should uncomment this
            # lhs = Number(lhs) if isNum(lhs) else lhs
            # rhs = Number(rhs) if isNum(rhs) else rhs
            return self.__class__(lhs, rhs)
        # else:
        #     return self
        # else:
        #     self.left = Number(lhs) if isNum(lhs) else lhs
        #     self.right = Number(rhs) if isNum(rhs) else rhs
        #     return self

class Sum(BinaryOp):
    opStr = 'Sum'
    op = operator.add

class Prod(BinaryOp):
    opStr = 'Prod'
    op = operator.mul

class Quot(BinaryOp):
    opStr = 'Quot'
    op = operator.div

class Diff(BinaryOp):
    opStr = 'Diff'
    op = operator.sub

class Assign(BinaryOp):
    opStr = 'Assign'

    def eval(self, env):
        # print("***", self.right)
        env[self.left.name] = self.right #.eval(env)
        # for key, value in env.items():
        #     parseTree =
        #     env[key] = value.eval(env)
        
class Number:
    def __init__(self, val):
        self.value = val
    def __str__(self):
        return 'Num('+str(self.value)+')'
    __repr__ = __str__

    def eval(self, env):
        return self.value

# def reverseParse(evalStr):
#     def reverseExp(index):
#         if reverseExp(index)

class Variable:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'Var('+self.name+')'
    __repr__ = __str__
    def eval(self, env):
        if self.name in env:
            value = env[self.name]
            if not isNum(value):
                # print("value", value)
                # env[self.name] = value.eval(env)
                return value.eval(env)
            else:
                return value

        else:
            return self

# characters that are single-character tokens
seps = ['(', ')', '+', '-', '*', '/', '=']

#Convert strings into a list of tokens (strings)
def tokenize(string):
    # <your code here>
    tokens = []
    this = ""
    for char in string:
        if char in seps:
            if this.strip():
                tokens.append(this.strip())
            tokens.append(char)
            this = ""
        elif char == ' ':
            if this.strip():
                tokens.append(this.strip())
            this = ""
        else:
            this += char
    if this.strip():
        tokens.append(this.strip())
    return tokens


# tokens is a list of tokens
# returns a syntax tree:  an instance of {\tt Number}, {\tt Variable},
# or one of the subclasses of {\tt BinaryOp} 
def parse(tokens):
    def parseExp(index):
        # <your code here>
        if index > len(tokens):
            return
        token = tokens[index]
        if numberTok(token):
            return Number(float(token)), index+1
        elif variableTok(token):
            return Variable(token), index+1
        elif token == '(':
            lt, nextIdx = parseExp(index+1)
            op = tokens[nextIdx]
            rt, nextIdx = parseExp(nextIdx+1)
            if op == "+":
                op = Sum(lt, rt)
            elif op == "-":
                op = Diff(lt, rt)
            elif op == "*":
                op = Prod(lt, rt)
            elif op == "/":
                op = Quot(lt, rt)
            elif op == "=":
                op = Assign(lt, rt)
            return op, nextIdx + 1
    (parsedExp, nextIndex) = parseExp(0)
    return parsedExp

# token is a string
# returns True if contains only digits
def numberTok(token):
    for char in token:
        if not char in string.digits: return False
    return True

# token is a string
# returns True its first character is a letter
def variableTok(token):
    for char in token:
        if char in string.letters: return True
    return False

# thing is any Python entity
# returns True if it is a number
def isNum(thing):
    return type(thing) == int or type(thing) == float

# Run calculator interactively
def calc():
    env = {}
    while True:
        e = raw_input('%')            # prints %, returns user input
        # print '%', # your expression here
        tokens = tokenize(e)
        parseT = parse(tokens)
        ret = parseT.eval(env)
        if ret:
            print ret
        print '   env =', env

class Tokenizer(sm.SM):
    startState = ("","")
    def getNextValues(self, state, inp):
        if inp in seps or inp == ' ':
            s0, s1 = state
            o = ""
            if s0.strip():
                o = s0.strip()
                s0 = ""
            elif s1.strip():
                o = s1.strip()
                s1 = ""
            s1 = inp.strip()
            return (s0, s1), o
        else:
            s0, s1 = state
            s0 += inp
            # print("***",s1)
            if s1:
                return (s0, ""), s1
            else:
                return (s0, s1), ""

    def tokenize(self, inputString):
        tokens = self.transduce(inputString)
        ret = []
        for _str in tokens:
            if _str:
                ret.append(_str)
        return ret


# print Tokenizer().transduce('fred ')
# print Tokenizer().transduce('777 ')
# print Tokenizer().transduce('777 hi 33 ')
# print Tokenizer().transduce('**-)( ')
# print Tokenizer().transduce('(hi*ho) ')
# print Tokenizer().transduce('(fred + george) ')

# print Tokenizer().tokenize('fred ')
# print Tokenizer().tokenize('777 ')
# print Tokenizer().tokenize('777 hi 33 ')
# print Tokenizer().tokenize('**-)( ')
# print Tokenizer().tokenize('(hi*ho) ')
# print Tokenizer().tokenize('(fred + george) ')




# exprs is a list of strings
# runs calculator on those strings, in sequence, using the same environment
def calcTest(exprs):
    env = {}
    for e in exprs:
        print '%', e                    # e is the experession 
        print parse(tokenize(e)).eval(env)
        print '   env =', env

# Simple tokenizer tests
'''Answers are:
['fred']
['777']
['777', 'hi', '33']
['*', '*', '-', ')', '(']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
'''
def testTokenize():
    print tokenize('fred ')
    print tokenize('777 ')
    print tokenize('777 hi 33 ')
    print tokenize('**-)(')
    print tokenize('( hi * ho )')
    print tokenize('(fred + george)')
    print tokenize('(hi*ho)')
    print tokenize('( fred+george )')

# testTokenize()


# Simple parsing tests from the handout
'''Answers are:
Var(a)
Num(888.0)
Sum(Var(fred), Var(george))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Assign(Var(a), Prod(Num(3.0), Num(5.0)))
'''
def testParse():
    print parse(['a'])
    print parse(['888'])
    print parse(['(', 'fred', '+', 'george', ')'])
    print parse(['(', '(', 'a', '*', 'b', ')', '/', '(', 'cee', '-', 'doh', ')' ,')'])
    print parse(tokenize('((a * b) / (cee - doh))'))
    print parse(tokenize('(a = (3 * 5))'))

# testParse()

####################################################################
# Test cases for EAGER evaluator
####################################################################

def testEval():
    env = {}
    Assign(Variable('a'), Number(5.0)).eval(env)
    print Variable('a').eval(env)
    env['b'] = 2.0
    print Variable('b').eval(env)
    env['c'] = 4.0
    print Variable('c').eval(env)
    print Sum(Variable('a'), Variable('b')).eval(env)
    print Sum(Diff(Variable('a'), Variable('c')), Variable('b')).eval(env)
    Assign(Variable('a'), Sum(Variable('a'), Variable('b'))).eval(env)
    print Variable('a').eval(env)
    print env

# testEval()

# Basic calculator test cases (see handout)
testExprs = ['(2 + 5)',
             '(z = 6)',
             'z',
             '(w = (z + 1))',
             'w'
             ]
# calcTest(testExprs)

####################################################################
# Test cases for LAZY evaluator
####################################################################

# Simple lazy eval test cases from handout
'''Answers are:
Sum(Var(b), Var(c))
Sum(2.0, Var(c))
6.0
'''
def testLazyEval():
    env = {}
    Assign(Variable('a'), Sum(Variable('b'), Variable('c'))).eval(env)
    print Variable('a').eval(env)
    env['b'] = Number(2.0)
    print Variable('a').eval(env)
    env['c'] = Number(4.0)
    print Variable('a').eval(env)

# Lazy partial eval test cases (see handout)
lazyTestExprs = ['(a = (b + c))',
                  '(b = ((d * e) / 2))',
                  'a',
                  '(d = 6)',
                  '(e = 5)',
                  'a',
                  '(c = 9)',
                  'a',
                  '(d = 2)',
                  'a']
calcTest(lazyTestExprs)

## More test cases (see handout)
partialTestExprs = ['(z = (y + w))',
                    'z',
                    '(y = 2)',
                    'z',
                    '(w = 4)',
                    'z',
                    '(w = 100)',
                    'z']

calcTest(partialTestExprs)
