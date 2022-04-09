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

from table_document import TableDocument

from PySide2.QtCore import Property, QUrl, Signal


class MdiDocument(TableDocument):

    urlChanged = Signal(object)


    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._url = QUrl()


    def getUrl(self):

        return self._url


    def setUrl(self, url):

        if url != self._url:
            self._url = url
            self.urlChanged.emit(url)


    def initUrl(self):

        self._url = QUrl()
        self.urlChanged.emit(QUrl())


    url = Property(QUrl, getUrl, setUrl, notify=urlChanged)
