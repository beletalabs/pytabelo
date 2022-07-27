# This Python file uses the following encoding: utf-8
#
# Copyright 2022 naracanto <https://naracanto.github.io>.
#
# This file is part of PyTabelo <https://github.com/beletalabs/pytabelo>.
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
from PySide2.QtWidgets import QTabWidget, QVBoxLayout, QWidget


class TableDocument(QWidget):

    def __init__(self, parent=None):
        """  """
        super().__init__(parent=parent)

        self._tabBarVisible = True

        self._tabBox = QTabWidget()
        self._tabBox.setDocumentMode(True)
        self._tabBox.setMovable(True)
#        self._tabBox.setTabsClosable(True)
        self._tabBox.tabCloseRequested.connect(self._slotCloseTab)

        self._loadSettings()

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self._tabBox)
        self.setLayout(mainLayout)


    def _loadSettings(self):
        """  """
        settings = QSettings()

        # Sheet Tab Bar Visible
        visible = settings.value("Document/SheetTabBarVisible", True, type=bool)
        self._tabBarVisible = visible
        self._setTabBarVisible(visible)

        # Sheet Tab Bar Position
        value = settings.value("Document/SheetTabBarPosition", QTabWidget.South, type=int)
        values = (int(QTabWidget.North), int(QTabWidget.South))
        position = QTabWidget.TabPosition(value) if value in values else QTabWidget.South
        self._tabBox.setTabPosition(position)

        # Sheet Tabs Auto Hide
        hide = settings.value("Document/SheetTabsAutoHide", True, type=bool)
        self._tabBox.setTabBarAutoHide(hide)


    def saveSettings(self):
        """  """
        settings = QSettings()

        # Sheet Tab Bar Visible
        visible = self._tabBarVisible
        settings.setValue("Document/SheetTabBarVisible", visible)


    #
    # Property: tabBarVisible
    #

    def isTabBarVisible(self):
        """  """
        return self._tabBarVisible


    def setTabBarVisible(self, visible):
        """  """
        if visible != self._tabBarVisible:
            self._tabBarVisible = visible
            self._setTabBarVisible(self._tabBarVisible)
            self.tabBarVisibleChanged.emit(self._tabBarVisible)


    def resetTabBarVisible(self):
        """  """
        self._tabBarVisible = True
        self._setTabBarVisible(self._tabBarVisible)
        self.tabBarVisibleChanged.emit(self._tabBarVisible)


    def initTabBarVisible(self):
        """  """
        self._setTabBarVisible(self._tabBarVisible)
        self.tabBarVisibleChanged.emit(self._tabBarVisible)


    tabBarVisibleChanged = Signal(bool)
    tabBarVisible = Property(bool, isTabBarVisible, setTabBarVisible, notify=tabBarVisibleChanged)


    def _setTabBarVisible(self, visible):
        """  """
        if not (self._tabBox.count() <= 1 and self._tabBox.tabBarAutoHide()):
            self._tabBox.tabBar().setVisible(visible)


    #
    # Property: tabBarPosition
    #

    def getTabBarPosition(self):
        """  """
        return self._tabBox.tabPosition()


    def setTabBarPosition(self, position):
        """  """
        if position != self.getTabBarPosition():
            self._tabBox.setTabPosition(position)
            self.tabBarPositionChanged.emit(self.getTabBarPosition())


    def resetTabBarPosition(self):
        """  """
        self._tabBox.setTabPosition(QTabWidget.South)
        self.tabsPositionChanged.emit(self.getTabBarPosition())


    def initTabBarPosition(self):
        """  """
        self.tabBarPositionChanged.emit(self.getTabBarPosition())


    tabBarPositionChanged = Signal(QTabWidget.TabPosition)
    tabBarPosition = Property(QTabWidget.TabPosition, getTabBarPosition, setTabBarPosition, notify=tabBarPositionChanged)


    #
    # Property: tabsAutoHide
    #

    def getTabsAutoHide(self):
        """  """
        return self._tabBox.tabBarAutoHide()


    def setTabsAutoHide(self, hide):
        """  """
        if hide != self.getTabsAutoHide():
            self._tabBox.setTabBarAutoHide(hide)
            self.tabsAutoHideChanged.emit(hide)


    def initTabsAutoHide(self):
        """  """
        self._tabBox.setTabBarAutoHide(True)
        self.tabsAutoHideChanged.emit(True)


    tabsAutoHideChanged = Signal(bool)
    tabsAutoHide = Property(bool, getTabsAutoHide, setTabsAutoHide, notify=tabsAutoHideChanged)


    #
    # Slots
    #

    def slotAddTab(self, count):
        """  """
        if not self._tabBox.count():
            for i in range(1, count+1):
                widget = QWidget()
                widget.setAttribute(Qt.WA_DeleteOnClose)
                self._tabBox.addTab(widget, self.tr("Sheet {0}").format(i))

        if self._tabBox.count() > 1:
            self._tabBox.setTabsClosable(True)


    def _slotCloseTab(self, index):
        """  """
        if self._tabBox.count() > 1:
            widget = self._tabBox.widget(index)
            if widget is not None:
                widget.close()
                self._tabBox.removeTab(index)

        if self._tabBox.count() <= 1:
            self._tabBox.setTabsClosable(False)
