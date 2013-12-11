def fsmDistinctIds(fsm):
    for state, stateDeclarations in fsm.iteritems():
        if not len(stateDeclarations) == 1:
            return False
    else:
        return True


def fsmSingleInitial(fsm):
    count = 0
    for _, [stateDeclaration] in fsm.iteritems():
        if stateDeclaration["initial"]:
            count += 1
    return count == 1


def fsmDeterministic(fsm):
    for state, [stateDeclaration] in fsm.iteritems():
        for input, transitions in stateDeclaration["transitions"].iteritems():
            if not len(transitions) == 1:
                return False
    else:
        return True


def fsmResolvable(fsm):
    for _, [stateDeclaration] in fsm.iteritems():
        for _, [(_, targetState)] in stateDeclaration["transitions"].iteritems():
            if not targetState in fsm:
                return False
    else:
        return True


def fsmReachable(fsm):
    for initialState, [stateDeclaration] in fsm.iteritems():
        if stateDeclaration["initial"]:
            reachables = set()
            findReachableStates(initialState, fsm, reachables)

    definedStates = set()
    for state in fsm:
        definedStates.add(state)
    return reachables == definedStates

def findReachableStates(currentState, fsm, visitedStates):
    for stateDeclaration in fsm[currentState]:
        for _, [(_, targetState)] in stateDeclaration["transitions"].iteritems():
            if not targetState in visitedStates:
                visitedStates.add(targetState)
                findReachableStates(targetState, fsm, visitedStates)


def ok(fsm):
    for fun in [fsmDistinctIds, fsmSingleInitial, fsmDeterministic, fsmResolvable, fsmReachable]:
        if not fun(fsm):
            print fun.__name__ + " failed"
            return False
    else:
        print "all constraints succeeded"
        return True