# This Python file uses the following encoding: utf-8
#
# Copyright 2022 Tabelo, <https://github.com/tabeloapp>.
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

from PySide2.QtWidgets import QApplication, QFrame, QTextBrowser, QVBoxLayout, QWidget


#
#
# Colophon page: About
#

class ColophonPageAbout(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        text = "<html><body>"
        text += self.tr("<p>{0} is an open source table editor written in Python using the Python bindings for the Qt framework.</p>").format(QApplication.applicationName())
        text += self.tr("<p>Copyright &copy; 2022 <a href=\"{0}\" title=\"Visit organization's homepage\">{1}</a>.</p>").format(QApplication.organizationDomain(), QApplication.organizationName())
        text += self.tr("<p>This application is licensed under the terms of the <a href=\"https://www.gnu.org/licenses/gpl-3.0.en.html\" title=\"Visit license's homepage\">GNU General Public License, version 3</a>.</p>")
        text += "</body></html>"

        textBox = QTextBrowser()
        textBox.setFrameStyle(QFrame.NoFrame)
        textBox.setStyleSheet("background-color:transparent;")
        textBox.setOpenExternalLinks(True)
        textBox.setHtml(text)

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(textBox)
        self.setLayout(mainLayout)


    def title(self):

        return self.tr("About")


#
#
# Colophon page: Authors
#

class ColophonPageAuthors(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        text = "<html><body><dl>"
        text += self.tr("<dt><strong>naracanto</strong></dt>")
        text += self.tr("<dd>Created and developed by <a href=\"https://naracanto.com\" title=\"Visit author's homepage\">naracanto</a>.</dd>")
        text += "</dl></body></html>"

        textBox = QTextBrowser()
        textBox.setFrameStyle(QFrame.NoFrame)
        textBox.setStyleSheet("background-color:transparent;")
        textBox.setOpenExternalLinks(True)
        textBox.setHtml(text)

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(textBox)
        self.setLayout(mainLayout)


    def title(self):

        return self.tr("Authors")


#
#
# Colophon page: Credits
#

class ColophonPageCredits(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        text = "<html><body><dl>"
        text += self.tr("<dt><strong>BreezeIcons project</strong></dt>")
        text += self.tr("<dd>Application logo and icons made by <a href=\"https://api.kde.org/frameworks/breeze-icons/html/\" title=\"Visit project's homepage\">BreezeIcons project</a> "
                        "from <a href=\"https://kde.org\" title=\"Visit organization's homepage\">KDE</a> are licensed under <a href=\"https://www.gnu.org/licenses/lgpl-3.0.en.html\" title=\"Visit license's homepage\">LGPLv3</a>.</dd>")
        text += "</dl></body></html>"

        textBox = QTextBrowser()
        textBox.setFrameStyle(QFrame.NoFrame)
        textBox.setStyleSheet("background-color:transparent;")
        textBox.setOpenExternalLinks(True)
        textBox.setHtml(text)

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(textBox)
        self.setLayout(mainLayout)


    def title(self):

        return self.tr("Credits")
