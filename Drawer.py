import pygraphviz
from FsmlModule import parseFSM


fsm = parseFSM()

fsm_graph = pygraphviz.AGraph(title="Sample FSM", directed=True, strict=False, rankdir='LR', nodesep=.5)

for fromState, [stateDeclaration] in fsm.iteritems():
    if stateDeclaration["initial"]:
        fsm_graph.add_node(n=fromState, shape='ellipse', style='filled')
    else:
        fsm_graph.add_node(n=fromState, shape='ellipse')


for fromState, [stateDeclaration] in fsm.iteritems():
    for input, [(action, toState)] in stateDeclaration["transitions"].iteritems():
        fsm_graph.add_edge(fromState, toState, label=input +"/"+action)

fsm_graph.write("./sample_graph.dot")