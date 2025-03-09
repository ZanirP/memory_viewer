import unittest

from .testAdd import TestInstructionParser as TestAdd
from .testAnd import TestInstructionParser as TestAnd
from .testEOR import TestInstructionParser as TestEOR
from .testLDR import TestInstructionParser as TestLDR
from .testLSL import TestInstructionParser as TestLSL
from .testLSR import TestInstructionParser as TestLSR
from .testORR import TestInstructionParser as TestORR
from .testSTR import TestInstructionParser as TestSTR
from .testSUB import TestInstructionParser as TestSUB

def suite():
	suite = unittest.TestSuite()
	suite.addTest(TestAdd())
	suite.addTest(TestAnd())
	suite.addTest(TestEOR())
	suite.addTest(TestLDR())
	suite.addTest(TestLSL())
	suite.addTest(TestLSR())
	suite.addTest(TestORR())
	suite.addTest(TestSTR())
	suite.addTest(TestSUB())
	return suite

if __name__ == '__main__':
	runner = unittest.TextTestRunner()
	runner.run(suite())