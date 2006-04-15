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
Fake Repository object.

Copyright (C) 2006 James Bowes <jbowes@redhat.com>
"""

__revision__ = "$Rev$"

class Repository:

    """
    Fake Repository object.
    """

    def __init__(self):
        pass

    def getPackage(self):
        """
        Pretend to download a package.

        Return the location of the downloaded package.
        """
        pass

    def getHeader(self):
        """
        Pretend to download a package header.

        Return the location of the downloaded header.
        """
        pass

    def getPackageSack(self):
        """ Return the PackageSack for this Repository. """
        pass
