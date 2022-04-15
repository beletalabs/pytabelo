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

from PySide2.QtCore import Property, Signal, Qt
from PySide2.QtWidgets import QMdiArea, QTabBar


class MdiArea(QMdiArea):

    tabBarVisibleChanged = Signal(bool)


    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setAttribute(Qt.WA_DeleteOnClose)

        self._tabBarVisible = True


    def hasTabBar(self):

        return self.findChild(QTabBar) is not None


    def isTabBarVisible(self):

        if self.hasTabBar():
            return self.findChild(QTabBar).isVisible()

        return True


    def getTabBarVisible(self):

        return self._tabBarVisible


    def setTabBarVisible(self, visible):

        if self.hasTabBar() and visible != self._tabBarVisible:
            self._tabBarVisible = visible
            self.tabBarVisibleChanged.emit(visible)

            if self.subWindowCount() == 1 and not self.isTabBarAutoHide():
                self.findChild(QTabBar).setVisible(visible)
            if self.subWindowCount() >= 2:
                self.findChild(QTabBar).setVisible(visible)


    tabBarVisible = Property(bool, getTabBarVisible, setTabBarVisible, notify=tabBarVisibleChanged)


    def initTabBarVisible(self):

        self._tabBarVisible = True
        self.tabBarVisibleChanged.emit(self._tabBarVisible)

        if self.subWindowCount() == 1 and not self.isTabBarAutoHide():
            self.findChild(QTabBar).setVisible(visible)
        if self.subWindowCount() >= 2:
            self.findChild(QTabBar).setVisible(visible)


    def isTabBarAutoHide(self):

        tabBar = self.findChild(QTabBar)
        if tabBar is not None:
            return tabBar.autoHide()

        return False


    def setTabBarAutoHide(self, hide):

        tabBar = self.findChild(QTabBar)
        if tabBar is not None:
            tabBar.setAutoHide(hide)


    def subWindowCount(self):

        return len(self.subWindowList())


    def findSubWindow(self, url):

        if url.isEmpty():
            return None

        subWindows = self.subWindowList()
        for subWindow in subWindows:

            document = subWindow.widget()
            if document.getUrl() == url:
                return subWindow

        return None


    def closeSelectedSubWindow(self, subWindow):

        if subWindow is None:
            return None

        subWindow.close()


    def closeOtherSubWindows(self, subWindow):

        subWindows = self.subWindowList()
        if subWindow not in subWindows:
            return None

        # First remove the subwindow from the list that should not be closed
        subWindows.remove(subWindow)

        # Then close all other subwindows
        for subWindow in subWindows:
            self.closeSelectedSubWindow(subWindow)
