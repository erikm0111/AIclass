import util 
import functools 

class Labels:
    """
    Labels describing the WumpusWorld
    """
    WUMPUS = 'w'
    TELEPORTER = 't'
    POISON = 'p'
    SAFE = 'o'

    """
    Some sets for simpler checks
    >>> if literal.label in Labels.DEADLY: 
    >>>     # Don't go there!!!
    """ 
    DEADLY = set([WUMPUS, POISON])
    WTP = set([WUMPUS, POISON, TELEPORTER])

    UNIQUE = set([WUMPUS, POISON, TELEPORTER, SAFE])

    POISON_CHEMICALS = 'c'
    TELEPORTER_GLOW = 'g'
    WUMPUS_STENCH = 's'

    INDICATORS = set([POISON_CHEMICALS, TELEPORTER_GLOW, WUMPUS_STENCH])


def stateWeight(state):
    """
    To ensure consistency in exploring states, they will be sorted 
    according to a simple linear combination. 
    The maps will never be larger than 20x20, and therefore this 
    weighting will be consistent.
    """
    x, y = state 
    return 20*x + y 


@functools.total_ordering
class Literal:
    """
    A literal is an atom or its negation
    In this case, a literal represents if a certain state (x,y) is or is not 
    the location of GhostWumpus, or the poisoned pills.
    """

    def __init__(self, label, state, negative=False):
        """
        Set all values. Notice that the state is remembered twice - you
        can use whichever representation suits you better.
        """
        x,y = state 
        
        self.x = x 
        self.y = y 
        self.state = state 

        self.negative = negative
        self.label = label 

    def __key(self):
        """
        Return a unique key representing the literal at a given point
        """
        return (self.x, self.y, self.negative, self.label)

    def __hash__(self):
        """
        Return the hash value - this operator overloads the hash(object) function.
        """
        return hash(self.__key())

    def __eq__(first, second):
        """
        Check for equality - this operator overloads '=='
        """
        return first.__key() == second.__key()

    def __lt__(self, other):
        """ 
        Less than check
        by using @functools decorator, this is enough to infer ordering
        """
        return stateWeight(self.state) < stateWeight(other.state)

    def __str__(self):
        """
        Overloading the str() operator - convert the object to a string
        """
        if self.negative: return '~' + self.label
        return self.label

    def __repr__(self):
        """
        Object representation, in this case a string
        """
        return self.__str__()

    def copy(self):
        """
        Return a copy of the current literal
        """
        return Literal(self.label, self.state, self.negative)

    def negate(self):
        """
        Return a new Literal containing the negation of the current one
        """
        return Literal(self.label, self.state, not self.negative)

    def isDeadly(self):
        """
        Check if a literal represents a deadly state
        """
        return self.label in labels.DEADLY

    def isWTP(self):
        """
        Check if a literal represents GhostWumpus, the Teleporter or 
        a poisoned pill
        """
        return self.label in labels.WTP

    def isSafe(self):
        """
        Check if a literal represents a safe spot
        """
        return self.label == Labels.SAFE

    def isTeleporter(self):
        """
        Check if a literal represents the teleporter
        """
        return self.label == Labels.TELEPORTER


class Clause: 
    """ 
    A disjunction of finitely many unique literals. 
    The Clauses have to be in the CNF so that resolution can be applied to them. The code 
    was written assuming that the clauses are in CNF, and will not work otherwise. 

    A sample of instantiating a clause (~B v C): 

    >>> premise = Clause(set([Literal('b', (0, 0), True), Literal('c', (0, 0), False)]))

    or; written more clearly
    >>> LiteralNotB = Literal('b', (0, 0), True)
    >>> LiteralC = Literal('c', (0, 0), False)

    >>> premise = Clause(set([[LiteralNotB, LiteralC]]))
    """ 

    def __init__(self, literals):
        """
        The constructor for a clause. The clause assumes that the data passed 
        is an iterable (e.g., list, set), or a single literal in case of a unit clause. 
        In case of unit clauses, the Literal is wrapped in a list to be safely passed to 
        the set.
        """
        if not type(literals) == set and not type(literals) == list:
            self.literals = set([literals])
        else:
            self.literals = set(literals)

    def isResolveableWith(self, otherClause):
        """
        Check if a literal from the clause is resolveable by another clause - 
        if the other clause contains a negation of one of the literals.
        e.g., (~A) and (A v ~B) are examples of two clauses containing opposite literals 
        """
        for literal in self.literals: 
            if literal.negate() in otherClause.literals:
                return True 
        return False 

    def isRedundant(self, otherClauses):
        """
        Check if a clause is a subset of another clause.
        """
        for clause in otherClauses:
            if self == clause: continue
            if clause.literals.issubset(self.literals):
                return True
        return False

    def negateAll(self):
        """
        Negate all the literals in the clause to be used 
        as the supporting set for resolution.
        """
        negations = set()
        for literal in self.literals:
            clause = Clause(literal.negate())
            negations.add(clause)
        return negations

    def __str__(self):
        """
        Overloading the str() operator - convert the object to a string
        """
        return ' V '.join([str(literal) for literal in self.literals])

    def __repr__(self):
        """
        The representation of the object
        """
        return self.__str__()


    def __hash__(self):
        """
        Return the hash value - this operator overloads the hash(object) function.
        """
        return hash(tuple(self.literals))

    def __eq__(self, other):
        if other == 'NIL':
            return tuple(self.literals) == 'NIL'
        else:
            return tuple(self.literals) == tuple(other.literals)


