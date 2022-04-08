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

from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QAction, QMdiSubWindow, QMessageBox

from confirmation_dialog import ConfirmationDialog


class MdiWindow(QMdiSubWindow):

    closeOtherSubWindows = Signal(object)


    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setAttribute(Qt.WA_DeleteOnClose)

        self._setupActions()


    def _setupActions(self):

        menu = self.systemMenu()
        if not menu:
            return

        self._actionClose = QAction(self.tr("&Close"), self)
        self._actionClose.setObjectName("actionClose")
        self._actionClose.setIcon(QIcon.fromTheme("window-close", QIcon(":/icons/actions/16/window-close.svg")))
        self._actionClose.setToolTip(self.tr("Close document"))
        self._actionClose.triggered.connect(self.close)

        self._actionCloseOther = QAction(self.tr("Close Ot&her"), self)
        self._actionCloseOther.setObjectName("actionCloseOther")
        self._actionCloseOther.setIcon(QIcon.fromTheme("window-close", QIcon(":/icons/actions/16/window-close.svg")))
        self._actionCloseOther.setToolTip(self.tr("Close other open documents"))
        self._actionCloseOther.triggered.connect(self._slotCloseOther)

        menu.clear()
        menu.addAction(self._actionClose)
        menu.addAction(self._actionCloseOther)


    def _enableActionCloseOther(self, enabled):

        self._actionCloseOther.setEnabled(enabled)


    def subWindowCountChanged(self, count):

        self._enableActionCloseOther(count >= 2)


    def _slotCloseOther(self):

        count = len(self.mdiArea().subWindowList()) if self.mdiArea() else 0
        if count >= 2:

            title = self.tr("Close all documents except this one")
            text = self.tr("This will close all open documents except this one.\n"
                           "Are you sure you want to continue?")
            buttons = QMessageBox.Yes | QMessageBox.Cancel
            default = QMessageBox.Yes

            if ConfirmationDialog.warning(self, title, text, buttons, default, "ConfirmCloseOther") is not QMessageBox.Cancel:
                self.closeOtherSubWindows.emit(self)
