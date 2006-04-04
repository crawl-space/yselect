"""
Yselect program.

This program is free software, released under the terms of the GPL.

Copyright (C) 2006 James Bowes <jbowes@redhat.com>
Copyright (C) 2006 Devan Goodwin <dg@fnordia.org>
"""

import curses
import curses.wrapper

__revision__ = "$Rev$"

version = "0.0.1"
program_name = "yselect"

class Menu:
    """
    Parent Menu class. Maintains a reference to the currently selected menu entry.
    """

    def __init__(self):
        self.selectedEntry = 0
        self.title = \
            "RPM/Yum `%s' package handling frontend." % (program_name)
        self.entries = []

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

    def select(self):
        """
        Select (act upon) the currently hilighted menu entry.
        """
        raise NotImplementedError

    def paint(self):
        """
        Draw or refresh the menu onscreen.
        """
        raise NotImplementedError

	def selectCurrent(self):
		"""
		Act upon the currently selected menu item.
		"""
		raise NotImplementedError

class MenuEntry:
    """
    Object representation of a menu entry.
    """

    # TODO: Remove default method None:
    def __init__(self, action, display, description, execute_method,
        shortcut_key):
        self.action = action
        self.action_display = display
        self.description = description
        self.execute_method = execute_method
        self.shortcut_key = shortcut_key

class MainMenu(Menu):

    """
    yselect main menu screen.
    """

    def __init__(self, stdscr):

        Menu.__init__(self)
        self.stdscr = stdscr

        self.entries.append(MenuEntry("update", "[U]pdate",
            "Update list of available packages, if possible.", None, 'u'))
        self.entries.append(MenuEntry("select", "[S]elect",
            "Request which packages you want on your system.", None, 's'))
        self.entries.append(MenuEntry("install", "[I]nstall",
            "Install and upgrade wanted packages.", None, 'i'))
        self.entries.append(MenuEntry("remove", "[R]emove",
            "Remove unwanted software.", None, 'r'))
        self.entries.append(MenuEntry("quit", "[Q]uit",
                "Quit %s." % (program_name), None, 'q'))

        self.navigation_info = \
            "Move around with ^P and ^N, cursor keys, initial letters, " + \
            "or digits;\n" + \
            "Press <enter> to confirm selection.  ^L redraws screen."
        self.copyright = \
            "Version %s.\n" + \
            "Copyright (C) 2006 Devan Goodwin.\n" + \
            "Copyright (C) 2006 James Bowes.\n" + \
            "This is free software; see the GNU General Public Licence " + \
            "version 2\n" + \
            "or later for copying conditions.  There is NO warrenty.  See\n" + \
            "%s --licence for details.\n"

        self.copyright = self.copyright % (version, program_name)

    def paint(self):
        """
        Draw or refresh the main menu onscreen.
        """
        self.stdscr.addstr(0, 0, self.title, curses.A_BOLD)

        (height, width) = self.stdscr.getmaxyx()

        x_pos = 2
        i = 0
        for menu_entry in self.entries:

            if menu_entry == self.entries[self.selectedEntry]:
                prefix = " * "
                format = curses.A_REVERSE
            else:
                prefix = "   "
                format = curses.A_NORMAL

            entry_string = "%s %d. %-11.11s %-80.80s" % (prefix, i, menu_entry.action_display, menu_entry.description)
            self.stdscr.addnstr(x_pos, 0, entry_string, width, format)
            x_pos = x_pos + 1
            i = i + 1

        x_pos = x_pos + 1
        self.stdscr.addstr(x_pos, 0, self.navigation_info, curses.A_BOLD)

        x_pos = x_pos + 3 # The previous string was two lines
        self.stdscr.addstr(x_pos, 0, self.copyright)

    def selectCurrent(self):
        raise Exception
        self.entries[self.selectedEntry].executeMethod()

class SelectMenu(Menu):
    """
    Main package listing.
    """

    def __init__(self):
        Menu.__init__(self)

    def paint(self, window):
        """
        Draw or refresh the main menu onscreen.
        """
        window.addstr(0, 0, self.title, curses.A_BOLD)

class MainApplication:

    """
    Application driver class.
    """

    def run(self, screen):
        """
		The main event loop for the application.
		"""

		# Start out with the main menu:
        currentMenu = MainMenu(screen)

        currentMenu.paint()
        screen.refresh()

        while True:
            char = screen.getch()

            if char == ord('q'):
                break
            elif char == curses.KEY_UP or char == ord('k') or char == 16:
                currentMenu.move_up()
            elif char == curses.KEY_DOWN or char == ord('j') or char == 14:
                currentMenu.move_down()
            elif char == curses.KEY_ENTER or char == 10:
                currentMenu.selectCurrent()

            currentMenu.paint()

def main(screen):
    yselect = MainApplication()
    yselect.run(screen)

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        # We don't want to complain on ctrl-c
        pass