def resolution(clauses, goal):
    """
    Implement refutation resolution. 

    The pseudocode for the algorithm of refutation resolution can be found 
    in the slides. The implementation here assumes you will use set of support 
    and simplification strategies. We urge you to go through the slides and 
    carefully design the code before implementing.
    """
    resolvedPairs = set()
    setOfSupport = goal.negateAll()

    while True:
        clauses = removeRedundant(clauses, setOfSupport)
        selectedClauses = selectClauses(clauses, setOfSupport, resolvedPairs)
        if len(selectedClauses) == 0:
            return False
        for pair in selectedClauses:
            resolvents = resolvePair(pair[0], pair[1])
            resolvedPairs.add(pair)
            if resolvents == 'NIL':
                return True
            else:
                setOfSupport.add(resolvents)
        for x in setOfSupport:
            clauses.add(x)
    

def removeRedundant(clauses, setOfSupport):
    """
    Remove redundant clauses (clauses that are subsets of other clauses)
    from the aforementioned sets. 
    Be careful not to do the operation in-place as you will modify the 
    original sets. (why?)
    """
    newClauses = []
    for clause in clauses:
        if clause.isRedundant(setOfSupport):
            continue
        else:
            newClauses.append(clause)
    return set(newClauses)



def resolvePair(firstClause, secondClause):
    """ Resolve a pair of clauses. """

    literalsNew = set()
    deleted = 0
    for literal in firstClause.literals:
        if literal.negate() in secondClause.literals:
            if deleted<1:
                deletedLiteral = literal.negate()
                deleted += 1
                continue
            else:
                literalsNew.add(literal)
        else:
            literalsNew.add(literal)
    if deleted==1:
        for literal in secondClause.literals:
            if literal==deletedLiteral:
                continue
            else:
                literalsNew.add(literal)
    if len(literalsNew) == 0:
        #print 'Resolving... {}, {} ==>> {}'.format(firstClause, secondClause, 'NIL')
        return 'NIL'
    else:
        #print 'Resolving... {}, {} ==>> {}'.format(firstClause, secondClause, Clause(literalsNew))
        return Clause(literalsNew)


def selectClauses(clauses, setOfSupport, resolvedPairs):
    """ Select pairs of clauses to resolve. """
    selectedClauses = set()
    for goalClause in setOfSupport:
        for otherClause in clauses:
            if (goalClause, otherClause) not in resolvedPairs:
                if goalClause.isResolveableWith(otherClause):
                    selectedClauses.add((goalClause, otherClause))
    return selectedClauses 

def testResolution():
    """
    A sample of a resolution problem that should return True. 
    You should come up with your own tests in order to validate your code. 
    """

    """

    ~a v b  |
    ~b v c  |   premises
    a       |
    --------+
    c       |   goal (needs to be negated first)

    """
    premise1 = Clause(set([Literal('a', (0, 0), True), Literal('b', (0, 0), False)]))
    premise2 = Clause(set([Literal('b', (0, 0), True), Literal('c', (0, 0), False)]))
    premise3 = Clause(Literal('a', (0,0)))

    goal = Clause(Literal('c', (0,0)))

    print resolution(set([premise1, premise2, premise3]), goal)

def testResolution2():
    """
    Dipl. problem

    u v ~t  |
    t v a   |   premises
    ~u v ~a |
    --------+
    ~t v ~a |   goal (needs to be negated first)

    """

    premise1 = Clause(set([Literal('u', (0, 0), False), Literal('t', (0, 0), True)]))
    premise2 = Clause(set([Literal('t', (0, 0), False), Literal('a', (0, 0), False)]))
    premise3 = Clause(set([Literal('u', (0, 0), True), Literal('a', (0, 0), True)]))

    goal = Clause(set([Literal('t', (0, 0), True), Literal('a', (0, 0), True)]))

    print resolution(set([premise1, premise2, premise3]), goal)

def testResolution3():
    """
    1.13 iz knjige

    ~p v q v r |
    s v ~q     |   premises
    s v ~r     |
    -----------+
    ~p         |   goal (needs to be negated first)
    s          |

    """

    premise1 = Clause(set([Literal('p', (0, 0), True), Literal('q', (0, 0), False), Literal('r', (0, 0), False)]))
    premise2 = Clause(set([Literal('s', (0, 0), False), Literal('q', (0, 0), True)]))
    premise3 = Clause(set([Literal('s', (0, 0), False), Literal('r', (0, 0), True)]))

    goal = Clause(set([Literal('p', (0, 0), True), Literal('s', (0, 0), False)]))

    print resolution(set([premise1, premise2, premise3]), goal)


