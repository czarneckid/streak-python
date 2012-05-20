import unittest

from streak_test_case import StreakTestCase

def all_tests():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(StreakTestCase))
  return suite
