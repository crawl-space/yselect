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

import menu
import mainmenu
import packagelist

__revision__ = "$Rev$"

program_name = "yselect"
program_version = "0.0.1"

class MainApplication:

    """
    Application driver class.
    """

    def __init__(self, screen):
        self.screen = screen
        self.do_quit = False

    def run(self):
        """
		The main event loop for the application.
		"""

		# Start out with the main menu:
        menu_model = mainmenu.MainMenuModel(program_name)
        menu_model.add_observer("quit", self)
        menu_model.add_observer("select", self)
        
        menu_view = mainmenu.MainMenuView(self.screen, menu_model, program_name,
            program_version)
        menu_controller = mainmenu.MainMenuController(menu_model)
       
        self.view = menu_view
        self.controller = menu_controller

        while not self.do_quit:
            self.view.paint()
            
            char = self.screen.getch()
            self.controller.handle_input(char)

    def notify(self, observable, signal_name):
        """ Respond to changes from user input. """
        if signal_name == "quit":
            self.do_quit = True
        elif signal_name == "select":
            self.screen.clear()
       
            list_model = packagelist.ListModel()
            list_model.add_sub_list(packagelist.ListModel())
           
            list_controller = packagelist.ListController(list_model)
            package_controller = packagelist.PackageController(list_controller)
           
            self.view = packagelist.PackageView(self.screen, list_model)
            self.controller = package_controller
        else:
            assert False, \
                "Recieved a notification for a signal we didn't know about."


def main(screen):
    """ Main yselect function. """
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)

    yselect = MainApplication(screen)
    yselect.run()

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        # We don't want to complain on ctrl-c
        pass