def testResolution4():
    """

    ~c v b     |
    ~b v e     |   premises
    ~e v b     |
    c          |
    ~d v ~e    |
    -----------+
    ~d         |   goal (needs to be negated first)
    ~a         |

    """

    premise1 = Clause(set([Literal('c', (0, 0), True), Literal('b', (0, 0), False)]))
    premise2 = Clause(set([Literal('b', (0, 0), True), Literal('e', (0, 0), False)]))
    premise3 = Clause(set([Literal('e', (0, 0), True), Literal('b', (0, 0), False)]))
    premise4 = Clause(set([Literal('c', (0,0), False)]))
    premise5 = Clause(set([Literal('d', (0, 0), True), Literal('e', (0, 0), True)]))

    goal = Clause(set([Literal('d', (0, 0), True), Literal('a', (0, 0), True)]))

    print resolution(set([premise1, premise2, premise3, premise4, premise5]), goal)


def testResolutionFalse1():
    """
    Example with result false

    ~a v b  |
    ~b v c  |   premises
    a       |
    --------+
    ~c      |   goal (needs to be negated first)

    """
    premise1 = Clause(set([Literal('a', (0, 0), True), Literal('b', (0, 0), False)]))
    premise2 = Clause(set([Literal('b', (0, 0), True), Literal('c', (0, 0), False)]))
    premise3 = Clause(Literal('a', (0,0)))

    goal = Clause(Literal('c', (0,0), True))

    print resolution(set([premise1, premise2, premise3]), goal)


def testResolution4KRIVO():
    """
    A v B v C v D |
    ~A v ~B v ~C  |   premises
    ~D            |
    --------------+
    D             |   goal (needs to be negated first)

    """

    premise1 = Clause(set([Literal('A', (0,0), False), Literal('B', (0,0), False), Literal('C', (0,0), False), Literal('D', (0,0), False)]))
    premise2 = Clause(set([Literal('A', (0,0), True), Literal('B', (0,0), True), Literal('C', (0,0), True)]))
    premise3 = Clause(Literal('D', (0,0), True))

    goal = Clause(Literal('D', (0,0)))
    
    print resolution(set([premise1, premise2, premise3]), goal)


def testResolutionFact():
    """
    ~a v b  |
    ~b v ~a |   premises
    --------+
    ~a      |   goal (needs to be negated first)

    """
    premise1 = Clause(set([Literal('a', (0, 0), True), Literal('b', (0, 0), False)]))
    premise2 = Clause(set([Literal('b', (0, 0), True), Literal('a', (0, 0), True)]))
    goal = Clause(Literal('a', (0,0), True))

    print resolution(set([premise1, premise2]), goal)


def testEleven():
    """
    s ~i
    ~s a
    ~a
    -----
    ~s
    """
    premise1 = Clause(set([Literal('s', (0, 0), False), Literal('i', (0, 0), True)]))
    premise2 = Clause(set([Literal('s', (0, 0), True), Literal('a', (0, 0), False)]))
    premise3 = Clause(set([Literal('a', (0, 0), True)]))

    goal = Clause(set([Literal('s', (0, 0), True)]))

    print resolution(set([premise1, premise2, premise3]), goal)


def testLab():
    """
    A sample of a resolution problem that should return True. 
    You should come up with your own tests in order to validate your code. 

    """
    premise1 = Clause(set([Literal('a', (0, 0), True), Literal('a', (0, 0), True)]))
    premise2 = Clause(set([Literal('a', (0, 0), False), Literal('a', (0, 0), False)]))

    goal = Clause(set([Literal('a', (0, 0), False), Literal('a', (0, 0), True)]))

    print resolution(set([premise1, premise2]), goal)

def test118Skripta():
    premise1 = Clause(set([Literal('a', (0, 0), True), Literal('b', (0, 0), False)]))
    premise2 = Clause(set([Literal('b', (0, 0), True), Literal('d', (0, 0), False)]))
    premise3 = Clause(set([Literal('c', (0, 0), True), Literal('d', (0, 0), False)]))
    premise4 = Clause(set([Literal('d', (0, 0), True), Literal('e', (0, 0), False)]))
    premise5 = Clause(set([Literal('b', (0, 0), False), Literal('c', (0, 0), False)]))

    goal = Clause(set([Literal('e', (0, 0), False)]))

    print resolution(set([premise1, premise2, premise3, premise4, premise5]), goal)


if __name__ == '__main__':
    """
    The main function - if you run logic.py from the command line by 
    >>> python logic.py 

    this is the starting point of the code which will run. 
    """ 
    test118Skripta()