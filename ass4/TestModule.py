import glob
import sys
import unittest

sys.path.append("../ass2")

from MainFSM import parseFSM
from ConstraintChecker import ok
from FsmExceptions import *
from DataGenerator import generateTestFiles


class DataTestCase(unittest.TestCase):
    def __init__(self, testdataFile):
        unittest.TestCase.__init__(self, methodName='testOneFile')
        self.testdataFile = testdataFile

    def testOneFile(self):
        fsm = parseFSM(self.testdataFile)
        self.assertTrue(ok(fsm))

    def shortDescription(self):
        return 'TestCase for file %s' % self.testdataFile


def get_test_data_suite():
    generateTestFiles(8)
    testFiles = glob.glob('./testdata/*.fsml')
    return unittest.TestSuite([DataTestCase(testFile) for testFile in testFiles])

if __name__ == '__main__':
    testRunner = unittest.TextTestRunner()
    testRunner.run(get_test_data_suite())