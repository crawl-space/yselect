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
Base class implementing observer pattern.
"""

class Observable:

    def __init__(self):
        self.signals = {}

    def register_signal(self, signal_name):
        if not self.signals.has_key(signal_name):
            self.signals[signal_name] = []

    def add_observer(self, signal_name, observer):
        if not self.signals.has_key(signal_name):
            raise NoSuchSignalException
        signal_observers = self.signals[signal_name]
        if signal_observers.count(observer) == 0:
            self.signals[signal_name].append(observer)

    def emit_signal(self, signal_name):
        observers = self.signals[signal_name]
        for observer in observers:
            observer.notify(self)

class NoSuchSignalException(Exception):
    pass
