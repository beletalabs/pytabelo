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

from PySide2.QtCore import Property, Signal, Qt, QSettings
from PySide2.QtWidgets import QMdiArea, QTabBar, QTabWidget


class MdiArea(QMdiArea):

    def __init__(self, parent=None):
        """  """
        super().__init__(parent=parent)

        self._loadSettings()


    def _loadSettings(self):
        """  """
        settings = QSettings()

        # Document Tabs Visible
        visible = settings.value("DocumentManager/DocumentTabsVisible", True, type=bool)
        self._tabsVisible = visible
        self._setTabBarVisible(visible)

        # Document Tabs Position
        value = settings.value("DocumentManager/DocumentTabsPosition", QTabWidget.North, type=int)
        position = QTabWidget.TabPosition(value) if QTabWidget.TabPosition(value) in [QTabWidget.North, QTabWidget.South] else QTabWidget.North
        self.setTabPosition(position)

        # Document Tabs Auto Hide
        hide = settings.value("DocumentManager/DocumentTabsAutoHide", False, type=bool)
        self._setTabBarAutoHide(hide)


    def saveSettings(self):
        """  """
        settings = QSettings()

        visible = self.getTabsVisible()
        settings.setValue("DocumentManager/DocumentTabsVisible", visible)

        position = self.getTabsPosition()
        settings.setValue("DocumentManager/DocumentTabsPosition", position)

        hide = self.getTabsAutoHide()
        settings.setValue("DocumentManager/DocumentTabsAutoHide", hide)


    #
    # Property helper functions
    #

    def hasTabBar(self):
        """  """
        return self.findChild(QTabBar) is not None


    def _isTabBarVisible(self):
        """  """
        return self.findChild(QTabBar).isVisible() if self.hasTabBar() else False


    def _setTabBarVisible(self, visible):
        """  """
        if self.hasTabBar() and not (self.getCount() <= 1 and self.getTabsAutoHide()):
            self.findChild(QTabBar).setVisible(visible)


    def _setTabBarAutoHide(self, hide):
        """  """
        if self.hasTabBar():
            self.findChild(QTabBar).setAutoHide(hide)


    #
    # Property: tabsVisible
    #

    def getTabsVisible(self):
        """  """
        return self._tabsVisible


    def setTabsVisible(self, visible):
        """  """
        if self.hasTabBar() and visible != self.getTabsVisible:
            self._tabsVisible = visible
            self._setTabBarVisible(visible)
            self.tabsVisibleChanged.emit(visible)


    def initTabsVisible(self):
        """  """
        if self.hasTabBar():
            visible = True
            self._tabsVisible = visible
            self._setTabBarVisible(visible)
            self.tabsVisibleChanged.emit(visible)


    tabsVisibleChanged = Signal(bool)
    tabsVisible = Property(bool, getTabsVisible, setTabsVisible, notify=tabsVisibleChanged)


    #
    # Property: tabsPosition
    #

    def getTabsPosition(self):
        """  """
        return self.tabPosition()


    def setTabsPosition(self, position):
        """  """
        if position != self.getTabsPosition():
            self.setTabPosition(position)
            self.tabsPositionChanged.emit(position)


    def initTabsPosition(self):
        """  """
        position = QTabWidget.North
        self.setTabPosition(position)
        self.tabsPositionChanged.emit(position)


    tabsPositionChanged = Signal(QTabWidget.TabPosition)
    tabsPosition = Property(QTabWidget.TabPosition, getTabsPosition, setTabsPosition, notify=tabsPositionChanged)


    #
    # Property: tabsAutoHide
    #

    def getTabsAutoHide(self):
        """  """
        return self.findChild(QTabBar).autoHide() if self.hasTabBar() else False


    def setTabsAutoHide(self, hide):
        """  """
        if self.hasTabBar() and hide != self.getTabsAutoHide():
            self._setTabBarAutoHide(hide)
            self.tabsAutoHideChanged.emit(hide)


    def initTabsAutoHide(self):
        """  """
        if self.hasTabBar():
            hide = False
            self._setTabBarAutoHide(hide)
            self.tabsAutoHideChanged.emit(hide)


    tabsAutoHideChanged = Signal(bool)
    tabsAutoHide = Property(bool, getTabsAutoHide, setTabsAutoHide, notify=tabsAutoHideChanged)


    #
    # Property: count
    #

    def getCount(self):
        """  """
        return len(self.subWindowList())


    count = Property(int, getCount)


    #
    #
    #

    def subWindowCount(self):
        """  """
        return len(self.subWindowList())


    def findSubWindow(self, url):
        """  """
        if url.isEmpty():
            return None

        for subWindow in self.subWindowList():
            if subWindow.widget().getUrl() == url:
                return subWindow

        return None


    def closeSelectedSubWindow(self, subWindow):
        """  """
        if subWindow is None:
            return None

        subWindow.close()


    def closeOtherSubWindows(self, subWindow):
        """  """
        subWindows = self.subWindowList()
        if subWindow not in subWindows:
            return None

        # First remove the subwindow from the list that should not be closed
        subWindows.remove(subWindow)

        # Then close all other subwindows
        for subWindow in subWindows:
            self.closeSelectedSubWindow(subWindow)
