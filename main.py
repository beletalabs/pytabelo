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

import sys

from PySide2.QtCore import QCommandLineParser, QDir, QUrl
from PySide2.QtWidgets import QApplication

from application_window import ApplicationWindow


if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setOrganizationName("Beleta Labs")
    app.setOrganizationDomain("https://beletalabs.github.io")
    app.setApplicationName("PyTabelo")
    app.setApplicationDisplayName("PyTabelo")
    app.setApplicationVersion("0.1.0")

    # Command line
    parser = QCommandLineParser()
    parser.setApplicationDescription("{0} - A table editor based on Qt for Python".format(app.applicationName()))
    parser.addHelpOption()
    parser.addVersionOption()
    parser.addPositionalArgument("urls", QApplication.translate("main", "Documents to open."), "[urls...]")
    parser.process(app)


    #
    # Application window

    window = ApplicationWindow()
    window.show()

    urls = parser.positionalArguments()
    for url in urls:
        window.openDocument(QUrl.fromUserInput(url, QDir.currentPath(), QUrl.AssumeLocalFile))


    sys.exit(app.exec_())
