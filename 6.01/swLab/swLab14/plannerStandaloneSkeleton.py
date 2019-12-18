import math
import lib601.ucSearch as ucSearch
import lib601.util as util
import lib601.basicGridMap as basicGridMap
import lib601.gridMap as gridMap
import lib601.sm as sm



######################################################################
###         Picking worlds
######################################################################

mapTestWorld = ['mapTestWorld.py', 0.2, util.Point(2.0, 5.5),
                util.Pose(2.0, 0.5, 0.0)]
bigPlanWorld = ['bigPlanWorld.py', 0.25, util.Point(3.0, 1.0),
                util.Pose(1.0, 1.0, 0.0)]


class GridDynamics(sm.SM):
    '''
    total are 8 directions around the square
    '''
    
    legalInputs = ['up', 'down', 'right', 'left', 'upLeft', 'upRight', 'downLeft', 'downRight']
    
    def __init__(self, theMap):
        self.map = theMap
        self.stepSize =self.map.xStep

    def getNextValues(self, state, inp):
        assert inp in self.legalInputs, "the input action is not valid"
        statex, statey = state
        hvCost = self.stepSize
        adjCost = 2.**0.5*self.stepSize
        if inp == 'up':
            statey += 1
            cost = hvCost
        elif inp == 'down':
            statey -= 1
            cost = hvCost
        elif inp == 'left':
            statex -= 1
            cost = hvCost
        elif inp == 'right':
            statex += 1
            cost = hvCost
        elif inp == 'upLeft':
            statex -= 1
            statey += 1
            cost = adjCost
        elif inp == 'upRight':
            statex += 1
            statey += 1
            cost = adjCost
        elif inp == 'downLeft':
            statex -= 1
            statey -= 1
            cost = adjCost
        elif inp == 'downRight':
            statex += 1
            statey -= 1
            cost = adjCost
        nextState = (statex, statey)
        if self.map.robotCanOccupy(nextState):
            return (nextState, cost)
        else:
            return (state, cost)


class TestGridMap(gridMap.GridMap):
    def __init__(self, gridSquareSize):
        gridMap.GridMap.__init__(self, 0, gridSquareSize * 5,
                               0, gridSquareSize * 5, gridSquareSize, 100)

    def makeStartingGrid(self):
        grid = util.make2DArray(5, 5, False)
        for i in range(5):
            grid[i][0] = True
            grid[i][4] = True
        for j in range(5):
            grid[0][j] = True
            grid[4][j] = True
        grid[3][3] = True
        return grid

    def robotCanOccupy(self, (xIndex, yIndex)):
        return not self.grid[xIndex][yIndex]

def testGridDynamics():
    gm = TestGridMap(0.15)
    print 'For TestGridMap(0.15):'
    r = GridDynamics(gm)
    print 'legalInputs', util.prettyString(r.legalInputs)
    ans1 = [r.getNextValues((1,1), a) for a in r.legalInputs]
    print 'starting from (1,1)', util.prettyString(ans1)
    ans2 = [r.getNextValues((2,3), a) for a in r.legalInputs]
    print 'starting from (2,3)', util.prettyString(ans2)
    ans3 = [r.getNextValues((3, 2), a) for a in r.legalInputs]
    print 'starting from (3,2)', util.prettyString(ans3)
    gm2 = TestGridMap(0.4)
    print 'For TestGridMap(0.4):'
    r2 = GridDynamics(gm2)
    ans4 = [r2.getNextValues((2,3), a) for a in r2.legalInputs]
    print 'starting from (2,3)', util.prettyString(ans4)

testGridDynamics()

def planner(initialPose, goalPoint, worldPath, gridSquareSize):
    ## create grid map
    # wordPath, a string representing the name of a file containing a soar world definition
    # gridSquareSize is the size, in meters, of a side of each grid cell
    gm = basicGridMap.BasicGridMap(worldPath, gridSquareSize)

    initialP = initialPose.point()
      #size, in world coordinates, of a grid square
    goalIndices = gm.pointToIndices(goalPoint)
    initIndices = gm.pointToIndices(initialP)

    def g(s):
        gm.drawSquare(s, 'gray')
        return s == goalIndices

    def heuristic(s):
        return ((goalIndices[0] - s[0]) ** 2. + (goalIndices[1] - s[1]) ** 2) ** (0.5)
    path = ucSearch.smSearch(GridDynamics(gm), initialState=initIndices, goalTest=lambda x:g(x), heuristic=lambda s: heuristic(s))
    # smToSearch - instance of sm.SM defining a search domain; getNextValues is used to determine the successor of a state given an action; the output field of getNextValues is interpreted as a cost.
    # initialState - initial state for the search; if not provided, will use smToSearch.startState
    # goalTest - function that takes a state as an argument and returns True if it is a goal state, and False otherwise
    # heuristic - function from state to estimated cost to reach a goal; defaults to a heuristic of 0, making this uniform cost search
    # maxNodes - maximum number of nodes to be searched; prevents runaway searches
    print "path=", path
    pathDrawing = []
    for element in path:
        action, indice = element
        pathDrawing.append(indice)
    # drawPath(self, listOfIndices) , where listOfIndices is of the form [(ix1, iy1), (ix2, iy2), ...]
    gm.drawPath(pathDrawing)
    return path


def testPlanner(world):
    (worldPath, gridSquareSize, goalPoint, initialPose) = world
    planner(initialPose, goalPoint, worldPath, gridSquareSize)

testPlanner(mapTestWorld)

