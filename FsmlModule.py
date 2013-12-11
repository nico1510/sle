import json
import antlr3
from FsmlLexer import FsmlLexer
from FsmlParser import FsmlParser
from OkFSM import ok
from SimulateFSM import simulateFSM
from CodeGenerator import generateCode
from Drawer import drawFSM

def parseFSM():
    char_stream = antlr3.ANTLRInputStream(open("./sample.fsml", 'r'))
    lexer = FsmlLexer(char_stream)
    tokens = antlr3.CommonTokenStream(lexer)
    parser = FsmlParser(tokens)
    parser.fsm()
    return parser.fsmObject


fsm = parseFSM()

sampleInput = json.load(open("./sample_input.json", "r"))

# just for visualization of the fsm dict
jsonFile = open("./sample_fsml.json", 'w')
jsonFile.write(json.dumps(fsm))

if ok(fsm):
    #simulate the fsm
    output = simulateFSM(fsm, sampleInput)
    # dump the simulation output to file
    outFile = open("./sample_output.json", 'w')
    outFile.write(json.dumps(output))

    #generate Code
    generateCode(fsm)

    #draw fsm
    drawFSM(fsm)


