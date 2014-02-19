import os
from random import randint
from jinja2 import FileSystemLoader, Environment
from FalseFSMGenerator import createWrongFSM
from SyntaxGenerator import generateRawTemplates
from FalseInputGenerator import generateInfeasibleInput, generateIllegalInput


def generateJinjaTemplateFile(filename, produceError):
    templatefile = open(filename, 'r')
    content = templatefile.read().split()
    noStates = 0
    currentState = None
    currentTransition = None
    transList = []
    errorPosition = 0 # default case no error is produced

    if produceError:
        if not "#stateDecl#" in content or not "#input#" in content:
            errorPosition = randint(1,3)  # no matter how small the fsm is, it is always possible to insert a parser error at these positions
        else:
            errorPosition = randint(1,7)  # if the fsm has any transitions, there are more possibilities to insert a parser error

    for index, token in enumerate(content):

        if errorPosition==1 and "initial" in token:
            content[index] = "initail"

        if errorPosition==2 and "state" in token:
            content[index] = "states"

        if "#initState#" in token:
            content[index] = "{{ states[0].name }} {" if errorPosition==3 else "{{ states[0].name }}"
            currentState = 0
            currentTransition = -1
            transList.insert(0,0)

        if "#stateDecl#" in token:
            noStates += 1
            currentState = noStates
            content[index] = "{{ states[" + str(currentState) + "].name }} ]" if errorPosition==4 else "{{ states[" + str(currentState) + "].name }}"
            currentTransition = -1
            transList.append(0)

        if "#input#" in token:
            currentTransition += 1
            transList[currentState]=currentTransition+1
            content[index] = "{{ states[" + str(currentState) + "].transitions[" + str(currentTransition) + "].input }} X" if errorPosition==5 else "{{ states[" + str(currentState) + "].transitions[" + str(currentTransition) + "].input }}"

        if "#action#" in token:
            content[index] = "/ {{ states[" + str(currentState) + "].transitions[" + str(currentTransition) + "].action }}" if errorPosition==6 else "{{ states[" + str(currentState) + "].transitions[" + str(currentTransition) + "].action }}"

        if "#newState#" in token:
            content[index] = "_ {{ states[" + str(currentState) + "].transitions[" + str(currentTransition) + "].newstate }}" if errorPosition==7 else "{{ states[" + str(currentState) + "].transitions[" + str(currentTransition) + "].newstate }}"


    templatefile.close()
    templatefile = open(filename, 'w')
    templatefile.write(' '.join(content))

    return transList

def generateNegativeTestData(depth, error):

    templatefiles = generateRawTemplates(depth)
    env = Environment(loader=FileSystemLoader('.'))
    count = 0

    for file in templatefiles:
        # after this command, the placeholders of the file are replaced with jinja placeholders
        transList = generateJinjaTemplateFile(file, error=='parsererror')

        try:
            # generate wrong .fsml File
            fsm = createWrongFSM(transList, error)
            template = env.get_template(file)
            fsmlData = template.render(states=fsm)
            fsmlFile = open(os.path.join("./testdata/negative/fsm", error, "sample"+file.split("template")[2]+".fsml"), 'w')
            fsmlFile.write(fsmlData)

            # generate wrong input .json File
            #correctInput, correctOutput = generateCorrectInput(fsm)
            #inputFile = open(os.path.join("./testdata/negative/input", error, "input"+file.split("template")[2]+".json"), 'w')
            #inputFile.write(json.dumps(correctInput))

            count += 1

        except ValueError:
            os.remove(file)

    print str(count)+" test-data files generated"
