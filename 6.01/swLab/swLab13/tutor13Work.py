import lib601.search as search
import lib601.sm as sm

# search(initialState, goalTest, actions, successor, depthFirst=False, DP=True, maxNodes=10000)
# Returns: path from initial state to a goal state as a list of (action, state) tuples

search.verbose = True

######################################################################
###
###  Map1 in notes
###
######################################################################

map1 = {'S' : ['A', 'B'],
        'A' : ['S', 'C', 'D'],
        'B' : ['S', 'D', 'E'],
        'C' : ['A', 'F'],
        'D' : ['A', 'B', 'F', 'H'],
        'E' : ['B', 'H'], 
        'F' : ['C', 'D', 'G'],
        'H' : ['D', 'E', 'G'],
        'G' : ['F', 'H']}

def map1successor(state, action):
    '''
    action is integer
    :param state: parent state
    :param action: action move
    :return:
    '''
    if action < len(map1[state]):
        return map1[state][action]
    else:
        return state

actions = range(max([len(map1[s]) for s in map1]))

path = search.search('A', lambda x: x=='G', actions, map1successor, depthFirst=False, DP=False, maxNodes=10000)
print(path)
# with dynamic
path = search.search('A', lambda x: x=='G', actions, map1successor, depthFirst=False, DP=True, maxNodes=10000)
print(path)

path = search.search('G', lambda x: x=='C', actions, map1successor, depthFirst=True, DP=False, maxNodes=10000)
print(path)

path = search.search('G', lambda x: x=='C', actions, map1successor, depthFirst=True, DP=True, maxNodes=10000)
print(path)


def mapObstTest(mapState, start, goal, badStates, badArcs, searchFn = search.breadthFirstDP):
    actions = range(max([len(mapState[s]) for s in mapState]))

    def succFn(s, a):
        if a < len(mapState):
            choosed = mapState[s]
            if s[a] in badStates:
                return s
            elif (s, choosed[a]) in badArcs:
                return s
            else:
                return s[a]
        else:
            return s

    def goalFn(s):
        return s == goal

    return searchFn(start, goalFn, actions, succFn)