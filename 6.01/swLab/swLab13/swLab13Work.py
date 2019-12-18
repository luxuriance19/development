import lib601.search as search
import lib601.sm as sm

# Indices into the state tuple.
# (farmer, goat, wolf, cabbage) = range(4)
LocIdx = dict(zip(('Farmer', 'Goat', 'Wolf', 'Cabbage'), range(4)))
transState = {'L':'R', 'R':'L'}

def changeState(state):
    return transState[state]

class FarmerGoatWolfCabbage(sm.SM):
    startState = ('L', 'L', 'L', 'L')
    legalInputs = ['takeNone','takeGoat','takeWolf','takeCabbage']
    def getNextValues(self, state, action):
        moveTarget = LocIdx.get(action[4:], 0)
        now_state = list(state)
        now_state[moveTarget] = changeState(now_state[moveTarget])
        if moveTarget:
           now_state[0] = changeState(now_state[0])
        return tuple(now_state), None

    def done(self, state):
        return state == ('R', 'R', 'R', 'R')
  
sm = FarmerGoatWolfCabbage()
sm.transduce(['takeGoat','takeNone','takeNone'],verbose = True)

class RobotMoves(sm.SM):
    legalInputs = ['left','right','down','up']
    def __init__(self):
        self.end_state = (3, 4)
    def getNextValues(self, state, inp):
        assert inp in RobotMoves.legalInputs, "the input action must be one of {0}".\
            format(', '.join(RobotMoves.legalInputs))
        statex, statey = state
        if inp == 'left':
            statex -= 1
        elif inp == 'right':
            statex += 1
        elif inp == 'down':
            statey -= 1
        else:
            statey += 1
    def done(self, state):
        return state == self.end_state

class KnightMoves(sm.SM):
    # knight has eight move, 2: 2 up and 1 left or right, 2: 2 left and 1 up or down,
    # 2: 2 right and 1 up or down, 2: 2 down and 1 left or right
    actions = {'TopLeft':{'up':2, 'left':1}, 'TopRight':{'up':2,'right':1},\
               'LeftUp':{'up':1, 'left':2}, 'RightUp':{'up':1, 'right':1},\
               'LeftDown':{'down':1, 'left':2},'RightDown':{'down':1, 'right':1},
               'BottomLeft':{'down':2, 'left':1}, 'BottomRight':{'down':2,'right':1}}
    legalInputs = ['TopLeft', 'TopRight', 'LeftUp', 'RightUp', 'LeftDown', 'RightDown', 'BottomLeft', 'BottomRight']
    def __init__(self):
        self.final_state = (7,7)

    def stateReason(self, statex):
        if statex < 0:
            return 0
        if statex > 7:
            return 7

    def transState(self, state, moves):
        statex, statey = state
        for key, value in moves.items():
            if key == 'up':
                statey += value
            elif key == 'down':
                statey -= value
            elif key == 'left':
                statex -= value
            elif key == 'right':
                statex += value
            statex = self.stateReason(statex)
            statey = self.stateReason(statey)
        return (statex, statey)

    def getNextValues(self, state, inp):
        assert inp in self.legalInputs, "the input action is not right"
        moves = self.actions.get(inp)
        new_state = self.transState(state, moves)
        return new_state, new_state

    def done(self, state):
        return state == self.final_state