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

""" List of packages display. """

import curses

import menu

__revision__ = "$Rev$"

class PackageView:

    """ Window for displaying the package list and details. """
    
    def __init__(self, window):
        self.window = window
        self.window.bkgd(" ", curses.color_pair(1))
        
        (height, width) = self.window.getmaxyx()

        list_model = ListModel()
        list_model.add_sub_list(ListModel())

        details_height = (height - 1) / 2

        self.list_view = ListView(window.derwin(height - details_height,
            width, 1, 0), list_model)
        list_controller = menu.MenuController(list_model)

        # TODO: Figure out a way to make the view ignorant of the controller
        self.package_controller = PackageController(list_controller)
        self.details_view = DetailsView(window.derwin(details_height, width,
            height - details_height, 0))
        self.details_view.model = DetailsModel()

    def paint(self):
        """ Draw the package view onscreen. """
        self.list_view.paint()
        self.details_view.paint()

        self.window.addstr(0, 0, 
            "yselect - inspection of package states (avail., priority)")


class PackageController:

    """ Controller for package selection. """

    def __init__(self, list_controller):
        self._list_controller = list_controller

    def handle_input(self, key):
        """
        Respond to key presses.

        The list controller handles input first.
        """

        if key == ord('x'):
            import sys
            sys.exit(0)
            return True
        else:
            return self._list_controller.handle_input(key)


class ListView(menu.MenuView):

    """ Displays a list of packages. """
    
    def __init__(self, window, list_model):
        menu.MenuView.__init__(self, list_model)
        
        self.window = window
        self.window.bkgd(" ", curses.color_pair(2))
        (height, width) = self.window.getmaxyx()
        
        self.pad = self.window.derwin(height - 1, width, 1, 0)
        self.pad.bkgd(" ", curses.color_pair(0))

        (height, width) = self.pad.getmaxyx()

        self.scroll_top = 0
        self.scroll_bottom = height - 2

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

        self.description_col_width = width - self.description_col_start

    def paint(self):
        """ Draw the list on screen. """
        self.window.addstr(0, 0, "EIOM Pri Section  Package      " + \
                "Inst.ver    Avail.ver   Description")
        self.__adjust_scroll_window()
        self.__paint_list(self._model, 0, 1)
        self.pad.refresh()
            
    def __get_attribute(self, row):
        """
        Determine if row is the selected_entry or not.

        Return the appropriate curses attribute.
        """
        if (row == self._model.selected_entry):
            attribute = curses.A_REVERSE
        else:
            attribute = curses.A_NORMAL
        return attribute

    def __paint_list(self, list_model, row, depth):
        """ Draw a list on the screen. """
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
                self.__paint_list(entry, draw_row, depth + 1)
            else:
                if (draw_row >= self.scroll_top and
                    draw_row <= self.scroll_bottom):
                    self.__add_menu_package(draw_row, entry)

    def __add_menu_title(self, cur_y, cur_x, title, depth, attribute):
        """
        Draw a menu title on the screen.

        Starting at position x,y draw a menu title. depth indicates how many
        parents the menu has. Title is rendered in bold.
        """
        line_length = depth * 2 - 1
       
        self.pad.addstr(cur_y, 0, cur_x * " ", attribute) 
        self.pad.hline(cur_y, cur_x, curses.ACS_HLINE, line_length, attribute)
        self.pad.addstr(cur_y, cur_x + line_length, " %s " % title,
            curses.A_BOLD and attribute)
        self.pad.hline(cur_y, cur_x + line_length + 2 + len(title),
            curses.ACS_HLINE, line_length, attribute)
        
        (max_y, max_x) = self.pad.getmaxyx()
        line_end = max_x - (cur_x + 2 * line_length + 2 + len(title))
        self.pad.addstr(cur_y, cur_x + 2 * line_length + 2 + len(title),
            line_end * " ", attribute)

    def __add_menu_package(self, cur_y, package):
        """ Draw a package line in the menu. """
        format_string = self.__make_package_format_string() 
        pkg_string = format_string % \
            (package.eiom, package.priority, package.section, package.name,
            package.version, package.avail_version, package.summary)
        attribute = self.__get_attribute(cur_y)
        self.pad.addstr(cur_y - self.scroll_top, 0, pkg_string, attribute)
       
    def __make_package_format_string(self):
        """
        Fill in the correct amounts to pad each column on the right with.
        """
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

    def __adjust_scroll_window(self):
        """ 
        Move the scrolling list window.
        
        We only adjust if the model's selected entry is at the bottom or the
        top of the scroll window.
        """
        if (self._model.selected_entry < self.scroll_top):
            self.scroll_top = self.scroll_top - 1
            self.scroll_bottom = self.scroll_bottom - 1

        if (self._model.selected_entry > self.scroll_bottom):
            self.scroll_top = self.scroll_top + 1
            self.scroll_bottom = self.scroll_bottom + 1


