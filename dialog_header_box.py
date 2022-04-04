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
from PySide2.QtSvg import QSvgWidget
from PySide2.QtWidgets import QApplication, QGridLayout, QLabel, QWidget

import icons_rc


class DialogHeaderBox(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        logo = QSvgWidget()
        logo.load(":/icons/apps/22/tabelo.svg")

        title = QLabel("<strong style=\"font-size:large;\">{0}</strong>".format(QApplication.applicationName()))
        version = QLabel(QApplication.applicationVersion())
        subtitle = QLabel(self.tr("A table editor based on Qt for Python"))

        # Main layout
        mainLayout = QGridLayout()
        mainLayout.addWidget(logo, 0, 0, 2, 1)
        mainLayout.addWidget(title, 0, 1, 1, 1)
        mainLayout.addWidget(version, 0, 2, 1, 1, Qt.AlignBottom)
        mainLayout.addWidget(subtitle, 1, 1, 1, 2)
        mainLayout.setColumnStretch(2, 1)
        self.setLayout(mainLayout)

        # Logo size
        height = title.sizeHint().height() + mainLayout.verticalSpacing() + subtitle.sizeHint().height()
        logo.setFixedSize(height, height)
