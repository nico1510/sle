import os
from GraphGenerator import createSpecificRandomGraph, graphAsList
from SyntaxGenerator import generateRawTemplates


def generateTemplate(filename):
    templatefile = open(filename, 'r')
    content = templatefile.read().split()
    noStates = 0
    currentState = None
    currentTransition = None
    edgeList = []

    for index, token in enumerate(content):
        if "#initState#" in token:
            content[index] = "states[0].name"
            currentState = 0
            currentTransition = -1
            edgeList.insert(0,0)

        if "#stateDecl#" in token:
            noStates += 1
            currentState = noStates
            content[index] = "states[" + str(currentState) + "].name"
            currentTransition = -1
            edgeList.append(0)

        if "#input#" in token:
            currentTransition += 1
            edgeList[currentState]=currentTransition+1
            content[index] = "states[" + str(currentState) + "].transitions[" + str(currentTransition) + "].input"

        if "#action#" in token:
            content[index] = "states[" + str(currentState) + "].transitions[" + str(currentTransition) + "].action"

        if "#newState#" in token:
            content[index] = "states[" + str(currentState) + "].transitions[" + str(currentTransition) + "].newstate"
    templatefile.close()
    templatefile = open(filename, 'w')
    templatefile.write(' '.join(content))

    return edgeList


templatefiles = generateRawTemplates()

for filename in templatefiles:
    edgeList = generateTemplate(filename)

    try:
        g = createSpecificRandomGraph(edgeList)
        states = graphAsList(g, edgeList)
        print states
        #open filename as correct template with jinja2 and give it states as input

    except ValueError:
        os.remove(filename)