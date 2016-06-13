
"""
In pacard.py, you will implement the search algorithm  based on refutation resolution 
which will lead Pacard through the cave of the evil GhostWumpus.
"""

import util
from logic import * 

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def miniWumpusSearch(problem): 
    """
    A sample pass through the miniWumpus layout. Your solution will not contain 
    just three steps! Optimality is not the concern here.
    """
    from game import Directions
    e = Directions.EAST 
    n = Directions.NORTH
    return  [e, n, n]


def logicBasedSearch(problem):
    """

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())

    print "Does the Wumpus's stench reach my spot?", 
               \ problem.isWumpusClose(problem.getStartState())

    print "Can I sense the chemicals from the pills?", 
               \ problem.isPoisonCapsuleClose(problem.getStartState())

    print "Can I see the glow from the teleporter?", 
               \ problem.isTeleporterClose(problem.getStartState())
    
    (the slash '\\' is used to combine commands spanning through multiple lines - 
    you should remove it if you convert the commands to a single line)
    
    Feel free to create and use as many helper functions as you want.

    A couple of hints: 
        * Use the getSuccessors method, not only when you are looking for states 
        you can transition into. In case you want to resolve if a poisoned pill is 
        at a certain state, it might be easy to check if you can sense the chemicals 
        on all cells surrounding the state. 
        * Memorize information, often and thoroughly. Dictionaries are your friends and 
        states (tuples) can be used as keys.
        * Keep track of the states you visit in order. You do NOT need to remember the
        tranisitions - simply pass the visited states to the 'reconstructPath' method 
        in the search problem. Check logicAgents.py and search.py for implementation.
    """
    # array in order to keep the ordering
    visitedStates = []
    startState = problem.getStartState()
    #visitedStates.append(startState)
    from util import PriorityQueue
    import logic
    import sys
    statesQueue = PriorityQueue()
    statesQueue.push(startState, stateWeight(startState))

    heapImitation = []
    heapImitation.append(startState)

    while True:
        try :
            currState = statesQueue.pop()
        except:
            break
        heapImitation.remove(currState)
        visitedStates.append(currState)
        if problem.isGoalState(currState):
            break
        for state in problem.getSuccessors(currState):
            if state[0] not in visitedStates and state[0] not in heapImitation:
                setFlags(problem, visitedStates, currState, state[0])
                if state[0] in safeStates:
                    statesQueue.push(state[0], stateWeight(state[0]))
                    heapImitation.append(state[0])
                    safeStates.remove(state[0])
                elif state[0] in unsafeStates:
                    if not True in unsafeStates[state[0]] and not None in unsafeStates[state[0]]:
                        safeStates.append(unsafeStates[state[0]])
                        statesQueue.push(state[0], stateWeight(state[0]))
                        heapImitation.append(state[0])
                        unsafeStates.pop(state[0], None)
                elif not safeStates:
                    statesQueue.push(state[0], stateWeight(state[0]))
                    heapImitation.append(state[0])
        if statesQueue.isEmpty():
            if len(problem.getSuccessors(currState)) > 2:
                minWeightState = None
                minWeight = sys.maxint
                for key in unsafeStates:
                    if minWeight > stateWeight(key):
                        minWeight = stateWeight(key)
                        minWeightState = key
                statesQueue.push(minWeightState, minWeight)
                heapImitation.append(minWeightState)
                unsafeStates.pop(minWeightState, None)
    return problem.reconstructPath(visitedStates)


def setFlags(problem, visitedStates, currState, currStateSuccessor):
    import logic
    premises = []
    s = problem.isWumpusClose(currState)
    c = problem.isPoisonCapsuleClose(currState)
    g = problem.isTeleporterClose(currState)

    # ~c v p
    premises.append(Clause(set([Literal(Labels.POISON_CHEMICALS, currState, True), Literal(Labels.POISON, currStateSuccessor, False)])))

    # w v p v o
    premises.append(Clause(set([Literal(Labels.WUMPUS, currStateSuccessor, False), Literal(Labels.POISON, currStateSuccessor, False), \
                                Literal(Labels.SAFE, currStateSuccessor, False)])))

    # s v g v c v o
    premises.append(Clause(set([Literal(Labels.WUMPUS_STENCH, currState, False), Literal(Labels.TELEPORTER_GLOW, currState, False), \
             Literal(Labels.POISON_CHEMICALS, currState, False), Literal(Labels.SAFE, currStateSuccessor, False)])))

    # ~s v w v ~g v t
    premises.append(Clause(set([Literal(Labels.WUMPUS_STENCH, currState, True), Literal(Labels.WUMPUS, currStateSuccessor, False)])))
    premises.append(Clause(set([Literal(Labels.TELEPORTER_GLOW, currState, True), Literal(Labels.TELEPORTER, currStateSuccessor, False)])))

    # ~g v c v s v o
    premises.append(Clause(set([Literal(Labels.TELEPORTER_GLOW, currState, True), Literal(Labels.POISON_CHEMICALS, currState, False), \
                                Literal(Labels.WUMPUS_STENCH, currState, False), Literal(Labels.SAFE, currStateSuccessor, False)])))


    premises.append(Clause(set([Literal(Labels.WUMPUS_STENCH, currState, not s)])))
    premises.append(Clause(set([Literal(Labels.TELEPORTER_GLOW, currState, not g)])))
    premises.append(Clause(set([Literal(Labels.POISON_CHEMICALS, currState, not c)])))
    
    if currStateSuccessor in unsafeStates:
        if unsafeStates[currStateSuccessor][0]==False or unsafeStates[currStateSuccessor][0]==True:
            w = unsafeStates[currStateSuccessor][0]
            premises.append(Clause(set([Literal(Labels.WUMPUS, currStateSuccessor, not w)])))
        if unsafeStates[currStateSuccessor][1]==False or unsafeStates[currStateSuccessor][1]==True:
            t = unsafeStates[currStateSuccessor][1]
            premises.append(Clause(set([Literal(Labels.TELEPORTER, currStateSuccessor, not t)])))
        if unsafeStates[currStateSuccessor][2]==False or unsafeStates[currStateSuccessor][2]==True:
            p = unsafeStates[currStateSuccessor][2]
            premises.append(Clause(set([Literal(Labels.POISON, currStateSuccessor, not p)])))

    goalIsSafe = Clause(set([Literal(Labels.SAFE, currStateSuccessor, False)]))
    goalIsMaybeTeleporter = Clause(set([Literal(Labels.TELEPORTER, currStateSuccessor, False)]))
    goalIsMaybeWumpus = Clause(set([Literal(Labels.WUMPUS, currStateSuccessor, False)]))
    goalIsMaybePoison = Clause(set([Literal(Labels.POISON, currStateSuccessor, False)]))

    safe = resolution(set(premises), goalIsSafe)
    maytel = resolution(set(premises), goalIsMaybeTeleporter)
    maywum = resolution(set(premises), goalIsMaybeWumpus)
    maypoi = resolution(set(premises), goalIsMaybePoison)

    if safe:
        if currStateSuccessor not in visitedStates:
            safeStates.append(currStateSuccessor)
    if maywum:
        if currStateSuccessor not in visitedStates:
            unsafeStates[currStateSuccessor] = [None, maytel, maypoi]
    if maypoi:
        if currStateSuccessor not in visitedStates:
            unsafeStates[currStateSuccessor] = [maywum, maytel, None]


safeStates = []
poisonsStates = []
unsafeStates = {}

# Abbreviations
lbs = logicBasedSearch
