# This Python file uses the following encoding: utf-8
#
# Copyright 2022 naracanto <https://naracanto.github.io>.
#
# This file is part of PyTabelo <https://github.com/cutelabs/pytabelo>.
#
# PyTabelo is an open source table editor written in Python using
# the Python bindings for the Qt framework.
#
# PyTabelo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# PyTabelo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyTabelo.  If not, see <https://www.gnu.org/licenses/>.
#

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMdiArea, QTabBar


class MdiArea(QMdiArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setAttribute(Qt.WA_DeleteOnClose)


    def isTabBarAutoHide(self):

        tabBar = self.findChild(QTabBar)
        if tabBar:
            return tabBar.autoHide()

        return False


    def setTabBarAutoHide(self, hide):

        tabBar = self.findChild(QTabBar)
        if tabBar:
            tabBar.setAutoHide(hide)


    def isTabBarVisible(self):

        tabBar = self.findChild(QTabBar)
        if tabBar:
            return tabBar.isVisible()

        return False


    def setTabBarVisible(self, visible):

        tabBar = self.findChild(QTabBar)
        if tabBar:
            tabBar.setVisible(visible)


    def closeSelectedSubWindow(self, subWindow):

        if subWindow is None:
            return

        subWindow.close()


    def closeOtherSubWindows(self, subWindow):

        subWindows = self.subWindowList()
        if not len(subWindows) or subWindow is None:
            return

        # First remove the subwindow from the list that should not be closed
        if subWindow in subWindows:
            subWindows.remove(subWindow)
        else:
            return

        # Then close all other subwindows
        for subWindow in subWindows:
            self.closeSelectedSubWindow(subWindow)
