import unittest
import alltests

class NotARealTestSuite(unittest.TestCase):

    def testSomething(self):
        pass

    def testSomethingElse(self):
        pass

def suite():
    result = unittest.TestSuite()
    # TODO: Shouldn't have to manually add all test classes:
    result.addTest(unittest.makeSuite(NotARealTestSuite))
    return result

if __name__ == "__main__":
    unittest.main(defaultTest="suite")

