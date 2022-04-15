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
from PySide2.QtWidgets import QTabWidget, QVBoxLayout, QWidget


class TableDocument(QWidget):

    documentCountChanged = Signal(int)

    tabBarVisibleChanged = Signal(bool)
    tabPositionChanged = Signal(QTabWidget.TabPosition)
    tabBarAutoHideChanged = Signal(bool)


    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._tabBarVisible = True
        self._tabPosition = QTabWidget.South
        self._tabBarAutoHide = True

        self._tabBox = QTabWidget()
        self._tabBox.setDocumentMode(True)
        self._tabBox.setMovable(True)
        self._tabBox.setTabBarAutoHide(self._tabBarAutoHide)
        self._tabBox.setTabPosition(self._tabPosition)
        self._tabBox.setTabsClosable(True)
        self._tabBox.tabCloseRequested.connect(self._closeTab)

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self._tabBox)
        self.setLayout(mainLayout)

        self.documentCountChanged.connect(self._addTab)


    def getTabBarVisible(self):

        return self._tabBarVisible


    def setTabBarVisible(self, visible):

        if visible != self._tabBarVisible:
            self._tabBarVisible = visible
            self.tabBarVisibleChanged.emit(visible)

            if self._tabBox.count() == 1 and not self.getTabBarAutoHide():
                self._tabBox.tabBar().setVisible(visible)
            if self._tabBox.count() >= 2:
                self._tabBox.tabBar().setVisible(visible)


    tabBarVisible = Property(bool, getTabBarVisible, setTabBarVisible, notify=tabBarVisibleChanged)


    def initTabBarVisible(self):

        self._tabBarVisible = True
        self.tabBarVisibleChanged.emit(self._tabBarVisible)

        if self._tabBox.count() == 1 and not self.getTabBarAutoHide():
            self._tabBox.tabBar().setVisible(self._tabBarVisible)
        if self._tabBox.count() >= 2:
            self._tabBox.tabBar().setVisible(self._tabBarVisible)


    def isTabBarVisible(self):

        return self._tabBox.tabBar().isVisible()


    def getTabPosition(self):

        return self._tabBox.tabPosition()


    def setTabPosition(self, position):

        if position != self._tabBox.tabPosition():
            self._tabBox.setTabPosition(position)
            self.tabPositionChanged.emit(position)


    tabPosition = Property(QTabWidget.TabPosition, getTabPosition, setTabPosition, notify=tabPositionChanged)


    def initTabPosition(self):

        self._tabBox.setTabPosition(self._tabPosition)
        self.tabPositionChanged.emit(self._tabPosition)


    def getTabBarAutoHide(self):

        return self._tabBox.tabBarAutoHide()


    def setTabBarAutoHide(self, hide):

        if hide != self._tabBox.tabBarAutoHide():
            self._tabBox.setTabBarAutoHide(hide)
            self.tabBarAutoHideChanged.emit(hide)


    tabBarAutoHide = Property(bool, getTabBarAutoHide, setTabBarAutoHide, notify=tabBarAutoHideChanged)


    def initTabBarAutoHide(self):

        self._tabBox.setTabBarAutoHide(self._tabBarAutoHide)
        self.tabBarAutoHideChanged.emit(self._tabBarAutoHide)


    def _addTab(self, count):

        if not self._tabBox.count():
            for i in range(1, count+1):
                widget = QWidget()
                widget.setAttribute(Qt.WA_DeleteOnClose)
                self._tabBox.addTab(widget, self.tr("Sheet {0}").format(i))


    def _closeTab(self, index):

        widget = self._tabBox.widget(index)
        if widget is not None:
            widget.close()

        self._tabBox.removeTab(index)
