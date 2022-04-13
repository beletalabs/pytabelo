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

from PySide2.QtCore import Qt, QSettings
from PySide2.QtWidgets import QCheckBox, QMessageBox


class ConfirmationDialog(QMessageBox):

    def __init__(self, confirmationKey, parent=None):
        super().__init__(parent=parent)

        self._confirmationKey = confirmationKey
        self._cbDoNotShowAgain = None

        if self._confirmationKey:
            self._cbDoNotShowAgain = QCheckBox(self.tr("Do not show again"))
            self.setCheckBox(self._cbDoNotShowAgain)


    def information(parent, title, text, buttons=QMessageBox.Ok, defaultButton=QMessageBox.NoButton, confirmationKey=""):

        dialog = ConfirmationDialog(confirmationKey, self);
        dialog.setIcon(QMessageBox.Information)
        dialog.setWindowTitle(title);
        dialog.setText(text);
        dialog.setStandardButtons(buttons);
        dialog.setDefaultButton(defaultButton);

        return dialog._execute()


    def warning(self, title, text, buttons=QMessageBox.Ok, defaultButton=QMessageBox.NoButton, confirmationKey=""):

        dialog = ConfirmationDialog(confirmationKey, self);
        dialog.setIcon(QMessageBox.Warning)
        dialog.setWindowTitle(title);
        dialog.setText(text);
        dialog.setStandardButtons(buttons);
        dialog.setDefaultButton(defaultButton);

        return dialog._execute()


    def critical(self, title, text, buttons=QMessageBox.Ok, defaultButton=QMessageBox.NoButton, confirmationKey=""):

        dialog = ConfirmationDialog(confirmationKey, self);
        dialog.setIcon(QMessageBox.Critical)
        dialog.setWindowTitle(title);
        dialog.setText(text);
        dialog.setStandardButtons(buttons);
        dialog.setDefaultButton(defaultButton);

        return dialog._execute()


    def question(self, title, text, buttons=QMessageBox.Ok, defaultButton=QMessageBox.NoButton, confirmationKey=""):

        dialog = ConfirmationDialog(confirmationKey, self);
        dialog.setIcon(QMessageBox.Question)
        dialog.setWindowTitle(title);
        dialog.setText(text);
        dialog.setStandardButtons(buttons);
        dialog.setDefaultButton(defaultButton);

        return dialog._execute()


    def _execute(self):

        settings = QSettings()

        if self._cbDoNotShowAgain is not None:
            confirm = settings.value("Confirmations/" + self._confirmationKey, True, type=bool)
            if not confirm:
                return QMessageBox.NoButton

        self.exec_()

        if self._cbDoNotShowAgain is not None:
            settings.setValue("Confirmations/" + self._confirmationKey, not self._cbDoNotShowAgain.isChecked())

        return self.standardButton(self.clickedButton())
