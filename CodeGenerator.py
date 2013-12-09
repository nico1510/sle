from jinja2 import Template, Environment, PackageLoader, FileSystemLoader
from FsmlModule import parseFSM

with open("./TurnstileHandler_generated.py","w") as handlerFile, open("./TurnstileStepper_generated.py","w") as stepperFile:

    actions = set()
    transitions = []

    fsm = parseFSM()
    for _, [stateDeclaration] in fsm.iteritems():
        for _, [(action, _)] in stateDeclaration["transitions"].iteritems():
            actions.add(action)

    for fromState, [stateDeclaration] in fsm.iteritems():
        if stateDeclaration["initial"]:
            initialState = fromState
        for input, [(action, toState)] in stateDeclaration["transitions"].iteritems():
            transitions.insert(0,(fromState, input, action, toState))

    env = Environment(loader=FileSystemLoader('./templates'))
    handlerTemplate = env.get_template('handler_template')
    stepperTemplate = env.get_template('stepper_template')

    handlerClass = handlerTemplate.render(actions=actions)
    stepperClass = stepperTemplate.render(initialState=initialState, transitions=transitions)

    handlerFile.write(handlerClass)
    stepperFile.write(stepperClass)

    print "Handler & Stepper generated"