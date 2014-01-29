from random import randint
import string
import pygraphviz as pgv


def randomWord():
    wordlength = randint(2,10)
    word = ""
    for i in range(wordlength):
        word += string.ascii_lowercase[randint(0,25)]
    return word

def randomEdgeName(node, g, edgeNames):
    nodeEdges = set([d for u,v,d in g.edges(nbunch=[node], keys=True)])
    remainingEdgeNames = set(edgeNames).difference(nodeEdges)
    if not remainingEdgeNames:
        newlabel = randomWord()
        # this while loop just makes sure that no random duplicates are created by accident
        while newlabel in edgeNames:
            newlabel = randomWord()
        edgeNames.append(newlabel)
        return newlabel
    else:
        return list(remainingEdgeNames)[randint(0,len(remainingEdgeNames)-1)]


def nodeToDict(g, nodeName):
    nodeDict = dict()
    nodeDict["name"] = nodeName
    nodeDict["transitions"] = []
    for startState, newState, input in g.edges(nbunch=[nodeName], keys=True):
        transDict = dict()
        transDict["input"] = input
        transDict["newstate"] = newState
        transDict["action"] = "action"
        nodeDict["transitions"].append(transDict)
    return nodeDict


def graphAsList(g, edgeList):

    nodes = g.nodes()

    # turn initial state into dict
    initialStateDict = nodeToDict(g, nodes.pop(0))
    # put initial state at head of the list
    graphList = [initialStateDict]

    # append dicts of all other states to list
    for edgeCount in edgeList[1:]:
        nodeWithCorrectEdges = [node for node in nodes if len(g.edges(nbunch=[node]))==edgeCount].pop()
        nodes.remove(nodeWithCorrectEdges)
        nodeDict = nodeToDict(g, nodeWithCorrectEdges)
        graphList.append(nodeDict)

    return graphList


def createRandomGraph(noNodes, noEdges):

    if noEdges < noNodes-1:
        raise ValueError("Can not construct a valid graph with given input")

    nodeNames = [randomWord() for i in range(noNodes)]
    # this while loop is only run if the random word generator accidently generates duplicate words
    while len(set(nodeNames)) < len(nodeNames):
        nodeNames = [randomWord() for i in range(noNodes)]

    edgeNames = []

    g = pgv.AGraph(title="Random FSM", directed=True, strict=False, rankdir='LR', nodesep=.5)

    g.add_node(nodeNames.pop(0), shape='ellipse', style='filled')
    noNodes -= 1

    for i in range(noNodes):
        newNode = nodeNames.pop()
        randomNode = g.nodes()[randint(0, len(g.nodes())-1)]
        g.add_node(newNode, shape='ellipse')
        edgename = randomEdgeName(randomNode, g, edgeNames)
        g.add_edge(randomNode, newNode, key=edgename, label=edgename)


    remainingEdges = noEdges - noNodes

    for i in range(remainingEdges):
        randomNode1 = g.nodes()[randint(0, len(g.nodes())-1)]
        randomNode2 = g.nodes()[randint(0, len(g.nodes())-1)]
        edgename = randomEdgeName(randomNode1, g, edgeNames)
        g.add_edge(randomNode1, randomNode2, key=edgename, label=edgename)

    return g

def createSpecificRandomGraph(edgeNumberList):

    noNodes = len(edgeNumberList)
    noEdges = sum(edgeNumberList)

    if noEdges < noNodes-1 or edgeNumberList[0]==0:
        raise ValueError("Can not construct a valid graph with given input")


    nodeNames = [randomWord() for i in range(noNodes)]
    # this while loop is only run if the random word generator accidently generates duplicate words
    while len(set(nodeNames)) < len(nodeNames):
        nodeNames = [randomWord() for i in range(noNodes)]

    edgeNames = []
    currentEdgeCountMap = dict()
    requiredEdgeCountMap = dict()

    for requiredEdges, node in zip([edgeNumberList[0]]+sorted(edgeNumberList[1:], reverse=True), nodeNames):
        currentEdgeCountMap[node] = 0
        requiredEdgeCountMap[node] = requiredEdges

    g = pgv.AGraph(title="Random FSM", directed=True, strict=False, rankdir='LR', nodesep=.5)
    # add the initial node
    g.add_node(nodeNames.pop(0), shape='ellipse', style='filled')
    noNodes -= 1

    stillNeedEdges = [node for node in g.nodes() if currentEdgeCountMap[node]<requiredEdgeCountMap[node]]

    for i in range(noNodes):
        newNode = nodeNames.pop(0)
        randomNode = stillNeedEdges[randint(0, len(stillNeedEdges)-1)]
        g.add_node(newNode, shape='ellipse')
        edgename = randomEdgeName(randomNode, g, edgeNames)
        g.add_edge(randomNode, newNode, key=edgename, label=edgename)
        currentEdgeCountMap[randomNode] += 1
        stillNeedEdges = [node for node in g.nodes() if currentEdgeCountMap[node]<requiredEdgeCountMap[node]]


    remainingEdges = noEdges - noNodes

    for i in range(remainingEdges):
        randomNode1 = stillNeedEdges[randint(0, len(stillNeedEdges)-1)]
        randomNode2 = g.nodes()[randint(0, len(g.nodes())-1)]
        edgename = randomEdgeName(randomNode1, g, edgeNames)
        g.add_edge(randomNode1, randomNode2, key=edgename, label=edgename)
        currentEdgeCountMap[randomNode1] += 1
        stillNeedEdges = [node for node in g.nodes() if currentEdgeCountMap[node]<requiredEdgeCountMap[node]]


    return g

#g = createSpecificRandomGraph([2, 2, 0])
#g.layout(prog='dot')
#g.draw('random.png')
