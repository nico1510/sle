import os
from nltk.parse.generate2 import generate
from nltk.grammar import parse_cfg

grammarstring = """
FSM -> ISTATE STATES
ISTATE -> 'initial' 'state' '#initState#' '{' TRANS '}'
STATES -> STATE STATES |
STATE -> 'state' '#stateDecl#' '{' TRANS '}'
TRANS -> TRANSITION TRANS |
TRANSITION -> '#input#' '/' '#action#' '->' '#newState#' ';'
"""

def generateRawTemplates():
    gram = parse_cfg(grammarstring)
    rawTemplates = generate(gram, depth=7)
    i = 0
    templatefiles = []

    for state in rawTemplates:
        filename = os.path.join("./rawTemplates","template"+str(i))
        with open(filename, 'w') as templatefile:
            templatefile.write(' '.join(state))
            i+=1
            templatefiles.append(filename)

    print str(len(rawTemplates))+" template files generated"

    return templatefiles