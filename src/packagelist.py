import curses


class PackageView:

    def __init__(self, window):
        self.window = window
        self.window.attrset(curses.color_pair(1))
        
        (height, width) = self.window.getmaxyx()

        self.list_window = ListView(window.derwin(1, 0))
        self.details_window = DetailsView(window.derwin(height / 2, 0))


    def update(self):
        self.list_window.update()
        self.details_window.update()

        self.window.addstr(0, 0, "yselect - inspection of package states (avail., priority)")
        self.window.refresh()

    def run(self):

        while True:
            self.update()
            char = self.window.getch()

            if char == ord('q'):
                break


class ListView:

    def __init__(self, window):
        self.window = window
        self.window.attrset(curses.color_pair(2))
        padwin = self.window.derwin(1,0)
        self.pad = padwin
        self.pad.attrset(curses.color_pair(0))

    def update(self):
        self.window.addstr(0,0, "EIOM Pri Section\tPackage\tInst.ver\tAvail.ver\tDescription")
        self.pad.addstr(0,3, "--- sublist ---")
        self.window.refresh()

class DetailsView:

    def __init__(self, window):
        self.window = window
        self.window.attrset(curses.color_pair(2))
        (height, width) = self.window.getmaxyx()
        self.details_pad = self.window.derwin(height - 2, 0, 1, 0) 
        self.details_pad.attrset(curses.color_pair(0))

    def update(self):
        (height, width) = self.window.getmaxyx()
        self.window.addnstr(0,0, "bar!   Required" + " " * width, width)
        self.window.addnstr(height - 1, 0, "press d for more." + " " * width, width - 1)
        self.details_pad.addstr(0,0, "DETAILS")


def main(window):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
    packageView = PackageView(window)
    packageView.run()

curses.wrapper(main)
