import glob
import os
from jinja2 import FileSystemLoader, Environment
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
            content[index] = "{{ states[0].name }}"
            currentState = 0
            currentTransition = -1
            edgeList.insert(0,0)

        if "#stateDecl#" in token:
            noStates += 1
            currentState = noStates
            content[index] = "{{ states[" + str(currentState) + "].name }}"
            currentTransition = -1
            edgeList.append(0)

        if "#input#" in token:
            currentTransition += 1
            edgeList[currentState]=currentTransition+1
            content[index] = "{{ states[" + str(currentState) + "].transitions[" + str(currentTransition) + "].input }}"

        if "#action#" in token:
            content[index] = "{{ states[" + str(currentState) + "].transitions[" + str(currentTransition) + "].action }}"

        if "#newState#" in token:
            content[index] = "{{ states[" + str(currentState) + "].transitions[" + str(currentTransition) + "].newstate }}"
    templatefile.close()
    templatefile = open(filename, 'w')
    templatefile.write(' '.join(content))

    return edgeList


oldFiles = glob.glob('./templates/template*')+glob.glob('./testdata/*.fsml')
for f in oldFiles:
    os.remove(f)

templatefiles = generateRawTemplates(7)
env = Environment(loader=FileSystemLoader('.'))
count = 0

for file in templatefiles:
    # after this command, the placeholders of the file are replaced with jinja placeholders
    edgeList = generateTemplate(file)

    try:
        g = createSpecificRandomGraph(edgeList)
        states = graphAsList(g, edgeList)
        template = env.get_template(file)
        testdata = template.render(states=states)
        testdataFile = open(os.path.join("./testdata", "sample"+file.split("template")[2]+".fsml"), 'w')
        testdataFile.write(testdata)
        count += 1

    except ValueError:
        os.remove(file)

print str(count)+" test-data files generated"