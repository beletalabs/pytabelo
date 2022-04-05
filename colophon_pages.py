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

import sys
import PySide2.QtCore

from PySide2.QtCore import QSysInfo
from PySide2.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget


#
#
# Colophon page: About
#

class ColophonPageAbout(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        description = QLabel()
        description.setWordWrap(True)
        description.setOpenExternalLinks(True)
        description.setText(self.tr(
            "{0} is an open source table editor written in Python using the Python bindings for the Qt framework."
        ).format(QApplication.applicationName()))

        copyright = QLabel()
        copyright.setWordWrap(True)
        copyright.setOpenExternalLinks(True)
        copyright.setText(self.tr(
            "Copyright &copy; 2022 <a href=\"{0}\" title=\"Visit organization's homepage\">{1}</a>."
        ).format(QApplication.organizationDomain(), QApplication.organizationName()))

        license = QLabel()
        license.setWordWrap(True)
        license.setOpenExternalLinks(True)
        license.setText(self.tr(
            "This application is licensed under the terms of the "
            "<a href=\"https://www.gnu.org/licenses/gpl-3.0.en.html\" title=\"Visit license's homepage\">GNU General Public License, version 3</a>."
        ))

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(description)
        mainLayout.addWidget(copyright)
        mainLayout.addWidget(license)
        mainLayout.addStretch()
        self.setLayout(mainLayout)


    def title(self):

        return self.tr("About")


#
#
# Colophon page: Authors
#

class ColophonPageAuthors(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        author1 = QLabel()
        author1.setWordWrap(True)
        author1.setOpenExternalLinks(True)
        author1.setText(self.tr(
            "<dl>"
                "<dt><strong>naracanto</strong></dt>"
                "<dd>Created and developed by <a href=\"https://naracanto.github.io\" title=\"Visit author's homepage\">naracanto</a>.</dd>"
            "</dl>"
        ))

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(author1)
        mainLayout.addStretch()
        self.setLayout(mainLayout)


    def title(self):

        return self.tr("Authors")


#
#
# Colophon page: Credits
#

class ColophonPageCredits(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        credit1 = QLabel()
        credit1.setWordWrap(True)
        credit1.setOpenExternalLinks(True)
        credit1.setText(self.tr(
            "<dl>"
                "<dt><strong>BreezeIcons project</strong></dt>"
                "<dd>Application logo and icons made by "
                    "<a href=\"https://api.kde.org/frameworks/breeze-icons/html/\" title=\"Visit project's homepage\">BreezeIcons project</a> "
                    "from <a href=\"https://kde.org\" title=\"Visit organization's homepage\">KDE</a> are licensed under "
                    "<a href=\"https://www.gnu.org/licenses/lgpl-3.0.en.html\" title=\"Visit license's homepage\">LGPLv3</a>.</dd>"
            "</dl>"
        ))

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(credit1)
        mainLayout.addStretch()
        self.setLayout(mainLayout)


    def title(self):

        return self.tr("Credits")


#
#
# Colophon page: Environment
#

class ColophonPageEnvironment(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        pysideVersion = PySide2.__version__
        qtVersion = PySide2.QtCore.qVersion()  # Qt version used to run Qt for Python
        qtBuildVersion = PySide2.QtCore.__version__  # Qt version used to compile PySide2
        pythonVersion = sys.version
        osName = QSysInfo.prettyProductName()
        osKernelVersion = QSysInfo.kernelVersion()
        osCpuArchitecture = QSysInfo.currentCpuArchitecture()


        app = QLabel()
        app.setWordWrap(True)
        app.setOpenExternalLinks(True)
        app.setText(self.tr(
            "<dl>"
                "<dt><strong>Application version</strong></dt>"
                "<dd>{0}</dd>"
            "</dl>"
        ).format(QApplication.applicationVersion()))

        pyside = QLabel()
        pyside.setWordWrap(True)
        pyside.setOpenExternalLinks(True)
        pyside.setText(self.tr(
            "<dl>"
                "<dt><strong>Qt for Python version</strong></dt>"
                "<dd>{0} runs on Qt {1} (Built against {2})</dd>"
            "</dl>"
        ).format(pysideVersion, qtVersion, qtBuildVersion))

        python = QLabel()
        python.setWordWrap(True)
        python.setOpenExternalLinks(True)
        python.setText(self.tr(
            "<dl>"
                "<dt><strong>Python version</strong></dt>"
                "<dd>{0}</dd>"
            "</dl>"
        ).format(pythonVersion))

        os = QLabel()
        os.setWordWrap(True)
        os.setOpenExternalLinks(True)
        os.setText(self.tr(
            "<dl>"
                "<dt><strong>Operation System</strong></dt>"
                "<dd>{0} (Kernel {1} on {2})</dd>"
            "</dl>"
        ).format(osName, osKernelVersion, osCpuArchitecture))

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(app)
        mainLayout.addWidget(pyside)
        mainLayout.addWidget(python)
        mainLayout.addWidget(os)
        mainLayout.addStretch()
        self.setLayout(mainLayout)


    def title(self):

        return self.tr("Environment")


#
#
# Colophon page: License
#

class ColophonPageLicense(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        license1 = QLabel()
        license1.setWordWrap(True)
        license1.setOpenExternalLinks(True)
        license1.setText(self.tr(
            "{0} is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License "
            "as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version."
        ).format(QApplication.applicationName()))

        license2 = QLabel()
        license2.setWordWrap(True)
        license2.setOpenExternalLinks(True)
        license2.setText(self.tr(
            "{0} is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of "
            "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details."
        ).format(QApplication.applicationName()))

        license3 = QLabel()
        license3.setWordWrap(True)
        license3.setOpenExternalLinks(True)
        license3.setText(self.tr(
            "You should have received a copy of the GNU General Public License along with {0}. If not, see "
            "<a href=\"https://www.gnu.org/licenses/\" title=\"Visit license's homepage\">https://www.gnu.org/licenses/</a>."
        ).format(QApplication.applicationName()))

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(license1)
        mainLayout.addWidget(license2)
        mainLayout.addWidget(license3)
        mainLayout.addStretch()
        self.setLayout(mainLayout)


    def title(self):

        return self.tr("License")
