import lib601.sf as sf

###5.2.1
def controllerSF(k):
    return sf.Gain(k)

def plantSF(T):
    dist = 50
    return sf.FeedbackAdd(-sf.Gain(T), sf.R(dist))

def sensorSF():
    pass # related to io

def wallFinderSystemSF(T, k):
    return sf.Cascade(controllerSF(k), plantSF(T))