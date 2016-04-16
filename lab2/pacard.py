
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
    print startState
    from util import PriorityQueue
    import logic
    states = {}
    statesQueue = PriorityQueue()
    statesQueue.push(startState, stateWeight(startState))

    while not statesQueue.isEmpty():
        currState = statesQueue.pop()
        visitedStates.append(currState)
        for state in problem.getSuccessors(currState):
            if state[0] not in visitedStates:
                if isSafe(problem, currState, state[0]):
                    states[state[0]] = [False, False, False]
                    statesQueue.push(state[0], stateWeight(state[0]))
                elif isMaybePoison(problem, currState, state[0]):
                    if state[0] not in states:
                        states[state[0]] = [False, False, None]
                    else:
                        if states[state[0]][0] == None:
                            states[state[0]][0] = False
                        if states[state[0]][1] == None:
                            states[state[0]][1] = False
                    if True not in states[state[0]] and None not in states[state[0]]:
                        statesQueue.push(state[0], stateWeight(state[0]))
                elif isMaybeWumpus(problem, currState, state[0]):
                    if state[0] not in states:
                        states[state[0]] = [None, False, False]
                    else:
                        if states[state[0]][1] == None:
                            states[state[0]][1] = False
                        if states[state[0]][2] == None:
                            states[state[0]][2] = False
                    if True not in states[state[0]] and None not in states[state[0]]:
                        statesQueue.push(state[0], stateWeight(state[0]))
                elif isMaybeTeleporter(problem, currState, state[0]):
                    if state[0] not in states:
                        states[state[0]] = [False, None, False]
                    else:
                        if states[state[0]][0] == None:
                            states[state[0]][0] = False
                        if states[state[0]][2] == None:
                            states[state[0]][2] = False
                    if states[state[0]][0] == False and states[state[0]][2] == False:
                        statesQueue.push(state[0], stateWeight(state[0]))


    print states
    return problem.reconstructPath(visitedStates)

def isMaybeTeleporter(problem, currState, currStateSuccessor):
    import logic
    premises = []
    s = problem.isWumpusClose(currState)
    c = problem.isPoisonCapsuleClose(currState)
    g = problem.isTeleporterClose(currState)

    for succ in problem.getSuccessors(currState):
        premises.append(Clause(set([Literal(Labels.TELEPORTER_GLOW, currState, True), Literal(Labels.TELEPORTER, succ[0], False)])))
    premises.append(Clause(set([Literal(Labels.WUMPUS_STENCH, currState, not s)])))
    premises.append(Clause(set([Literal(Labels.TELEPORTER_GLOW, currState, not g)])))
    premises.append(Clause(set([Literal(Labels.POISON_CHEMICALS, currState, not c)])))

    goal = Clause(set([Literal(Labels.TELEPORTER, currStateSuccessor, False)]))

    return resolution(set(premises), goal)


def isMaybeWumpus(problem, currState, currStateSuccessor):
    import logic
    premises = []
    s = problem.isWumpusClose(currState)
    c = problem.isPoisonCapsuleClose(currState)
    g = problem.isTeleporterClose(currState)

    for succ in problem.getSuccessors(currState):
        premises.append(Clause(set([Literal(Labels.WUMPUS_STENCH, currState, True), Literal(Labels.WUMPUS, succ[0], False)])))
    premises.append(Clause(set([Literal(Labels.WUMPUS_STENCH, currState, not s)])))
    premises.append(Clause(set([Literal(Labels.TELEPORTER_GLOW, currState, not g)])))
    premises.append(Clause(set([Literal(Labels.POISON_CHEMICALS, currState, not c)])))

    goal = Clause(set([Literal(Labels.WUMPUS, currStateSuccessor, False)]))

    return resolution(set(premises), goal)

def isSafe(problem, currState, currStateSuccessor):
    import logic
    premises = []
    s = problem.isWumpusClose(currState)
    c = problem.isPoisonCapsuleClose(currState)
    g = problem.isTeleporterClose(currState)

    for succ in problem.getSuccessors(currState):
        premises.append(Clause(set([Literal(Labels.WUMPUS_STENCH, currState, False), Literal(Labels.TELEPORTER_GLOW, currState, False), \
             Literal(Labels.POISON_CHEMICALS, currState, False), Literal(Labels.SAFE, succ[0], False)])))
    premises.append(Clause(set([Literal(Labels.WUMPUS_STENCH, currState, not s)])))
    premises.append(Clause(set([Literal(Labels.TELEPORTER_GLOW, currState, not g)])))
    premises.append(Clause(set([Literal(Labels.POISON_CHEMICALS, currState, not c)])))

    goal = Clause(set([Literal(Labels.SAFE, currStateSuccessor, False)]))

    return resolution(set(premises), goal)

def isMaybePoison(problem, currState, currStateSuccessor):
    import logic
    premises = []
    s = problem.isWumpusClose(currState)
    c = problem.isPoisonCapsuleClose(currState)
    g = problem.isTeleporterClose(currState)

    for succ in problem.getSuccessors(currState):
        premises.append(Clause(set([Literal(Labels.POISON_CHEMICALS, currState, True), Literal(Labels.POISON, succ[0], False)])))
    premises.append(Clause(set([Literal(Labels.WUMPUS_STENCH, currState, not s)])))
    premises.append(Clause(set([Literal(Labels.TELEPORTER_GLOW, currState, not g)])))
    premises.append(Clause(set([Literal(Labels.POISON_CHEMICALS, currState, not c)])))

    goal = Clause(set([Literal(Labels.POISON, currStateSuccessor, False)]))

    return resolution(set(premises), goal)

#states = {} #za pamcenje informacija o pojedinom stanju, sastoji se od W, T, P zastavica

# Abbreviations
lbs = logicBasedSearch
