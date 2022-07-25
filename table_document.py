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

    documentCountChanged = Signal(int)


    def __init__(self, parent=None):
        """  """
        super().__init__(parent=parent)

        self._tabBox = QTabWidget()
        self._tabBox.setDocumentMode(True)
        self._tabBox.setMovable(True)
        self._tabBox.setTabsClosable(True)
        self._tabBox.tabCloseRequested.connect(self._slotCloseTab)

        self._loadSettings()

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self._tabBox)
        self.setLayout(mainLayout)

        self.documentCountChanged.connect(self._slotAddTab)


    def _loadSettings(self):
        """  """
        settings = QSettings()

        # Sheet Tabs Visible
        visible = settings.value("Document/SheetTabsVisible", True, type=bool)
        self._tabsVisible = visible
        self._setTabBarVisible(visible)

        # Sheet Tabs Position
        value = settings.value("Document/SheetTabsPosition", QTabWidget.South, type=int)
        position = QTabWidget.TabPosition(value) if QTabWidget.TabPosition(value) in [QTabWidget.North, QTabWidget.South] else QTabWidget.South
        self._tabBox.setTabPosition(position)

        # Sheet Tabs Auto Hide
        hide = settings.value("Document/SheetTabsAutoHide", True, type=bool)
        self._tabBox.setTabBarAutoHide(hide)


    def saveSettings(self):
        """  """
        settings = QSettings()


    #
    # Property helper functions
    #

    def _isTabBarVisible(self):
        """  """
        return self._tabBox.tabBar().isVisible()


    def _setTabBarVisible(self, visible):
        """  """
        if not (self._tabBox.count() <= 1 and self.getTabsAutoHide()):
            self._tabBox.tabBar().setVisible(visible)


    #
    # Property: tabsVisible
    #

    def getTabsVisible(self):
        """  """
        return self._tabsVisible


    def setTabsVisible(self, visible):
        """  """
        if visible != self.getTabsVisible:
            self._tabsVisible = visible
            self._setTabBarVisible(visible)
            self.tabsVisibleChanged.emit(visible)


    def initTabsVisible(self):
        """  """
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
        return self._tabBox.tabPosition()


    def setTabsPosition(self, position):
        """  """
        if position != self.getTabsPosition():
            self._tabBox.setTabPosition(position)
            self.tabsPositionChanged.emit(position)


    def initTabsPosition(self):
        """  """
        position = QTabWidget.South
        self._tabBox.setTabPosition(position)
        self.tabsPositionChanged.emit(position)


    tabsPositionChanged = Signal(QTabWidget.TabPosition)
    tabsPosition = Property(QTabWidget.TabPosition, getTabsPosition, setTabsPosition, notify=tabsPositionChanged)


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
    #
    #

    def _slotAddTab(self, count):
        """  """
        if not self._tabBox.count():
            for i in range(1, count+1):
                widget = QWidget()
                widget.setAttribute(Qt.WA_DeleteOnClose)
                self._tabBox.addTab(widget, self.tr("Sheet {0}").format(i))


    def _slotCloseTab(self, index):
        """  """
        widget = self._tabBox.widget(index)
        if widget is not None:
            widget.close()
        self._tabBox.removeTab(index)
