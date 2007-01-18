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

""" yselect's main menu. """

import curses

import menu
import observable

__revision__ = "$Rev$"

class MenuEntry(object):

    """
    Object representation of a menu entry.
    """

    def __init__(self, action, display, description, shortcut_key):
        self.action = action
        self.action_display = display
        self.description = description
        self.shortcut_key = shortcut_key


class MainMenuModel(observable.Observable, menu.MenuModel):

    """
    yselect main menu data model.
    """

    def __init__(self, program_name):
        observable.Observable.__init__(self)
        menu.MenuModel.__init__(self)

        self.entries = []
        self.entries.append(MenuEntry("update", "[U]pdate",
            "Update list of available packages, if possible.", 'u'))
        self.entries.append(MenuEntry("select", "[S]elect",
            "Request which packages you want on your system.", 's'))
        self.entries.append(MenuEntry("install", "[I]nstall",
            "Install and upgrade wanted packages.", 'i'))
        self.entries.append(MenuEntry("remove", "[R]emove",
            "Remove unwanted software.", 'r'))
        self.entries.append(MenuEntry("quit", "[Q]uit",
            "Quit %s." % (program_name), 'q'))

        for entry in self.entries:
            self.register_signal(entry.action)

    def move_up(self):
        """
        Move the menu cursor up one entry.

        We only move up if we're not already at the top of the list.
        If we are, we wrap to the bottom.
        """
        if self.selected_entry > 0:
            self.selected_entry = self.selected_entry - 1
        else:
            self.selected_entry = len(self.entries) - 1

    def move_down(self):
        """
        Move the menu cursor down an entry.

        We only move if we're not already at the bottom of the list.
        If we are, we wrap to the top.
        """
        if self.selected_entry < len(self.entries) - 1:
            self.selected_entry = self.selected_entry + 1
        else:
            self.selected_entry = 0
           
    def select_current(self):
        """ Select the currently highlighted entry. """
        self.select(self.selected_entry)
       
    def select(self, selection):
        """ Select the entry at selection. """
        if (selection < 0 or selection > len(self.entries)):
            raise IndexError
        self.emit_signal(self.entries[selection].action)

class MainMenuController(menu.MenuController):

    """
    yselect main menu input handler.
    """

    def __init__(self, model):
        super(MainMenuController, self).__init__(model)

    def handle_input(self, key):
        """ React to keyboard input. """
        #Try Super's implementation first.
        handled = super(MainMenuController, self).handle_input(key)
        if not handled:
            for entry in self._model.entries:
                entry_num = self._model.entries.index(entry)
                if key == ord(entry.shortcut_key) or key == ord(str(entry_num)):
                    self._model.selected_entry = entry_num
                    handled = True
                    break

        return handled


class MainMenuView(menu.MenuView):

    """
    yselect main menu screen.
    """

    def __init__(self, stdscr, menu_model, program_name, program_version):

        super(MainMenuView, self).__init__(menu_model)
        self.stdscr = stdscr

        self.title = \
            "RPM/Yum `%s' package handling frontend." % (program_name)

        self.navigation_info = \
            "Move around with ^P and ^N, cursor keys, initial letters, " + \
            "or digits;\n" + \
            "Press <enter> to confirm selection.  ^L redraws screen."

        self.copyright = \
            "Version %s (noarch).\n" + \
            "Copyright (C) 2006 Devan Goodwin.\n" + \
            "Copyright (C) 2006, 2007 James Bowes.\n" + \
            "This is free software; see the GNU General Public Licence " + \
            "version 2\n" + \
            "or later for copying conditions.  There is NO warrenty.  See\n" + \
            "%s --licence for details.\n"

        self.copyright = self.copyright % (program_version, program_name)

    def paint(self):
        """
        Draw or refresh the main menu onscreen.
        """
        self.stdscr.addstr(0, 0, self.title, curses.A_BOLD)

        (height, width) = self.stdscr.getmaxyx()

        x_pos = 2
        i = 0
        for menu_entry in self._model.entries:

            if menu_entry == self._model.entries[self._model.selected_entry]:
                prefix = " * "
                format = curses.A_REVERSE
            else:
                prefix = "   "
                format = curses.A_NORMAL

            entry_string = "%s %d. %-11.11s %-80.80s" % \
                (prefix, i, menu_entry.action_display, menu_entry.description)
            self.stdscr.addnstr(x_pos, 0, entry_string, width, format)
            x_pos = x_pos + 1
            i = i + 1

        x_pos = x_pos + 1
        self.stdscr.addstr(x_pos, 0, self.navigation_info, curses.A_BOLD)

        x_pos = x_pos + 3 # The previous string was two lines
        self.stdscr.addstr(x_pos, 0, self.copyright)

        self.stdscr.refresh()
