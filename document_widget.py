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

from table_document import TableDocument

from PySide2.QtCore import Property, Signal, Qt, QUrl
from PySide2.QtGui import QClipboard
from PySide2.QtWidgets import QApplication


class DocumentWidget(TableDocument):

    def __init__(self, parent=None):
        """  """
        super().__init__(parent=parent)

        self._modified = False
        self._url = QUrl()

        self.setAttribute(Qt.WA_DeleteOnClose)


    def closeEvent(self, event):
        """  """
        self.saveSettings()
        event.accept()


    #
    # Property: modified
    #

    def isModified(self):
        """  """
        return self._modified


    def setModified(self, modified):
        """  """
        if modified != self._modified:
            self._modified = modified
            self.modifiedChanged.emit(modified)


    def resetModified(self):
        """  """
        self._modified = False
        self.modifiedChanged.emit(False)


    def initModified(self):
        """  """
        self.modifiedChanged.emit(self._modified)


    modifiedChanged = Signal(bool)
    modified = Property(bool, isModified, setModified, notify=modifiedChanged)


    #
    # Property: url
    #

    def getUrl(self):
        """  """
        return self._url


    def setUrl(self, url):
        """  """
        if url != self._url:
            self._url = url
            self.urlChanged.emit(url)


    def resetUrl(self):
        """  """
        self._url = QUrl()
        self.urlChanged.emit(QUrl())


    def initUrl(self):
        """  """
        self.urlChanged.emit(self._url)


    urlChanged = Signal(object)
    url = Property(QUrl, getUrl, setUrl, notify=urlChanged)


    #
    #
    #

    def copyPathToClipboard(self):
        """  """
        if not self._url.isEmpty():
            QApplication.clipboard().setText(self._url.toDisplayString(QUrl.FormattingOptions(QUrl.PreferLocalFile)))


    def copyFilenameToClipboard(self):
        """  """
        if not self._url.isEmpty():
            QApplication.clipboard().setText(self._url.fileName())
