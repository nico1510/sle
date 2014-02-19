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

# Code for testing all valid fsml files

class parsererrorTestCase(unittest.TestCase):

    def __init__(self, fsmlFile):
        unittest.TestCase.__init__(self, methodName='testOneFile')
        self.fsmlFile = fsmlFile

    def testOneFile(self):
        self.assertRaises(FsmParseException, parseFSM, self.fsmlFile)

    def shortDescription(self):
        return 'TestCase for file %s' % self.fsmlFile

def parsererrorTestSuite():
    # delete old test data
    for path, _, files in os.walk("./testdata/negative/fsm/parsererror"):
        for testfile in files:
            if not testfile == ".gitignore":
                os.remove(os.path.join(path, testfile))

    # generate new test data
    generateNegativeTestData(7,'parsererror')

    fsmlFiles = glob.glob('./testdata/negative/fsm/parsererror/*.fsml')
    return unittest.TestSuite([parsererrorTestCase(fsmlFile) for fsmlFile in fsmlFiles])

# main module Code for running all the tests

if __name__ == '__main__':
    testRunner = unittest.TextTestRunner()
    testRunner.run(parsererrorTestSuite())
