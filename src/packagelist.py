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

        details_height = (height - 1) / 2

        self.list_window = ListView(window.derwin(height - details_height,
            width, 1, 0), list_model)
        self.details_window = DetailsView(window.derwin(details_height, width,
            height - details_height, 0))
        self.details_window.model = DetailsModel()

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
        (height, width) = self.window.getmaxyx()
        
        self.pad = self.window.derwin(height - 1, width, 1, 0)
        self.pad.bkgd(" ", curses.color_pair(0))

        self.list_model = list_model
        self.selectedEntry = 3

        (y, x) = self.pad.getmaxyx()

        self.scroll_top = 0
        self.scroll_bottom = y - 2

        self.EIOM_col_start = 0
        self.priority_col_start = 5
        self.section_col_start = 9
        self.package_col_start = 18
        self.installed_col_start = 31
        self.available_col_start = 43
        self.description_col_start = 55
        
        self.EIOM_col_width = 4
        self.priority_col_width = 3
        self.section_col_width = 8
        self.package_col_width = 12
        self.installed_col_width = 11
        self.available_col_width = 11

        self.description_col_width = x - self.description_col_start

    def paint(self):
        (height, width) = self.window.getmaxyx()
        self.window.addstr(0,0, "EIOM Pri Section  Package      Inst.ver    Avail.ver   Description")
        self.__add_list(self.list_model, 0, 1)
        self.pad.refresh()
            
    def __get_attribute(self, row):
        if (row == self.selectedEntry):
            attribute = curses.A_REVERSE
        else:
            attribute = curses.A_NORMAL
        return attribute

    def __add_list(self, list_model, row, depth):
        # FIXME: Too much duplicated code and nastiness
        # Could use a generator here to provide items in the list.
        if (row >= self.scroll_top and row <= self.scroll_bottom):
            attribute = self.__get_attribute(row)
            self.__add_menu_title(row - self.scroll_top, 5, list_model.title,
                depth, attribute)
        for i in range(len(list_model.packages)):
            entry = list_model.packages[i]
            draw_row = i + row + 1
            if entry.__class__ == ListModel:
                self.__add_list(entry, draw_row, depth + 1)
            else:
                if (draw_row >= self.scroll_top and draw_row <= self.scroll_bottom):
                    self.__add_menu_package(draw_row, entry)

    def __add_menu_title(self, y, x, title, depth, attribute):
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

    def __add_menu_package(self, cur_y, package):
        """ Draw a package line in the menu. """
        (max_y, max_x) = self.pad.getmaxyx()
        format_string = self.__make_package_format_string() 
        pkg_string = format_string % \
            ("", "", package.section, package.name, package.version,
            package.avail_version, package.summary)
        attribute = self.__get_attribute(cur_y)
        self.pad.addstr(cur_y - self.scroll_top, 0, pkg_string, attribute)
       
    def __make_package_format_string(self):
        # Fill in the correct amounts to pad each column on the right with.
        format_string = "%%-%d.%ds %%-%d.%ds %%-%d.%ds %%-%d.%ds %%-%d.%ds " \
            "%%-%d.%ds %%-%d.%ds" % \
            (self.EIOM_col_width, self.EIOM_col_width,
            self.priority_col_width, self.priority_col_width, 
            self.section_col_width, self.section_col_width,
            self.package_col_width, self.package_col_width,
            self.installed_col_width, self.installed_col_width,
            self.available_col_width, self.available_col_width, 
            self.description_col_width, self.description_col_width)
        return format_string
            
    def move_up(self):
        if (self.selectedEntry > 0):
            self.selectedEntry = self.selectedEntry - 1

            if (self.selectedEntry < self.scroll_top):
                self.scroll_top = self.scroll_top - 1
                self.scroll_bottom = self.scroll_bottom - 1
                
    def move_down(self):
        if (self.selectedEntry < self.list_model.length - 1):
            self.selectedEntry = self.selectedEntry + 1

            if (self.selectedEntry > self.scroll_bottom):
                self.scroll_top = self.scroll_top + 1
                self.scroll_bottom = self.scroll_bottom + 1


class ListModel:

    def __init__(self):
        self.title = "All Packages"
        self.packages = [DetailsModel(), DetailsModel()]

    def addSubList(self, sub_list):
        self.packages.append(sub_list)

    def __getLength(self):
        """ Return the length of the list including sublists. """
        length = 1 # Include the title.
        for entry in self.packages:
            if entry.__class__ == ListModel:
                length = length + entry.__getLength()
            else:
                length = length + 1
        return length

    length = property(__getLength)
                
class DetailsView:

    def __init__(self, window):
        self.window = window
        self.window.bkgd(" ", curses.color_pair(2))
        (height, width) = self.window.getmaxyx()
        self.details_pad = self.window.derwin(height - 2, 0, 1, 0) 
        self.details_pad.bkgd(" ", curses.color_pair(0))

        self.model = None

    def paint(self):
        (height, width) = self.window.getmaxyx()
               
        if self.model:
            self.window.addstr(0,0, self.model.name)
            # TODO: Only show this when there is more to display
            self.window.addstr(height - 1, 0, "press d for more.")
            self.paint_summary(height, width)

    def paint_summary(self, height, width):
        self.details_pad.addstr(0, 0, "%s - %s" % (self.model.name,
            self.model.summary), curses.A_BOLD)
        self.details_pad.addstr(2, 0, self.model.description)

    def paint_full(self, height, width):
        self.details_pad.addstr(0,0, "Name: %s" % self.model.name)
        self.details_pad.addstr(1,0,
            "Version: %s" % self.model.version)
        self.details_pad.addstr(2,0,
            "Release: %s" % self.model.release)
        self.details_pad.addstr(3,0,
            "Architecture: %s" % self.model.arch)
        self.details_pad.addstr(4,0,
            "Details: %s" % self.model.description)


class DetailsModel:

    def __init__(self):
        self.name = "fizzle"
        self.version = "1.2.45"
        self.section = "System/Base"
        self.release = "4"
        self.avail_version = "1.2.45"
        self.avail_release = "5"
        self.arch = "i386"
        self.summary = "the jozzlebazzer phanf."
        self.description = "Jozzlebaz\nflark! phanf."


def main(window):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
    packageView = PackageView(window)
    packageView.run()

curses.wrapper(main)
