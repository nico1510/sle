import json
import sys
import unittest

sys.path.append('..')
from OkFSM import ok
from FsmlModule import parseFSM
from FsmExceptions import *
from SimulateFSM import simulateFSM

# test cases for the OK Constraints

class TestOkConstraints(unittest.TestCase):

    def setUp(self):
        self.determinismNotOkFsm = parseFSM("./determinismNotOk.fsml")
        self.idsNotOkFsm = parseFSM("./idsNotOk.fsml")
        self.initialNotOkFsm = parseFSM("./initialNotOk.fsml")
        self.reachabilityNotOkFsm = parseFSM("./reachabilityNotOk.fsml")
        self.resolutionNotOkFsm = parseFSM("./resolutionNotOk.fsml")

    def testDeterminism(self):
        self.assertRaises(DeterministicException, ok, self.determinismNotOkFsm)
    def testDistinctIDs(self):
        self.assertRaises(DistinctIdsException, ok, self.idsNotOkFsm)
    def testSingleInitial(self):
        self.assertRaises(SingleInitialException, ok, self.initialNotOkFsm)
    def testReachability(self):
        self.assertRaises(ReachableException, ok, self.reachabilityNotOkFsm)
    def testResolution(self):
        self.assertRaises(ResolvableException, ok, self.resolutionNotOkFsm)


class OtherConstraints(unittest.TestCase):

    def setUp(self):
        self.parserErrorFsm = "./parserError.fsml"

        self.correctFsm = parseFSM("../sample.fsml")
        self.illegalSymbolInput = json.load(open("illegalSymbol_input.json"))
        self.infeasibleSymbolInput = json.load(open("infeasibleSymbol_input.json"))

    def testParserError(self):
        self.assertRaises(FsmParseException, parseFSM, self.parserErrorFsm)
    def testIllegalSymbol(self):
        self.assertRaises(IllegalSymbolException, simulateFSM, self.correctFsm, self.illegalSymbolInput)
    def testInfeasibleSymbol(self):
        self.assertRaises(InfeasibleSymbolException, simulateFSM, self.correctFsm, self.infeasibleSymbolInput)

if __name__ == '__main__':
    unittest.main()