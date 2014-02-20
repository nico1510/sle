import glob
import json
import os
import sys
import unittest

sys.path.append("../ass2")

from MainFSM import parseFSM
from ConstraintChecker import ok
from FsmExceptions import *
from FalseDataGenerator import generateNegativeTestData
from Simulator import simulateFSM
from CodeGenerator import generateCode


class parsererrorTestCase(unittest.TestCase):

    def __init__(self, fsmlFile):
        unittest.TestCase.__init__(self, methodName='testOneFile')
        self.fsmlFile = fsmlFile

    def testOneFile(self):
        self.assertRaises(FsmParseException, parseFSM, self.fsmlFile)

    def shortDescription(self):
        return 'TestCase for file %s' % self.fsmlFile

def parsererrorTestSuite(depth):
    # generate new test data
    generateNegativeTestData(depth,'parsererror')

    fsmlFiles = glob.glob('./testdata/negative/fsm/parsererror/*.fsml')
    return unittest.TestSuite([parsererrorTestCase(fsmlFile) for fsmlFile in fsmlFiles])

class infeasibleInputTestCase(unittest.TestCase):

    def __init__(self, fsmlFile, inputFile):
        unittest.TestCase.__init__(self, methodName='testOneFile')
        self.fsmlFile = fsmlFile
        self.inputFile = inputFile

    def testOneFile(self):
        fsm = parseFSM(self.fsmlFile)
        with open(self.inputFile) as inputFile:
            self.assertRaises(InfeasibleSymbolException, simulateFSM, fsm, json.load(inputFile))

    def shortDescription(self):
        return 'TestCase for file %s and input %s' % (self.fsmlFile, self.inputFile)

def infeasibleInputTestSuite(depth):
    # generate new test data
    generateNegativeTestData(depth,'infeasible')

    fsmlFiles = sorted(glob.glob('./testdata/negative/input/infeasible/fsm/*.fsml'))
    inputFiles = sorted(glob.glob('./testdata/negative/input/infeasible/*.json'))
    return unittest.TestSuite([infeasibleInputTestCase(fsmlFile, inputFile) for fsmlFile, inputFile in zip(fsmlFiles, inputFiles)])

class IllegalInputTestCase(unittest.TestCase):

    def __init__(self, fsmlFile, inputFile):
        unittest.TestCase.__init__(self, methodName='testOneFile')
        self.fsmlFile = fsmlFile
        self.inputFile = inputFile

    def testOneFile(self):
        fsm = parseFSM(self.fsmlFile)
        with open(self.inputFile) as inputFile:
            self.assertRaises(IllegalSymbolException, simulateFSM, fsm, json.load(inputFile))

    def shortDescription(self):
        return 'TestCase for file %s and input %s' % (self.fsmlFile, self.inputFile)

def illegalInputTestSuite(depth):
    # generate new test data
    generateNegativeTestData(depth,'illegal')

    fsmlFiles = sorted(glob.glob('./testdata/negative/input/illegal/fsm/*.fsml'))
    inputFiles = sorted(glob.glob('./testdata/negative/input/illegal/*.json'))
    return unittest.TestSuite([IllegalInputTestCase(fsmlFile, inputFile) for fsmlFile, inputFile in zip(fsmlFiles, inputFiles)])


class SingleinitialTestCase(unittest.TestCase):

    def __init__(self, fsmlFile):
        unittest.TestCase.__init__(self, methodName='testOneFile')
        self.fsmlFile = fsmlFile

    def testOneFile(self):
        fsm = parseFSM(self.fsmlFile)
        self.assertRaises(SingleInitialException, ok, fsm)

    def shortDescription(self):
        return 'TestCase for file %s' % self.fsmlFile

def singleinitialTestSuite(depth):
    # generate new test data
    generateNegativeTestData(depth,'singleinitial')

    fsmlFiles = glob.glob('./testdata/negative/fsm/singleinitial/*.fsml')
    return unittest.TestSuite([SingleinitialTestCase(fsmlFile) for fsmlFile in fsmlFiles])

# main module Code for running all the tests

if __name__ == '__main__':
    depth = 7
    testRunner = unittest.TextTestRunner()
    testRunner.run(parsererrorTestSuite(depth))
    testRunner.run(infeasibleInputTestSuite(depth))
    testRunner.run(illegalInputTestSuite(depth))
    testRunner.run(singleinitialTestSuite(depth))

