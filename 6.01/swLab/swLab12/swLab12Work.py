import lib601.dist as dist
import lib601.sm as sm
import lib601.ssm as ssm
import lib601.util as util

def incrDictEntry(d, k, v):
    """
    If dictionary C{d} has key C{k}, then increment C{d[k]} by C{v}.
    Else set C{d[k] = v}.

    @param d: dictionary
    @param k: legal dictionary key (doesn't have to be in C{d})
    @param v: numeric value
    """
    if d.has_key(k):
        d[k] += v
    else:
        d[k] = v

class StateEstimator(sm.SM):
    def __init__(self, model):
        self.model = model
        self.startState = model.startDistribution

    def getNextValues(self, state, inp):  # bayesEvidence(PBgA, PA, b)
        (o, i) = inp
        # print("state",state)
        # print(self.model.observationDistribution)
        # sGo = dist.bayesEvidence(state, self.model.observationDistribution, o) # bayesEvidence(conditionProb, priorProb, condition)
        # print("SGo", sGo)
        # # print('transition',self.model.transitionDistribution(i))
        # dSPrime = dist.totalProbability(sGo,
        #                                 self.model.transitionDistribution(i)) # totalProbability(conditionProb, priorProb) return numerator probs
        # # print("dsPrime",dSPrime)
        # return (dSPrime, dSPrime)
        # self.bayesEvidence(state, o)
        sGo = self.efficientBayesEvidence(state, self.model.observationDistribution, o)
        print("SGo", sGo)
        dSPrime = self.efficientTotalProbability(sGo, self.model.transitionDistribution(i))
        return (dSPrime, dSPrime)

    def bayesEvidence(self, state, observation):
        joint = dist.JDist(state, self.model.observationDistribution)
        # print('joint', joint)
        belief = joint.conditionOnVar(1, observation)
        return belief

    def efficientBayesEvidence(self, state, observationCondition, observation):
        ## state should be condition probability
        ## just calculation the useful part
        belief = {}
        observation_prob = 0.
        for now_state in state.support():
            observa_probs_with_now = observationCondition(now_state)
            this_joint_prob = state.prob(now_state)*observa_probs_with_now.prob(observation)
            belief[now_state] = this_joint_prob
            observation_prob += this_joint_prob
        # print("belief", belief)
        for key in belief.keys():
            belief[key] = belief[key] / observation_prob
        return dist.DDist(belief)

    def efficientTotalProbability(self, priorState, transitionContidition):
        totalProbs = {}
        for state in priorState.support():
            transitionProbs = transitionContidition(state)
            for transed_state in transitionProbs.support():
                incrDictEntry(totalProbs, transed_state, priorState.prob(state)*transitionProbs.prob(transed_state))
        return dist.DDist(totalProbs)




 



# Test

transitionTable = \
   {'good': dist.DDist({'good' : 0.7, 'bad' : 0.3}),
    'bad' : dist.DDist({'good' : 0.1, 'bad' : 0.9})}
observationTable = \
   {'good': dist.DDist({'perfect' : 0.8, 'smudged' : 0.1, 'black' : 0.1}),
    'bad': dist.DDist({'perfect' : 0.1, 'smudged' : 0.7, 'black' : 0.2})}

copyMachine = \
 ssm.StochasticSM(dist.DDist({'good' : 0.9, 'bad' : 0.1}),
                # Input is irrelevant; same dist no matter what
                lambda i: lambda s: transitionTable[s],  # transitionDistribution: take and action and return a procedure, which takes an old state and return a distribution over new states
                lambda s: observationTable[s])  # take a state and return a distribution over observation
obs = [('perfect', 'step'), ('smudged', 'step'), ('perfect', 'step')]

func1 = lambda i: lambda s: transitionTable[s]  # first give the parameter to i, then give the parameter to s, i is not useful
print(func1('good')('good'), func1('bad')('good'))
func2 = lambda s: observationTable[s]
print('lambda', func2('good'))

def observationModel(s):
    # All of the rooms in our world have white walls, except for room
    # 2, which has green walls; observations are wrong with
    # probability 0.1
    if s == 2:
        return dist.DDist({'green' : 0.9, 'white' : 0.1})
    else:
        return dist.DDist({'white' : 0.9, 'green' : 0.1})

def transitionModel(action):
    def transGivenA(oldS):
        # Robot moves to the nominal new location (that is, the
        # old location plus the action) with probability 0.8; some
        # chance that it moves one step too little, or one step too
        # much. Be careful not to run off the end of the world.
        nominalNewS = oldS + action
        # This is from Wk.11.1.2, Part 3
        d = {}
        dist.incrDictEntry(d, util.clip(nominalNewS, 0, 5), 0.8)
        dist.incrDictEntry(d, util.clip(nominalNewS+1, 0, 5), 0.1)
        dist.incrDictEntry(d, util.clip(nominalNewS-1, 0, 5), 0.1)
        return dist.DDist(d)
    return transGivenA
simpleHallway = ssm.StochasticSM(dist.UniformDist(range(5)),transitionModel,observationModel)
# for i in range(10):
#     print simpleHallway.transduce([1, 1, 1, 1])

cmse = StateEstimator(copyMachine)

print cmse.transduce(obs)


