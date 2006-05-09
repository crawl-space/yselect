#   yselect - An RPM/Yum package handling frontend.
#   Copyright (C) 2006 James Bowes <jbowes@redhat.com> 
#   Copyright (C) 2006 Devan Goodwin <dg@fnordia.org>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
#   02110-1301  USA

import unittest
import settestpath

import mainmenu

class MainMenuModelTests(unittest.TestCase):

    def setUp(self):
        self.model = mainmenu.MainMenuModel("program name")
   
    def testSelectBorderValues(self):
        try:
            self.model.select(-1)
            self.fail()
        except:
            # Expected, do nothing.
            pass
  
        try:
            self.model.select(len(self.model.entries))
            self.fail()
        except:
            pass
        
        try:
            self.model.select(0)
        except:
            self.fail()

        try:
            self.model.select(len(self.model.entries) - 1)
        except:
            self.fail()

    def testSignals(self):
        observer = TestObserver()
        self.model.add_observer("quit", observer)
        self.model.add_observer("select", observer)
        
        self.model.emit_signal("quit")
        self.assertTrue(observer.been_notified)
        self.assertEquals("quit", observer.notified_signal)
        observer.reset()

        self.model.emit_signal("select")
        self.assertTrue(observer.been_notified)
        self.assertEquals("select", observer.notified_signal)

class TestObserver:

    def __init__(self):
        self.been_notified = False
        self.notified_signal = None

    def notify(self, observable, signal_name):
        self.been_notified = True
        self.notified_signal = signal_name

    def reset(self):
        self.been_notified = False
        self.notified_signal = None

def suite():
    return unittest.makeSuite(MainMenuModelTests)

if __name__ == "__main__":
    unittest.main(defaultTest="suite")
