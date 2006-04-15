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
import alltests

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


def suite():
    result = unittest.TestSuite()
    # TODO: Shouldn't have to manually add all test classes:
    result.addTest(unittest.makeSuite(MainMenuModelTests))
    return result


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
