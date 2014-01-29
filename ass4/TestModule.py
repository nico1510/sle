import glob
import sys

sys.path.append("../ass2")

from MainFSM import parseFSM
from ConstraintChecker import ok
from FsmExceptions import *

testFiles = glob.glob('./testdata/*.fsml')

for f in testFiles:
    try:
        fsm = parseFSM(f)
        ok(fsm)
    except FsmException:
        print f+" failed"