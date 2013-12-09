from jinja2 import Template, Environment, PackageLoader, FileSystemLoader
from FsmlModule import parseFSM

with open("./TurnstileHandler_generated.py","w") as handlerfile:

    actions = set()

    fsm = parseFSM()
    for _, [stateDeclaration] in fsm.iteritems():
        for _, [(action, _)] in stateDeclaration["transitions"].iteritems():
            actions.add(action)

    env = Environment(loader=FileSystemLoader('./templates'))
    template = env.get_template('handler_template')

    s = template.render(actions=actions)
    handlerfile.write(s)
    print "Handler generated"