# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import copy

class SearchNode:
    """
    This class represents a node in the graph which represents the search problem.
    The class is used as a basic wrapper for search methods - you may use it, however
    you can solve the assignment without it.

    REMINDER: You need to fill in the backtrack function in this class!
    """

    def __init__(self, position, parent=None, transition=None, cost=0, heuristic=0):
        """
        Basic constructor which copies the values. Remember, you can access all the 
        values of a python object simply by referencing them - there is no need for 
        a getter method. 
        """
        self.position = position
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
        self.transition = transition

    def isRootNode(self):
        """
        Check if the node has a parent.
        returns True in case it does, False otherwise
        """
        return self.parent == None 

    def unpack(self):
        """
        Return all relevant values for the current node.
        Returns position, parent node, cost, heuristic value
        """
        return self.position, self.parent, self.cost, self.heuristic


    def backtrack(self):
        """
        Reconstruct a path to the initial state from the current node.
        Bear in mind that usually you will reconstruct the path from the 
        final node to the initial.
        """
        moves = []
        # make a deep copy to stop any referencing isues.
        node = copy.deepcopy(self)

        if node.isRootNode(): 
            # The initial state is the final state
            return moves        

        "**YOUR CODE HERE**"
        while not node.isRootNode():
            moves.append(node.transition)
            node = node.parent

        moves.reverse()
        return moves


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


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def expand(problem, currentNode):
    """Expand successors of current node."""
    return [SearchNode(succ[0], currentNode, succ[1], currentNode.cost+succ[2], 0) for succ in problem.getSuccessors(currentNode.position)]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    from util import Stack

    stackOpen = Stack()

    rootNode = SearchNode(problem.getStartState(), None, None, 0, 0)

    if problem.isGoalState(rootNode.position):
        return []

    stackOpen.push(rootNode)
    visited = {}

    while not stackOpen.isEmpty():
        currentNode = stackOpen.pop()
        if currentNode.position in visited:
            continue
        if problem.isGoalState(currentNode.position):
            return currentNode.backtrack()
        visited[currentNode.position] = True
        for succ in expand(problem, currentNode):
            if succ.position not in visited:
                temp = SearchNode(succ.position, currentNode, succ.transition, succ.cost, 0)
                stackOpen.push(temp)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue

    queueOpen = Queue()

    rootNode = SearchNode(problem.getStartState(), None, None, 0, 0)

    if problem.isGoalState(rootNode.position):
        return []

    queueOpen.push(rootNode)
    visited = {}
    #visited;
    #cvorovi = [pocetni];

    while not queueOpen.isEmpty():
        #ako je cvor u visited -> continue
        #stavi cvor u visited
        #za svakog sljedbenika: ako nije u visited, dodaj ga u cvorove
        currentNode = queueOpen.pop()
        if currentNode.position in visited:
            continue
        if problem.isGoalState(currentNode.position):
            return currentNode.backtrack()
        visited[currentNode.position] = True
        for succ in expand(problem, currentNode):
            if succ.position not in visited:
                temp = SearchNode(succ.position, currentNode, succ.transition, succ.cost, 0)
                queueOpen.push(temp)


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    from util import PriorityQueue

    queueOpen = PriorityQueue()

    rootNode = SearchNode(problem.getStartState(), None, None, 0, 0)

    if problem.isGoalState(rootNode.position):
        return []

    queueOpen.push(rootNode, 0)
    visited = {}

    while not queueOpen.isEmpty():
        currentNode = queueOpen.pop()
        if currentNode.position in visited:
            continue
        if problem.isGoalState(currentNode.position):
            return currentNode.backtrack()
        visited[currentNode.position] = True
        for succ in expand(problem, currentNode):
            if succ.position not in visited:
                temp = SearchNode(succ.position, currentNode, succ.transition, succ.cost, 0)
                queueOpen.push(temp, succ.cost)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue

    queueOpen = PriorityQueue()
    openNodes = []
    closedNodes = []
    visited = {}
    opened = []

    rootNode = SearchNode(problem.getStartState(), None, None, 0, 0)

    if problem.isGoalState(rootNode.position):
        return []

    queueOpen.push(rootNode, 0)
    openNodes.append(rootNode)
    opened.append(rootNode.position)

    while not queueOpen.isEmpty():
        currentNode = queueOpen.pop()
        openNodes.remove(currentNode)
        opened.remove(currentNode.position)
        if currentNode.position in visited:
            continue
        if problem.isGoalState(currentNode.position):
            return currentNode.backtrack()
        visited[currentNode.position] = True
        closedNodes.append(currentNode)
        for succ in expand(problem, currentNode):
            """provjera da li je u visited, provjera da li je u opened, ako je u nekom od ta dva 
            onda preskoci dodavanje novog cvora jer vec postoji onaj s manjom vrijednosti"""
            flag = False
            if succ.position in visited:
                for t in closedNodes:
                    if t.position==succ.position:
                        if t.cost < succ.cost:
                            flag = True
                            break;
            if succ.position in opened:
                for t in openNodes:
                    if t.position==succ.position:
                        if t.cost < succ.cost:
                            flag = True
                            break;
            if not flag:
                temp = SearchNode(succ.position, currentNode, succ.transition, succ.cost, 0)
                f = succ.cost + heuristic(succ.position, problem)
                queueOpen.push(temp, f)
                openNodes.append(temp)
                opened.append(temp.position)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
