import json
import antlr3
from FsmlLexer import FsmlLexer
from FsmlParser import FsmlParser

def parseFSM():
    char_stream = antlr3.ANTLRInputStream(open("./sample.fsml", 'r'))
    lexer = FsmlLexer(char_stream)
    tokens = antlr3.CommonTokenStream(lexer)
    parser = FsmlParser(tokens)
    parser.fsm()
    return parser.fsmObject


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


sampleInput = json.load(open("./sample_input.json", "r"))

fsm = parseFSM()

# just for visualization of the fsm dict
jsonFile = open("./sample_fsml.json", 'w')
jsonFile.write(json.dumps(fsm))

if ok(fsm):
    output = simulateFSM(fsm, sampleInput)

# dump the simulation output to file
outFile = open("./sample_output.json", 'w')
outFile.write(json.dumps(output))

