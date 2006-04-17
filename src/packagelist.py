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

import menu

__revision__ = "$Rev$"

class PackageView:

    def __init__(self, window):
        self.window = window
        self.window.bkgd(" ", curses.color_pair(1))
        
        (height, width) = self.window.getmaxyx()

        list_model = ListModel()
        list_model.addSubList(ListModel())

        self.list_window = ListView(window.derwin(1, 0), list_model)
        self.details_window = DetailsView(window.derwin(height / 2, 0))
        self.details_window.setModel(DetailsModel())


    def paint(self):
        self.list_window.paint()
        self.details_window.paint()

        (height, width) = self.window.getmaxyx()

        self.window.addstr(0, 0, "yselect - inspection of package states (avail., priority)")

    def run(self):

        while True:
            self.paint()
            char = self.window.getch()

            if char == ord('q'):
                break
            
            self.list_window.handle_input(char)

class ListView(menu.Menu):

    def __init__(self, window, list_model):
        menu.Menu.__init__(self)
        
        self.window = window
        self.window.bkgd(" ", curses.color_pair(2))
        padwin = self.window.derwin(1,0)
        self.pad = padwin
        self.pad.bkgd(" ", curses.color_pair(0))

        self.list_model = list_model
        self.selectedEntry = 3

    def paint(self):
        (height, width) = self.window.getmaxyx()
        self.window.addstr(0,0, "EIOM Pri Section\tPackage\tInst.ver\tAvail.ver\tDescription")
        self.add_list(self.list_model, 0, 1)
        self.pad.refresh()
            
    def get_attribute(self, row):
        if (row == self.selectedEntry):
            attribute = curses.A_REVERSE
        else:
            attribute = curses.A_NORMAL
        return attribute

    def add_list(self, list_model, row, depth):
        # FIXME: Too much duplicated code and nastiness
        attribute = self.get_attribute(row)
        self.add_menu_title(row, 5, list_model.title, depth, attribute)
        for i in range(len(list_model.packages)):
            entry = list_model.packages[i]
            if entry.__class__ == ListModel:
                self.add_list(entry, i + row + 1, 2)
            else:
                (y, x) = self.pad.getmaxyx()
                format_string = "%%-%ds" % x 
                pkg_string = format_string % list_model.packages[i]
                attribute = self.get_attribute(i + row + 1)
                self.pad.addstr(i + row + 1, 0, pkg_string,
                    attribute)

    def add_menu_title(self, y, x, title, depth, attribute):
        """
        Draw a menu title on the screen.

        Starting at position x,y draw a menu title. depth indicates how many
        parents the menu has. Title is rendered in bold.
        """
        line_length = depth * 2 - 1
       
        self.pad.addstr(y, 0, x * " ", attribute) 
        self.pad.hline(y, x, curses.ACS_HLINE, line_length, attribute)
        self.pad.addstr(y, x + line_length, " %s " % title, curses.A_BOLD
            and attribute)
        self.pad.hline(y, x + line_length + 2 + len(title), curses.ACS_HLINE,
            line_length, attribute)
        
        (max_y, max_x) = self.pad.getmaxyx()
        line_end = max_x - (x + 2 * line_length + 2 + len(title))
        self.pad.addstr(y, x + 2 * line_length + 2 + len(title), line_end * " ",
            attribute)

    def move_up(self):
        if (self.selectedEntry > 0):
            self.selectedEntry = self.selectedEntry - 1

    def move_down(self):
        if (self.selectedEntry < self.list_model.getLength() - 1):
            self.selectedEntry = self.selectedEntry + 1


class ListModel:

    def __init__(self):
        self.title = "All Packages"
        self.packages = ['pkg1', 'pkg2', 'pkgz', 'pkg5']

    def addSubList(self, sub_list):
        self.packages.append(sub_list)

    def getLength(self):
        """ Return the length of the list including sublists. """
        length = 1 # Include the title.
        for entry in self.packages:
            if entry.__class__ == ListModel:
                length = length + entry.getLength()
            else:
                length = length + 1
        return length

                
class DetailsView:

    def __init__(self, window):
        self.window = window
        self.window.bkgd(" ", curses.color_pair(2))
        (height, width) = self.window.getmaxyx()
        self.details_pad = self.window.derwin(height - 2, 0, 1, 0) 
        self.details_pad.bkgd(" ", curses.color_pair(0))

        self.details_model = None

    def paint(self):
        (height, width) = self.window.getmaxyx()
               
        if self.details_model:
            self.window.addstr(0,0, self.details_model.name)
            # TODO: Only show this when there is more to display
            self.window.addstr(height - 1, 0, "press d for more.")
            self.paint_summary(height, width)

    def paint_summary(self, height, width):
        self.details_pad.addstr(0, 0, "%s - %s" % (self.details_model.name,
            self.details_model.summary), curses.A_BOLD)
        self.details_pad.addstr(2, 0, self.details_model.description)

    def paint_full(self, height, width):
        self.details_pad.addstr(0,0, "Name: %s" % self.details_model.name)
        self.details_pad.addstr(1,0,
            "Version: %s" % self.details_model.version)
        self.details_pad.addstr(2,0,
            "Release: %s" % self.details_model.release)
        self.details_pad.addstr(3,0,
            "Architecture: %s" % self.details_model.arch)
        self.details_pad.addstr(4,0,
            "Details: %s" % self.details_model.description)
       
    def setModel(self, details_model):
        self.details_model = details_model


class DetailsModel:

    def __init__(self):
        self.name = "fizzle"
        self.version = "1.2.45"
        self.release = "4"
        self.arch = "i386"
        self.summary = "the jozzlebazzer phanf."
        self.description = "Jozzlebaz\nflark! phanf."


def main(window):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
    packageView = PackageView(window)
    packageView.run()

curses.wrapper(main)