class ListModel(menu.MenuModel):

    """ Model of a list of packages. """
    
    def __init__(self):
        menu.MenuModel.__init__(self)

        self.title = "All Packages"
        self.packages = [DetailsModel(), DetailsModel()]

    def add_sub_list(self, sub_list):
        """ Add a sub list to this list. """
        self.packages.append(sub_list)
            
    def move_up(self):
        """ Move the selection up one entry. """
        if (self.selected_entry > 0):
            self.selected_entry = self.selected_entry - 1
                
    def move_down(self):
        """ Move the selection down one entry. """
        if (self.selected_entry < self.length - 1):
            self.selected_entry = self.selected_entry + 1

    def __get_length(self):
        """ Return the length of the list including sublists. """
        length = 1 # Include the title.
        for entry in self.packages:
            if entry.__class__ == ListModel:
                length = length + entry.__get_length()
            else:
                length = length + 1
        return length

    length = property(__get_length)
                
class DetailsView:

    """ Class for displaying package details. """
    
    def __init__(self, window):
        self.window = window
        self.window.bkgd(" ", curses.color_pair(2))
        (height, width) = self.window.getmaxyx()
        self.details_pad = self.window.derwin(height - 2, 0, 1, 0) 
        self.details_pad.bkgd(" ", curses.color_pair(0))

        self.model = None

    def paint(self):
        """ Draw the DetailsView on screen. """
        (height, width) = self.window.getmaxyx()
               
        if self.model:
            self.window.addstr(0, 0, self.model.name)
            # TODO: Only show this when there is more to display
            self.window.addstr(height - 1, 0, "press d for more.")
            self.paint_summary()

    def paint_summary(self):
        """ Draw the package details summary line. """
        self.details_pad.addstr(0, 0, "%s - %s" % (self.model.name,
            self.model.summary), curses.A_BOLD)
        self.details_pad.addstr(2, 0, self.model.description)

    def paint_full(self):
        """ Draw the package's full details. """
        self.details_pad.addstr(0, 0, "Name: %s" % self.model.name)
        self.details_pad.addstr(1, 0,
            "Version: %s" % self.model.version)
        self.details_pad.addstr(2, 0,
            "Release: %s" % self.model.release)
        self.details_pad.addstr(3, 0,
            "Architecture: %s" % self.model.arch)
        self.details_pad.addstr(4, 0,
            "Details: %s" % self.model.description)


class DetailsModel:

    """ A model of package details. """
    
    def __init__(self):
        self.name = "fizzle"
        self.version = "1.2.45"
        self.section = "System/Base"
        self.release = "4"
        self.avail_version = "1.2.45"
        self.avail_release = "5"
        self.eiom = "  _*"
        self.priority = "Required"
        self.arch = "i386"
        self.summary = "the jozzlebazzer phanf."
        self.description = "Jozzlebaz\nflark! phanf."
