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
        yum_base.closeRpmDB()
        yum_base.doTsSetup()
        yum_base.doRpmDBSetup()
        yum_base.doRepoSetup()
        yum_base.doSackSetup()

        yum_base.repos.populateSack()
        self.packages = []
 
        for po in yum_base.pkgSack.returnNewestByNameArch():
            if self.simpleDBInstalled(yum_base, po.returnSimple('name')):
                continue
            self.packages.append(DetailsModel(po, False))
        for po in yum_base.rpmdb.returnPackages():
            self.packages.append(DetailsModel(po, True))

    def simpleDBInstalled(self, yum_base, name):
        # From pirut.
        # FIXME: doing this directly instead of using self.rpmdb.installed()
        # speeds things up by 400%
        mi = yum_base.ts.ts.dbMatch('name', name)
        if mi.count() > 0:
            return True
        return False

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
        return self.packages[self.selected_entry - 1]

    selected = property(__get_selected)


class DetailsModel(object):

    """ A model of package details. """
    
    def __init__(self, pkg, installed):
        self.pkg = pkg

        self.name = pkg.name

        self.avail_version = pkg.version
        self.avail_release = pkg.release

        self.section = pkg.returnSimple("group")
        self.priority = "Required"
        self.arch = pkg.arch
        self.summary = pkg.returnSimple('summary')
        self.description = pkg.returnSimple('description')

        self.installed = installed
        if self.installed:
            self.version = pkg.version
            self.release = pkg.release
            self.action = 'INSTALL'
        else:
            self.version = '<none>'
            self.release = None
            self.action = 'REMOVE'

    def __get_eiom(self):
        eiom = " "
        if self.installed:
            eiom = eiom + "*" + "*"
        else:
            eiom = eiom + " " + "_"

        if self.action == 'INSTALL':
            eiom = eiom + "*"
        else:
            eiom = eiom + "_"

        return eiom

    eiom = property(__get_eiom)
