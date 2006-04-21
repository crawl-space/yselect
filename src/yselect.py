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

"""
Yselect program.
"""

import curses.wrapper

import mainmenu

__revision__ = "$Rev$"

program_name = "yselect"
program_version = "0.0.1"

class MainApplication:

    """
    Application driver class.
    """

    def __init__(self):
        self.do_quit = False

    def run(self, screen):
        """
		The main event loop for the application.
		"""

		# Start out with the main menu:
        currentMenu = mainmenu.MainMenu(screen, program_name, program_version)

        currentMenu.model.add_observer("quit", self)

        while not self.do_quit:
            currentMenu.paint()
            
            char = screen.getch()
            currentMenu.handle_input(char)

    def notify(self, observable, signal_name):
        if signal_name == "quit":
            self.do_quit = True
        else:
            assert False, \
                "Recieved a notification for a signal we didn't know about."


def main(screen):
    yselect = MainApplication()
    yselect.run(screen)

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        # We don't want to complain on ctrl-c
        pass
