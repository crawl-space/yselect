"""
Tests for the observable class.

Copyright (C) 2006 James Bowes <jbowes@redhat.com>
"""

import unittest
import alltests

import observable

class ObservableTests(unittest.TestCase):

    def setUp(self):
        self.observable = TestObservable()
    
    def testRegisterSignal(self):
        test_observable = observable.Observable()
        test_observable.register_signal("bounce")

        self.assertEquals(len(test_observable.signals), 1)

    def testRegisterDuplicateSignal(self):
        test_observable = observable.Observable()
        test_observable.register_signal("bounce")
        test_observable.register_signal("bounce")

        self.assertEquals(len(test_observable.signals), 1)

    def testAddObserver(self):
        observer = TestObserver()
        self.observable.add_observer("bark", observer) 
        self.assertEquals(len(self.observable.signals["bark"]), 1)

    def testAddObserverDuplicateObserver(self):
        observer = TestObserver()
        self.observable.add_observer("bark", observer)
        self.observable.add_observer("bark", observer)
        self.assertEquals(len(self.observable.signals["bark"]), 1)

    def testAddObserverNoSignal(self):
        observer = TestObserver()
        try:
            self.observable.add_observer("blonk", observer)
            self.fail()
        except observable.NoSuchSignalException:
            pass

    def testEmitSignal(self):
        observer = TestObserver()
        self.observable.add_observer("bark", observer)
        self.observable.emit_signal("bark")

        self.assertTrue(observer.been_notified)

class TestObservable(observable.Observable):
    
    def __init__(self):
        observable.Observable.__init__(self)
        self.register_signal("bark")


class TestObserver:

    def __init__(self):
        self.been_notified = False

    def notify(self, observable):
        self.been_notified = True


def suite():
    result = unittest.TestSuite()
    # TODO: Shouldn't have to manually add all test classes:
    result.addTest(unittest.makeSuite(ObservableTests))
    return result


if __name__ == "__main__":
    unittest.main(defaultTest="suite")

