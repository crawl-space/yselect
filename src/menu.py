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

import curses

__revision__ = "$Rev$"

class Menu:
    """
    Parent Menu class. Maintains a reference to the currently selected menu entry.
    """

    def __init__(self):
        self.selectedEntry = 0
        self.entries = []

    def handle_input(self, char):
        """ React to the provided input. """

        handled = True
        
        # 16 is CTRL+p
        if char == curses.KEY_UP or char == ord('k') or char == 16:
            self.move_up()
        # 14 is CTRL+n    
        elif char == curses.KEY_DOWN or char == ord('j') or char == 14:
            self.move_down()
        # 10 is another 'ENTER' or return key or whatever. I needed it for my
        # keyboard.
        elif char == curses.KEY_ENTER or char == 10:
            self.select_current()
        else:
            # We didn't handle the input.
            handled = False

        return handled

    def move_up(self):
        """
        Move the menu cursor up one entry.

        We only move up if we're not already at the top of the list. If we are,
        we wrap to the bottom.
        """
        if self.selectedEntry > 0:
            self.selectedEntry = self.selectedEntry - 1
        else:
            self.selectedEntry = len(self.entries) - 1

    def move_down(self):
        """
        Move the menu cursor down an entry.

        We only move if we're not already at the bottom of the list. If we are,
        we wrap to the top.
        """
        if self.selectedEntry < len(self.entries) - 1:
            self.selectedEntry = self.selectedEntry + 1
        else:
            self.selectedEntry = 0

    def paint(self):
        """
        Draw or refresh the menu onscreen.
        """
        raise NotImplementedError

	def select_current(self):
		"""
		Act upon the currently selected menu item.
		"""
		raise NotImplementedError

