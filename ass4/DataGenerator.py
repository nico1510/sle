import glob
import os
from jinja2 import FileSystemLoader, Environment
from FSMGenerator import createSpecificFSM
from SyntaxGenerator import generateRawTemplates


def generateTemplate(filename):
    templatefile = open(filename, 'r')
    content = templatefile.read().split()
    noStates = 0
    currentState = None
    currentTransition = None
    transList = []

    for index, token in enumerate(content):
        if "#initState#" in token:
            content[index] = "{{ states[0].name }}"
            currentState = 0
            currentTransition = -1
            transList.insert(0,0)

        if "#stateDecl#" in token:
            noStates += 1
            currentState = noStates
            content[index] = "{{ states[" + str(currentState) + "].name }}"
            currentTransition = -1
            transList.append(0)

        if "#input#" in token:
            currentTransition += 1
            transList[currentState]=currentTransition+1
            content[index] = "{{ states[" + str(currentState) + "].transitions[" + str(currentTransition) + "].input }}"

        if "#action#" in token:
            content[index] = "{{ states[" + str(currentState) + "].transitions[" + str(currentTransition) + "].action }}"

        if "#newState#" in token:
            content[index] = "{{ states[" + str(currentState) + "].transitions[" + str(currentTransition) + "].newstate }}"
    templatefile.close()
    templatefile = open(filename, 'w')
    templatefile.write(' '.join(content))

    return transList

def generateTestFiles(depth):
    oldFiles = glob.glob('./templates/template*')+glob.glob('./testdata/*.fsml')
    for f in oldFiles:
        os.remove(f)

    templatefiles = generateRawTemplates(depth)
    env = Environment(loader=FileSystemLoader('.'))
    count = 0

    for file in templatefiles:
        # after this command, the placeholders of the file are replaced with jinja placeholders
        transList = generateTemplate(file)

        try:
            fsm = createSpecificFSM(transList)
            template = env.get_template(file)
            testdata = template.render(states=fsm)
            testdataFile = open(os.path.join("./testdata", "sample"+file.split("template")[2]+".fsml"), 'w')
            testdataFile.write(testdata)
            count += 1

        except ValueError:
            os.remove(file)

    print str(count)+" test-data files generated"