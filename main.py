# This Python file uses the following encoding: utf-8
#
# Copyright 2022 naracanto <https://naracanto.github.io>.
#
# This file is part of Tabelo-QtPy, <https://github.com/tabeloapp/tabelo-qtpy>.
#
# Tabelo-QtPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tabelo-QtPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tabelo-QtPy.  If not, see <https://www.gnu.org/licenses/>.
#

import sys

from PySide2.QtCore import QCommandLineParser
from PySide2.QtWidgets import QApplication

from window import Window


if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setOrganizationName("Tabelo")
    app.setOrganizationDomain("https://github.com/tabeloapp")
    app.setApplicationName("Tabelo-QtPy")
    app.setApplicationDisplayName("Tabelo-QtPy")
    app.setApplicationVersion("0.1.0")

    # Command line
    parser = QCommandLineParser()
    parser.setApplicationDescription("{0} - A table editor based on Qt for Python".format(app.applicationName()))
    parser.addHelpOption()
    parser.addVersionOption()
    parser.process(app)

    window = Window()
    window.show()

    sys.exit(app.exec_())
