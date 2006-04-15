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
import sys

# Adjust path so we can see the src modules running from branch as well as test dir:
sys.path.append('./src/')
sys.path.append('../src/')

import yselectTests
import observabletests
import mainmenutests

def suite():
    result = unittest.TestSuite()

    # Must add all modules here at this point in time
    # TODO: Find a way to search these out:
    result.addTest(yselectTests.suite())
    result.addTest(observabletests.suite())
    result.addTest(mainmenutests.suite())

    return result

if __name__ == "__main__":
    unittest.main(defaultTest="suite")

