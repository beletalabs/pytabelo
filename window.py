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

from PySide2.QtCore import QByteArray, QSettings, Qt
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtWidgets import QAction, QActionGroup, QApplication, QMainWindow, QMenu

from about_dialog import AboutDialog
from colophon_dialog import ColophonDialog
from preferences_dialog import PreferencesDialog

import icons_rc


class Window(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowIcon(QIcon(":/icons/apps/16/tabelo.svg"))

        self._createActions()
        self._createMenuBar()
        self._createStatusBar()
        self._createToolBars()

        self._loadSettings()


    def closeEvent(self, event):

        if True:
            # Store application properties
            self._saveSettings()

            event.accept()
        else:
            event.ignore()


    def _loadSettings(self):

        settings = QSettings()

        # Application property: Geometry
        geometry = settings.value("Application/Geometry", QByteArray())
        if not geometry.isEmpty():
            self.restoreGeometry(geometry)
        else:
            # Default: Center window
            availableGeometry = self.screen().availableGeometry()
            self.resize(availableGeometry.width() * 2/3, availableGeometry.height() * 2/3)
            self.move((availableGeometry.width() - self.width()) / 2, (availableGeometry.height() - self.height()) / 2)

        # Application property: State
        state = settings.value("Application/State", QByteArray())
        if not state.isEmpty():
            self.restoreState(state)
        else:
            # Default: Show/hide toolbars
            self._toolbarApplication.setVisible(True)
            self._toolbarFile.setVisible(True)
            self._toolbarEdit.setVisible(True)
            self._toolbarView.setVisible(True)
            self._toolbarFormat.setVisible(True)
            self._toolbarTools.setVisible(True)
            self._toolbarAppearance.setVisible(False)
            self._toolbarHelp.setVisible(False)

        # Application property: Menu Bar
        visibleMenuBar = settings.value("Application/MenuBar", True, type=bool)
        self.menuBar().setVisible(visibleMenuBar)
        self._actionMenubar.setChecked(visibleMenuBar)

        # Application property: Status Bar
        visible = settings.value("Application/StatusBar", True, type=bool)
        self._statusbar.setVisible(visible)
        self._actionStatusbar.setChecked(visible)

        # Application property: Tool Button Style
        style = settings.value("Application/ToolButtonStyle", Qt.ToolButtonFollowStyle, type=int)
        self._updateActionsToolButtonStyle(Qt.ToolButtonStyle(style))


    def _saveSettings(self):

        settings = QSettings()

        # Application property: Geometry
        geometry = self.saveGeometry()
        settings.setValue("Application/Geometry", geometry)

        # Application property: State
        state = self.saveState()
        settings.setValue("Application/State", state)

        # Application property: Status Bar
        visible = self._statusbar.isVisible()
        settings.setValue("Application/StatusBar", visible)

        # Application property: Tool Button Style
        style = self._actionsToolButtonStyle.checkedAction().data()
        settings.setValue("Application/ToolButtonStyle", style)


    def _createActions(self):

        #
        # Actions: Application

        self._actionAbout = QAction(self.tr("About {0}").format(QApplication.applicationName()), self)
        self._actionAbout.setObjectName("actionAbout")
        self._actionAbout.setIcon(QIcon(":/icons/apps/16/tabelo.svg"))
        self._actionAbout.setIconText(self.tr("About"))
        self._actionAbout.setToolTip(self.tr("Brief description of the application"))
        self._actionAbout.triggered.connect(self._onActionAboutTriggered)

        self._actionColophon = QAction(self.tr("Colophon"), self)
        self._actionColophon.setObjectName("actionColophon")
        self._actionColophon.setToolTip(self.tr("Lengthy description of the application"))
        self._actionColophon.triggered.connect(self._onActionColophonTriggered)

        self._actionPreferences = QAction(self.tr("Preferences…"), self)
        self._actionPreferences.setObjectName("actionPreferences")
        self._actionPreferences.setIcon(QIcon.fromTheme("configure", QIcon(":/icons/actions/16/configure.svg")))
        self._actionPreferences.setToolTip(self.tr("Customize the appearance and behavior of the application"))
        self._actionPreferences.triggered.connect(self._onActionPreferencesTriggered)

        self._actionQuit = QAction(self.tr("Quit"), self)
        self._actionQuit.setObjectName("actionQuit")
        self._actionQuit.setIcon(QIcon.fromTheme("application-exit", QIcon(":/icons/actions/16/application-exit.svg")))
        self._actionQuit.setShortcut(QKeySequence.Quit)
        self._actionQuit.setToolTip(self.tr("Quit the application"))
        self._actionQuit.triggered.connect(self.close)


        #
        # Actions: Appearance

        self._actionMenubar = QAction(self.tr("Show Menu Bar"), self)
        self._actionMenubar.setObjectName("actionMenubar")
        self._actionMenubar.setCheckable(True)
        self._actionMenubar.setIcon(QIcon.fromTheme("show-menu", QIcon(":/icons/actions/16/show-menu.svg")))
        self._actionMenubar.setIconText("Menu Bar")
        self._actionMenubar.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_M))
        self._actionMenubar.setToolTip(self.tr("Display the Menu bar"))
        self._actionMenubar.toggled.connect(lambda checked: self.menuBar().setVisible(checked))
        self.addAction(self._actionMenubar)

        self._actionToolbarApplication = QAction(self.tr("Show Application Toolbar"), self)
        self._actionToolbarApplication.setObjectName("actionToolbarApplication")
        self._actionToolbarApplication.setCheckable(True)
        self._actionToolbarApplication.setToolTip(self.tr("Display the Application toolbar"))
        self._actionToolbarApplication.toggled.connect(lambda checked: self._toolbarApplication.setVisible(checked))

        self._actionToolbarFile = QAction(self.tr("Show File Toolbar"), self)
        self._actionToolbarFile.setObjectName("actionToolbarFile")
        self._actionToolbarFile.setCheckable(True)
        self._actionToolbarFile.setToolTip(self.tr("Display the File toolbar"))
        self._actionToolbarFile.toggled.connect(lambda checked: self._toolbarFile.setVisible(checked))

        self._actionToolbarEdit = QAction(self.tr("Show Edit Toolbar"), self)
        self._actionToolbarEdit.setObjectName("actionToolbarEdit")
        self._actionToolbarEdit.setCheckable(True)
        self._actionToolbarEdit.setToolTip(self.tr("Display the Edit toolbar"))
        self._actionToolbarEdit.toggled.connect(lambda checked: self._toolbarEdit.setVisible(checked))

        self._actionToolbarView = QAction(self.tr("Show View Toolbar"), self)
        self._actionToolbarView.setObjectName("actionToolbarView")
        self._actionToolbarView.setCheckable(True)
        self._actionToolbarView.setToolTip(self.tr("Display the View toolbar"))
        self._actionToolbarView.toggled.connect(lambda checked: self._toolbarView.setVisible(checked))

        self._actionToolbarFormat = QAction(self.tr("Show Format Toolbar"), self)
        self._actionToolbarFormat.setObjectName("actionToolbarFormat")
        self._actionToolbarFormat.setCheckable(True)
        self._actionToolbarFormat.setToolTip(self.tr("Display the Format toolbar"))
        self._actionToolbarFormat.toggled.connect(lambda checked: self._toolbarFormat.setVisible(checked))

        self._actionToolbarTools = QAction(self.tr("Show Tools Toolbar"), self)
        self._actionToolbarTools.setObjectName("actionToolbarTools")
        self._actionToolbarTools.setCheckable(True)
        self._actionToolbarTools.setToolTip(self.tr("Display the Tools toolbar"))
        self._actionToolbarTools.toggled.connect(lambda checked: self._toolbarTools.setVisible(checked))

        self._actionToolbarAppearance = QAction(self.tr("Show Appearance Toolbar"), self)
        self._actionToolbarAppearance.setObjectName("actionToolbarAppearance")
        self._actionToolbarAppearance.setCheckable(True)
        self._actionToolbarAppearance.setToolTip(self.tr("Display the Appearance toolbar"))
        self._actionToolbarAppearance.toggled.connect(lambda checked: self._toolbarAppearance.setVisible(checked))

        self._actionToolbarHelp = QAction(self.tr("Show Help Toolbar"), self)
        self._actionToolbarHelp.setObjectName("actionToolbarHelp")
        self._actionToolbarHelp.setCheckable(True)
        self._actionToolbarHelp.setToolTip(self.tr("Display the Help toolbar"))
        self._actionToolbarHelp.toggled.connect(lambda checked: self._toolbarHelp.setVisible(checked))

        self._actionStatusbar = QAction(self.tr("Show Status Bar"), self)
        self._actionStatusbar.setObjectName("actionStatusbar")
        self._actionStatusbar.setCheckable(True)
        self._actionStatusbar.setToolTip(self.tr("Display the Status bar"))
        self._actionStatusbar.toggled.connect(lambda checked: self._statusbar.setVisible(checked))


        #
        # Action group: Tool Button Style

        actionToolButtonStyleIconOnly = QAction(self.tr("Icon Only"), self)
        actionToolButtonStyleIconOnly.setObjectName("actionToolButtonStyleIconOnly")
        actionToolButtonStyleIconOnly.setCheckable(True)
        actionToolButtonStyleIconOnly.setToolTip(self.tr("Only display the icon"))
        actionToolButtonStyleIconOnly.setData(Qt.ToolButtonIconOnly)

        actionToolButtonStyleTextOnly = QAction(self.tr("Text Only"), self)
        actionToolButtonStyleTextOnly.setObjectName("actionToolButtonStyleTextOnly")
        actionToolButtonStyleTextOnly.setCheckable(True)
        actionToolButtonStyleTextOnly.setToolTip(self.tr("Only display the text"))
        actionToolButtonStyleTextOnly.setData(Qt.ToolButtonTextOnly)

        actionToolButtonStyleTextBesideIcon = QAction(self.tr("Text Beside Icon"), self)
        actionToolButtonStyleTextBesideIcon.setObjectName("actionToolButtonStyleTextBesideIcon")
        actionToolButtonStyleTextBesideIcon.setCheckable(True)
        actionToolButtonStyleTextBesideIcon.setToolTip(self.tr("The text appears beside the icon"))
        actionToolButtonStyleTextBesideIcon.setData(Qt.ToolButtonTextBesideIcon)

        actionToolButtonStyleTextUnderIcon = QAction(self.tr("Text Under Icon"), self)
        actionToolButtonStyleTextUnderIcon.setObjectName("actionToolButtonStyleTextUnderIcon")
        actionToolButtonStyleTextUnderIcon.setCheckable(True)
        actionToolButtonStyleTextUnderIcon.setToolTip(self.tr("The text appears under the icon"))
        actionToolButtonStyleTextUnderIcon.setData(Qt.ToolButtonTextUnderIcon)

        actionToolButtonStyleFollowStyle = QAction(self.tr("Follow Style"), self)
        actionToolButtonStyleFollowStyle.setObjectName("actionToolButtonStyleFollowStyle")
        actionToolButtonStyleFollowStyle.setCheckable(True)
        actionToolButtonStyleFollowStyle.setToolTip(self.tr("Follow the style"))
        actionToolButtonStyleFollowStyle.setData(Qt.ToolButtonFollowStyle)

        self._actionsToolButtonStyle = QActionGroup(self)
        self._actionsToolButtonStyle.setObjectName("actionsToolButtonStyle")
        self._actionsToolButtonStyle.addAction(actionToolButtonStyleIconOnly)
        self._actionsToolButtonStyle.addAction(actionToolButtonStyleTextOnly)
        self._actionsToolButtonStyle.addAction(actionToolButtonStyleTextBesideIcon)
        self._actionsToolButtonStyle.addAction(actionToolButtonStyleTextUnderIcon)
        self._actionsToolButtonStyle.addAction(actionToolButtonStyleFollowStyle)
        self._actionsToolButtonStyle.triggered.connect(self._onActionsToolButtonStyleTriggered)


    def _createMenuBar(self):

        # Menu: Application
        menuApplication = self.menuBar().addMenu(self.tr("Application"))
        menuApplication.setObjectName("menuApplication")
        menuApplication.addAction(self._actionAbout)
        menuApplication.addAction(self._actionColophon)
        menuApplication.addSeparator()
        menuApplication.addAction(self._actionPreferences)
        menuApplication.addSeparator()
        menuApplication.addAction(self._actionQuit)

        # Menu: File
        menuFile = self.menuBar().addMenu(self.tr("File"))
        menuFile.setObjectName("menuFile")

        # Menu: Edit
        menuEdit = self.menuBar().addMenu(self.tr("Edit"))
        menuEdit.setObjectName("menuEdit")

        # Menu: View
        menuView = self.menuBar().addMenu(self.tr("View"))
        menuView.setObjectName("menuView")

        # Menu: Format
        menuFormat = self.menuBar().addMenu(self.tr("Format"))
        menuFormat.setObjectName("menuFormat")

        # Menu: Tools
        menuTools = self.menuBar().addMenu(self.tr("Tools"))
        menuTools.setObjectName("menuTools")


        #
        # Menus: Appearance

        menuToolButtonStyle = QMenu(self.tr("Tool Button Style"), self)
        menuToolButtonStyle.setObjectName("menuToolButtonStyle")
        menuToolButtonStyle.addActions(self._actionsToolButtonStyle.actions())

        menuAppearance = self.menuBar().addMenu(self.tr("Appearance"))
        menuAppearance.setObjectName("menuAppearance")
        menuAppearance.addAction(self._actionMenubar)
        menuAppearance.addSeparator()
        menuAppearance.addAction(self._actionToolbarApplication)
        menuAppearance.addAction(self._actionToolbarFile)
        menuAppearance.addAction(self._actionToolbarEdit)
        menuAppearance.addAction(self._actionToolbarView)
        menuAppearance.addAction(self._actionToolbarFormat)
        menuAppearance.addAction(self._actionToolbarTools)
        menuAppearance.addAction(self._actionToolbarAppearance)
        menuAppearance.addAction(self._actionToolbarHelp)
        menuAppearance.addMenu(menuToolButtonStyle)
        menuAppearance.addSeparator()
        menuAppearance.addAction(self._actionStatusbar)


        # Menu: Help
        menuHelp = self.menuBar().addMenu(self.tr("Help"))
        menuHelp.setObjectName("menuHelp")


    def _createStatusBar(self):

        self._statusbar = self.statusBar()
        self._statusbar.showMessage(self.tr("Ready"), 3000)


    def _createToolBars(self):

        # Toolbar: Application
        self._toolbarApplication = self.addToolBar(self.tr("Application Toolbar"))
        self._toolbarApplication.setObjectName("toolbarApplication")
        self._toolbarApplication.addAction(self._actionAbout)
        self._toolbarApplication.addAction(self._actionPreferences)
        self._toolbarApplication.addSeparator()
        self._toolbarApplication.addAction(self._actionQuit)
        self._toolbarApplication.visibilityChanged.connect(lambda visible: self._actionToolbarApplication.setChecked(visible))

        # Toolbar: File
        self._toolbarFile = self.addToolBar(self.tr("File Toolbar"))
        self._toolbarFile.setObjectName("toolbarFile")
        self._toolbarFile.visibilityChanged.connect(lambda visible: self._actionToolbarFile.setChecked(visible))

        # Toolbar: Edit
        self._toolbarEdit = self.addToolBar(self.tr("Edit Toolbar"))
        self._toolbarEdit.setObjectName("toolbarEdit")
        self._toolbarEdit.visibilityChanged.connect(lambda visible: self._actionToolbarEdit.setChecked(visible))

        # Toolbar: View
        self._toolbarView = self.addToolBar(self.tr("View Toolbar"))
        self._toolbarView.setObjectName("toolbarView")
        self._toolbarView.visibilityChanged.connect(lambda visible: self._actionToolbarView.setChecked(visible))

        # Toolbar: Format
        self._toolbarFormat = self.addToolBar(self.tr("Format Toolbar"))
        self._toolbarFormat.setObjectName("toolbarFormat")
        self._toolbarFormat.visibilityChanged.connect(lambda visible: self._actionToolbarFormat.setChecked(visible))

        # Toolbar: Tools
        self._toolbarTools = self.addToolBar(self.tr("Tools Toolbar"))
        self._toolbarTools.setObjectName("toolbarTools")
        self._toolbarTools.visibilityChanged.connect(lambda visible: self._actionToolbarTools.setChecked(visible))

        # Toolbar: Appearance
        self._toolbarAppearance = self.addToolBar(self.tr("Appearance Toolbar"))
        self._toolbarAppearance.setObjectName("toolbarAppearance")
        self._toolbarAppearance.addAction(self._actionMenubar)
        self._toolbarAppearance.visibilityChanged.connect(lambda visible: self._actionToolbarAppearance.setChecked(visible))

        # Toolbar: Help
        self._toolbarHelp = self.addToolBar(self.tr("Help Toolbar"))
        self._toolbarHelp.setObjectName("toolbarHelp")
        self._toolbarHelp.visibilityChanged.connect(lambda visible: self._actionToolbarHelp.setChecked(visible))


    def _updateActionsToolButtonStyle(self, toolButtonStyle):

        for action in self._actionsToolButtonStyle.actions():
            if Qt.ToolButtonStyle(action.data()) == toolButtonStyle:
                action.setChecked(True)
                self._onActionsToolButtonStyleTriggered(action)
                break


    def _onActionAboutTriggered(self):

        dialog = AboutDialog(self)
        dialog.open()


    def _onActionColophonTriggered(self):

        dialog = ColophonDialog(self)
        dialog.open()


    def _onActionPreferencesTriggered(self):

        dialog = PreferencesDialog(self)
        dialog.open()


    def _onActionsToolButtonStyleTriggered(self, actionToolButtonStyle):

        style = Qt.ToolButtonStyle(actionToolButtonStyle.data())

        self._toolbarApplication.setToolButtonStyle(style)
        self._toolbarFile.setToolButtonStyle(style)
        self._toolbarEdit.setToolButtonStyle(style)
        self._toolbarView.setToolButtonStyle(style)
        self._toolbarFormat.setToolButtonStyle(style)
        self._toolbarTools.setToolButtonStyle(style)
        self._toolbarAppearance.setToolButtonStyle(style)
        self._toolbarHelp.setToolButtonStyle(style)
