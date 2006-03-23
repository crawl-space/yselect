import curses

__version__ = "0.0.1"
__program_name__ = "yselect"

class MainMenu:
    def __init__(self):
        self.title = \
            "RPM/Yum %s package handling frontend." % (__program_name__)
        
        self.entries = (
            ("update", "[U]pdate", "Update list of available packages, if possible."),
            ("select", "[S]elect", "Request which packages you want on your system."),
            ("install", "[I]nstall", "Install and upgrade wanted packages."),
            ("quit", "[Q]uit", "Quit %s." % (__program_name__))
        )

        self.navigation_info = \
            "Move around with ^P and ^N, cursor keys, initial letters, or digits;\n" + \
            "Press <enter> to confirm selection.  ^L redraws screen."
        self.copyright = \
            "Version %s\n" + \
            "Copyright (C) 2006 Devan Goodwin and James Bowes\n" + \
            "This is free software; see the GNU General Public Licence version 2\n" + \
            "or later for copying conditions.  There is NO warrenty.  See\n" + \
            "%s --licence for details." 
            
        self.copyright = self.copyright % (__version__, __program_name__)
      
        self.selected = "update"
      
    def moveUp(self):
        pass

    def moveDown(self):
        pass

    def select(self):
        pass

    def paint(self, window):
        window.addstr(self.title, curses.A_BOLD)
        
        x_pos = 2
        for i in range(len(self.entries)):
            menu_entry = self.entries[i]

            if self.selected == menu_entry[0]:
                prefix = " * "
                format = curses.A_REVERSE
            else:
                prefix = "   "
                format = curses.A_NORMAL
            
            entry_string = \
                prefix + str(i) + ". " + menu_entry[1] + "\t" + menu_entry[2]
            window.addstr(x_pos, 0, entry_string, format)
            x_pos = x_pos + 1
     
        x_pos = x_pos + 1
        window.addstr(x_pos, 0, self.navigation_info, curses.A_BOLD)
        
        x_pos = x_pos + 3 # The previous string was two lines
        window.addstr(x_pos, 0, self.copyright)

# startup
stdscr = curses.initscr()

curses.noecho()
curses.cbreak()

stdscr.keypad(True)

# end startup
menu = MainMenu()

menu.paint(stdscr)
stdscr.refresh()

while True:
    c = stdscr.getch()

    if c == ord('q'):
        break

# shutdown
stdscr.keypad(False)

curses.nocbreak()
curses.echo()
curses.endwin()
# end shutdown
