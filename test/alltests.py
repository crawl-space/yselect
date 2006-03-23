import unittest
import sys

import yselectTests

# Adjust path so we can see the src modules running from branch as well as test dir:
sys.path.append('./src/')
sys.path.append('../src/')

def suite():
    result = unittest.TestSuite()

    # Must add all modules here at this point in time
    # TODO: Find a way to search these out:
    result.addTest(yselectTests.suite())

    return result

if __name__ == "__main__":
    unittest.main(defaultTest="suite")

