import curses


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


    def update(self):
        self.list_window.update()
        self.details_window.update()

        (height, width) = self.window.getmaxyx()

        self.window.addstr(0, 0, "yselect - inspection of package states (avail., priority)")
        self.window.refresh()

    def run(self):

        while True:
            self.update()
            char = self.window.getch()

            if char == ord('q'):
                break


class ListView:

    def __init__(self, window, list_model):
        self.window = window
        self.window.bkgd(" ", curses.color_pair(2))
        padwin = self.window.derwin(1,0)
        self.pad = padwin
        self.pad.bkgd(" ", curses.color_pair(0))

        self.list_model = list_model

    def update(self):
        (height, width) = self.window.getmaxyx()
        self.window.addstr(0,0, "EIOM Pri Section\tPackage\tInst.ver\tAvail.ver\tDescription")
        self.add_list(self.list_model, 0, 1)
        self.window.refresh()

    def add_list(self, list_model, row, depth):
        self.add_menu_title(row, 5, list_model.title, depth)
        for i in range(len(list_model.packages)):
            entry = list_model.packages[i]
            if entry.__class__ == ListModel:
                self.add_list(entry, i + row + 1, 2)
            else:
                self.pad.addstr(i + row + 1, 0, list_model.packages[i])

    def add_menu_title(self, y, x, title, depth):
        """
        Draw a menu title on the screen.

        Starting at position x,y draw a menu title. depth indicates how many
        parents the menu has. Title is rendered in bold.
        """
        line_length = depth * 2 - 1
        
        self.pad.hline(y, x, curses.ACS_HLINE, line_length)
        self.pad.addstr(y, x + line_length + 1 , title, curses.A_BOLD)
        self.pad.hline(y, x + line_length + 2 + len(title), curses.ACS_HLINE,
            line_length)


class ListModel:

    def __init__(self):
        self.title = "All Packages"
        self.packages = ['pkg1', 'pkg2', 'pkgz', 'pkg5']

    def addSubList(self, sub_list):
        self.packages.append(sub_list)


class DetailsView:

    def __init__(self, window):
        self.window = window
        self.window.bkgd(" ", curses.color_pair(2))
        (height, width) = self.window.getmaxyx()
        self.details_pad = self.window.derwin(height - 2, 0, 1, 0) 
        self.details_pad.bkgd(" ", curses.color_pair(0))

        self.details_model = None

    def update(self):
        (height, width) = self.window.getmaxyx()
               
        if self.details_model:
            self.window.addstr(0,0, self.details_model.name)
            # TODO: Only show this when there is more to display
            self.window.addstr(height - 1, 0, "press d for more.")
            self.update_summary(height, width)

    def update_summary(self, height, width):
        self.details_pad.addstr(0, 0, "%s - %s" % (self.details_model.name,
            self.details_model.summary), curses.A_BOLD)
        self.details_pad.addstr(2, 0, self.details_model.description)

    def update_full(self, height, width):
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
