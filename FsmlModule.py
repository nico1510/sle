import json
import antlr3
import sys
from FsmlLexer import FsmlLexer
from FsmlParser import FsmlParser

def parseFSM():
    char_stream = antlr3.ANTLRInputStream(sys.stdin)
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
    count=0
    for _, [stateDeclaration] in fsm.iteritems():
        if stateDeclaration["initial"]:
            count+=1
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


def ok(fsm):
    for fun in [fsmDistinctIds, fsmSingleInitial, fsmDeterministic, fsmResolvable]:
        if not fun(fsm):
            print fun.__name__ + " failed"
            return False
    else:
        print "all constraints succeeded"
        return True


def simulateFSM(fsm, inputList):

    # getting the initial state
    for stateName, [stateDeclaration] in fsm.iteritems():
        if stateDeclaration["initial"]:
            currentState = stateDeclaration

    # processing the input
    while inputList:
        input = inputList.pop(0)
        [(action, targetState)] = currentState["transitions"][input]
        print ([str(action)], str(targetState))
        [currentState] = fsm[targetState]


sampleInput = ["ticket", "pass", "ticket", "pass", "ticket", "ticket", "pass", "pass", "ticket", "pass", "mute", "release", "ticket", "pass"]

fsm = parseFSM()

# just for visualization of the fsm dict
jsonFile = open("./sample.json", 'w')
jsonFile.write(json.dumps(fsm))

if ok(fsm):
    simulateFSM(fsm, sampleInput)

