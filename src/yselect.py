"""
Yselect program.

This program is free software, released under the terms of the GPL.

Copyright (C) 2006 James Bowes <jbowes@redhat.com>
Copyright (C) 2006 Devan Goodwin <dg@fnordia.org>
"""

import curses

__revision__ = "$Rev$"

version = "0.0.1"
program_name = "yselect"

class Menu:
    """
    Parent Menu class.
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

    def paint(self, window):
        """
        Draw or refresh the menu onscreen.
        """
        raise NotImplementedError

class MenuEntry:
    """
    Object representation of a menu entry.
    """

    def __init__(self, action, display, description):
        self.action = action
        self.action_display = display
        self.description = description

class MainMenu(Menu):

    """
    yselect main menu screen.
    """

    def __init__(self):

        Menu.__init__(self)

        self.entries.append(MenuEntry("update", "[U]pdate",
            "Update list of available packages, if possible."))
        self.entries.append(MenuEntry("select", "[S]elect",
            "Request which packages you want on your system."))
        self.entries.append(MenuEntry("install", "[I]nstall",
            "Install and upgrade wanted packages."))
        self.entries.append(MenuEntry("remove", "[R]emove",
            "Remove unwanted software."))
        self.entries.append(MenuEntry("quit", "[Q]uit",
                "Quit %s." % (program_name)))

        self.navigation_info = \
            "Move around with ^P and ^N, cursor keys, initial letters, " + \
            "or digits;\n" + \
            "Press <enter> to confirm selection.  ^L redraws screen."
        self.copyright = \
            "Version %s\n" + \
            "Copyright (C) 2006 Devan Goodwin and James Bowes\n" + \
            "This is free software; see the GNU General Public Licence " + \
            "version 2\n" + \
            "or later for copying conditions.  There is NO warrenty.  See\n" + \
            "%s --licence for details.\n"

        self.copyright = self.copyright % (version, program_name)

    def paint(self, window):
        """
        Draw or refresh the main menu onscreen.
        """
        window.addstr(0, 0, self.title, curses.A_BOLD)

        x_pos = 2
        i = 0
        for menu_entry in self.entries:

            if menu_entry == self.entries[self.selectedEntry]:
                prefix = " * "
                format = curses.A_REVERSE
            else:
                prefix = "   "
                format = curses.A_NORMAL

            entry_string = \
                prefix + str(i) + ". " + menu_entry.action_display + "\t" + menu_entry.description
            window.addstr(x_pos, 0, entry_string, format)
            x_pos = x_pos + 1
            i = i + 1

        x_pos = x_pos + 1
        window.addstr(x_pos, 0, self.navigation_info, curses.A_BOLD)

        x_pos = x_pos + 3 # The previous string was two lines
        window.addstr(x_pos, 0, self.copyright)

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

    def __init__(self):
        self.stdscr = MainApplication.__initialize_curses()

    def __del__(self):
        MainApplication.__terminate_curses(self.stdscr)

    def run(self):
        """ The main event loop for the application. """
        menu = MainMenu()

        menu.paint(self.stdscr)
        self.stdscr.refresh()

        while True:
            char = self.stdscr.getch()

            if char == ord('q'):
                break
            elif char == curses.KEY_UP or char == ord('k') or char == 16:
                menu.move_up()
                menu.paint(self.stdscr)
            elif char == curses.KEY_DOWN or char == ord('j') or char == 14:
                menu.move_down()
                menu.paint(self.stdscr)

    @staticmethod
    def __initialize_curses():
        """ Start up the curses UI. """
        stdscr = curses.initscr()

        curses.noecho()
        curses.cbreak()

        stdscr.keypad(True)

        return stdscr

    @staticmethod
    def __terminate_curses(stdscr):
        """
        Shut down the curses UI. We set the console back to a nice condition.
        """
        stdscr.keypad(False)

        curses.nocbreak()
        curses.echo()
        curses.endwin()

def main():
    yselect = MainApplication()
    yselect.run()

if __name__ == "__main__":
    main()
