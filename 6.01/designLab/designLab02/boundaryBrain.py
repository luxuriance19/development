import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io

def wall_ahead(sonars):
    return sonars[3] < 0.5 or sonars[4] < 0.5

def right_wall_too_far(sonars):
    return 0.3 < sonars[7]

def right_wall_too_close(sonars):
    return sonars[7] < 0.5

class MySMClass(sm.SM):
    # fvel: forward velocity
    # rvel: rotational velocity
    def __init__(self):
        self.startState = "initialize"

    def getNextValues(self, state, inp):
        if state == 'initialize':
            if not wall_ahead(inp.sonars):
                fvel = 0.03
                rvel = 0.0
                return (state, io.action(fvel,rvel))
            else:
                fvel = 0.0
                rvel = 0.0
                return ("follow", io.action(fvel, rvel))

        if state == 'follow':
            if wall_ahead(inp.sonars):
                fvel = 0.0
                rvel = 0.03
                print "turning left", "cause wall ahead"
                return ("follow", io.Action(fvel=fvel, rvel=rvel))
            elif right_wall_too_close(inp.sonars):
                fvel = 0.01
                rvel = 0.03
                print "turning left", "cause wall too close"
                return ("follow", io.Action(fvel=fvel, rvel=rvel))
            elif right_wall_too_far(inp.sonars):
                fvel = 0.01
                rvel = -0.03
                print "turning right", "cause wall too far"
                return ("follow", io.Action(fvel=fvel, rvel=rvel))


mySM = MySMClass()
mySM.name = 'brainSM'

######################################################################
###
###          Brain methods
###
######################################################################

def plotSonar(sonarNum):
    robot.gfx.addDynamicPlotFunction(y=('sonar'+str(sonarNum),
                                        lambda: 
                                        io.SensorInput().sonars[sonarNum]))

# this function is called when the brain is (re)loaded
def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=True, # slime trails
                                  sonarMonitor=False) # sonar monitor widget
    
    # set robot's behavior
    robot.behavior = mySM

# this function is called when the start button is pushed
def brainStart():
    robot.behavior.start(traceTasks = robot.gfx.tasks())

# this function is called 10 times per second
def step():
    inp = io.SensorInput()
    print inp.sonars[3]
    # robot.behavior.step(inp).execute()
    io.done(robot.behavior.isDone())

# called when the stop button is pushed
def brainStop():
    pass

# called when brain or world is reloaded (before setup)
def shutdown():
    pass
