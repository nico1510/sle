def simulateFSM(fsm, inputList):

    output = []

    # getting the initial state
    for stateName, [stateDeclaration] in fsm.iteritems():
        if stateDeclaration["initial"]:
            currentState = stateDeclaration

    # processing the input
    while inputList:
        input = inputList.pop(0)
        [(action, targetState)] = currentState["transitions"][input]
        item = dict()
        item[str(targetState)] = str(action)
        output.append(item)
        [currentState] = fsm[targetState]

    return output