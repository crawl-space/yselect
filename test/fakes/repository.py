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
