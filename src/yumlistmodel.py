import yum

import menu
import observable

class ListModel(menu.MenuModel, observable.Observable):

    """ Model of a list of packages. """
    
    def __init__(self):
        menu.MenuModel.__init__(self)
        observable.Observable.__init__(self)

        self.register_signal("selection-changed")
               
        self.title = "All Packages"
        self.name = self.title

        yum_base = yum.YumBase()

        yum_base.doConfigSetup()
        yum_base.doRepoSetup()

        yum_base.repos.populateSack()
        self.packages = []
        for pkg in yum_base.repos.pkgSack.returnPackages():
            self.packages.append(DetailsModel(pkg))

    def add_sub_list(self, sub_list):
        """ Add a sub list to this list. """
        self.packages.append(sub_list)
            
    def move_up(self):
        """ Move the selection up one entry. """
        if (self.selected_entry > 0):
            self.selected_entry = self.selected_entry - 1
        self.emit_signal("selection-changed")
                
    def move_down(self):
        """ Move the selection down one entry. """
        if (self.selected_entry < self.length - 1):
            self.selected_entry = self.selected_entry + 1
        self.emit_signal("selection-changed")
    
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

    def __get_selected(self):
        return DetailsModel(self.packages[self.selected_entry - 1])

    selected = property(__get_selected)


class DetailsModel(object):

    """ A model of package details. """
    
    def __init__(self, pkg):
        self.pkg = pkg

        self.version = "1.2.45"
        self.section = "System/Base"
        self.release = "4"
        self.avail_version = "1.2.45"
        self.avail_release = "5"
        self.priority = "Required"
        self.arch = "i386"
        self.summary = pkg.returnSimple('summary')
        self.description = "Jozzlebaz\nflark! phanf."

        self.installed = True
        self.action = 'INSTALL'

    def __get_eiom(self):
        eiom = " "
        if self.installed:
            eiom = eiom + "*" + "*"
        else:
            eiom = eiom + " " + " "

        if self.action == 'INSTALL':
            eiom = eiom + "*"
        else:
            eiom = eiom + "_"

        return eiom

    eiom = property(__get_eiom)

    def __getattr__(self, x):
        return getattr(self.pkg, x)
