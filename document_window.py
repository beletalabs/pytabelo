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

from PySide2.QtCore import Property, Signal, Qt, QDir, QUrl
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QAction, QMdiSubWindow, QMessageBox

from confirmation_dialog import ConfirmationDialog


class DocumentWindow(QMdiSubWindow):

    actionCloseOtherSubWindows = Signal(object)
    actionCopyPath = Signal()
    actionCopyFilename = Signal()


    def __init__(self, parent=None):
        """  """
        super().__init__(parent=parent)

        self._filenameSequenceNumber = 0

        self.setAttribute(Qt.WA_DeleteOnClose)

        self._setupActions()


    def _setupActions(self):
        """  """
        menu = self.systemMenu()
        if menu is None:
            return None

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

        self._actionShowPath = QAction(self.tr("Show &Path"), self)
        self._actionShowPath.setObjectName("actionShowPath")
        self._actionShowPath.setCheckable(True)
        self._actionShowPath.setIcon(QIcon.fromTheme("show-path", QIcon(":/icons/actions/16/show-path.svg")))
        self._actionShowPath.setToolTip(self.tr("Show document path in the tab caption"))
        self._actionShowPath.toggled.connect(self._updateWindowTitle)

        self._actionCopyPath = QAction(self.tr("Cop&y Path"), self)
        self._actionCopyPath.setObjectName("actionCopyPath")
        self._actionCopyPath.setIcon(QIcon.fromTheme("edit-copy-path", QIcon(":/icons/actions/16/edit-copy-path.svg")))
        self._actionCopyPath.setToolTip(self.tr("Copy document path to clipboard"))
        self._actionCopyPath.triggered.connect(self.actionCopyPath)

        self._actionCopyFilename = QAction(self.tr("Copy &Filename"), self)
        self._actionCopyFilename.setObjectName("actionCopyFilename")
        self._actionCopyFilename.setIcon(QIcon.fromTheme("edit-copy-path", QIcon(":/icons/actions/16/edit-copy-path.svg")))
        self._actionCopyFilename.setToolTip(self.tr("Copy document filename to clipboard"))
        self._actionCopyFilename.triggered.connect(self.actionCopyFilename)

        menu.clear()
        menu.addAction(self._actionClose)
        menu.addAction(self._actionCloseOther)
        menu.addSeparator()
        menu.addAction(self._actionShowPath)
        menu.addAction(self._actionCopyPath)
        menu.addAction(self._actionCopyFilename)


    def _enableActionCloseOther(self, enabled):
        """  """
        self._actionCloseOther.setEnabled(enabled)


    #
    # Property: filenameSequenceNumber
    #

    def getFilenameSequenceNumber(self):
        """  """
        return self._filenameSequenceNumber


    def setFilenameSequenceNumber(self, number):
        """  """
        if number != self._filenameSequenceNumber:
            self._filenameSequenceNumber = number


    def initFilenameSequenceNumber(self):
        """  """
        self._filenameSequenceNumber = 0


    filenameSequenceNumber = Property(int, getFilenameSequenceNumber, setFilenameSequenceNumber)


    def _latestFilenameSequenceNumber(self, url):
        """  """
        number = 0

        subWindows = self.mdiArea().subWindowList() if self.mdiArea() is not None else []
        for subWindow in subWindows:
            if subWindow.widget().getUrl().fileName() == url.fileName():
                if subWindow.getFilenameSequenceNumber() > number:
                    number = subWindow.getFilenameSequenceNumber()

        return number


    #
    # Document window
    #

    def windowCaption(self, pathVisible):
        """  """
        if self.widget() is None:
            return None

        caption = self.tr("Untitled")
        url = self.widget().getUrl()

        # Name
        if not url.isEmpty():

            if pathVisible:
                caption = url.toString(QUrl.FormattingOptions(QUrl.PreferLocalFile))
                if caption.startswith(QDir.homePath()):
                    caption = caption.replace(QDir.homePath(), "~", 1)

            elif url.isLocalFile():
                caption = url.fileName()

        # Sequence number
        if (not pathVisible or url.isEmpty()) and self._filenameSequenceNumber > 1:
            caption = self.tr("{0} ({1})").format(caption, self._filenameSequenceNumber)

        return caption


    def _updateWindowTitle(self, pathVisible):
        """  """
        self.setWindowTitle(self.windowCaption(pathVisible))


    def _updateWindowIcon(self, modified):
        """  """
        icon = QIcon.fromTheme("document-save", QIcon(":/icons/actions/16/document-save.svg")) if modified else QIcon()
        self.setWindowIcon(icon)


    #
    # Document
    #

    def documentModifiedChanged(self, modified):
        """  """
        self.setWindowModified(modified)
        self._updateWindowIcon(modified)


    def documentUrlChanged(self, url):
        """  """
        self.initFilenameSequenceNumber()
        self.setFilenameSequenceNumber(self._latestFilenameSequenceNumber(url) + 1)

        self._updateWindowTitle(self._actionShowPath.isChecked())

        self._actionShowPath.setEnabled(not url.isEmpty())
        self._actionCopyPath.setEnabled(not url.isEmpty())
        self._actionCopyFilename.setEnabled(not url.isEmpty())


    def documentCountChanged(self, count):
        """  """
        self._enableActionCloseOther(count >= 2)


    #
    # Action slots
    #

    def _slotCloseOther(self):
        """  """
        count = len(self.mdiArea().subWindowList()) if self.mdiArea() is not None else 0
        if count >= 2:

            title = self.tr("Close all documents except this one")
            text = self.tr("This will close all open documents except this one.\n"
                           "Are you sure you want to continue?")
            buttons = QMessageBox.Yes | QMessageBox.Cancel
            default = QMessageBox.Yes

            if ConfirmationDialog.warning(self, title, text, buttons, default, "ConfirmCloseOtherDocuments") != QMessageBox.Cancel:
                self.actionCloseOtherSubWindows.emit(self)
