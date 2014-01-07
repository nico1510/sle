from FsmExceptions import *


def fsmDistinctIds(fsm):
    for state, stateDeclarations in fsm.iteritems():
        if not len(stateDeclarations) == 1:
            raise DistinctIdsException()
    else:
        return True


def fsmSingleInitial(fsm):
    count = 0
    for _, [stateDeclaration] in fsm.iteritems():
        if stateDeclaration["initial"]:
            count += 1

    if not count == 1:
        raise SingleInitialException()
    else:
        return True


def fsmDeterministic(fsm):
    for state, [stateDeclaration] in fsm.iteritems():
        for input, transitions in stateDeclaration["transitions"].iteritems():
            if not len(transitions) == 1:
                raise DeterministicException()
    else:
        return True


def fsmResolvable(fsm):
    for _, [stateDeclaration] in fsm.iteritems():
        for _, [(_, targetState)] in stateDeclaration["transitions"].iteritems():
            if not targetState in fsm:
                raise ResolvableException()
    else:
        return True


def fsmReachable(fsm):
    for initialState, [stateDeclaration] in fsm.iteritems():
        if stateDeclaration["initial"]:
            reachables = set()
            reachables.add(initialState)
            findReachableStates(initialState, fsm, reachables)

    definedStates = set()
    for state in fsm:
        definedStates.add(state)

    if reachables == definedStates:
        return True
    else:
        raise ReachableException()

def findReachableStates(currentState, fsm, visitedStates):
    for stateDeclaration in fsm[currentState]:
        for _, [(_, targetState)] in stateDeclaration["transitions"].iteritems():
            if not targetState in visitedStates:
                visitedStates.add(targetState)
                findReachableStates(targetState, fsm, visitedStates)


def ok(fsm):
    for fun in [fsmDistinctIds, fsmSingleInitial, fsmDeterministic, fsmResolvable, fsmReachable]:
        try:
            fun(fsm)
        except OkFsmException:
            raise
    else:
        print "all constraints succeeded"

