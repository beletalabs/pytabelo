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

from PySide2.QtCore import QByteArray, QSettings, Qt
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtWidgets import QAction, QActionGroup, QApplication, QMainWindow, QMenu

from about_dialog import AboutDialog
from colophon_dialog import ColophonDialog
from mdi_area import MdiArea
from mdi_document import MdiDocument
from preferences_dialog import PreferencesDialog

import icons_rc


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowIcon(QIcon(":/icons/apps/16/tabelo.svg"))

        self._documentsArea = MdiArea()
        self._documentsArea.setViewMode(MdiArea.TabbedView)
        self._documentsArea.setDocumentMode(True)
        self._documentsArea.setTabsClosable(True)
        self._documentsArea.setTabsMovable(True)
        self.setCentralWidget(self._documentsArea)

        self._setupActions()

        self._loadSettings()

        self._actionViewFullScreen.setChecked(self.isFullScreen())
        self._updateActionViewFullScreen()


    def closeEvent(self, event):

        if True:
            # Store application properties
            self._saveSettings()

            event.accept()
        else:
            event.ignore()


    def _setupActions(self):

        #
        # Application

        self._actionAbout = QAction(self.tr("&About {0}").format(QApplication.applicationName()), self)
        self._actionAbout.setObjectName("actionAbout")
        self._actionAbout.setIcon(QIcon(":/icons/apps/16/tabelo.svg"))
        self._actionAbout.setIconText(self.tr("About"))
        self._actionAbout.setToolTip(self.tr("Brief description of the application"))
        self._actionAbout.setMenuRole(QAction.AboutRole)
        self._actionAbout.triggered.connect(self._slotAbout)

        self._actionColophon = QAction(self.tr("&Colophon"), self)
        self._actionColophon.setObjectName("actionColophon")
        self._actionColophon.setIcon(QIcon.fromTheme("help-about", QIcon(":/icons/actions/16/help-about.svg")))
        self._actionColophon.setToolTip(self.tr("Lengthy description of the application"))
        self._actionColophon.setMenuRole(QAction.ApplicationSpecificRole)
        self._actionColophon.triggered.connect(self._slotColophon)

        self._actionPreferences = QAction(self.tr("&Preferences..."), self)
        self._actionPreferences.setObjectName("actionPreferences")
        self._actionPreferences.setIcon(QIcon.fromTheme("configure", QIcon(":/icons/actions/16/configure.svg")))
        self._actionPreferences.setToolTip(self.tr("Customize the appearance and behavior of the application"))
        self._actionPreferences.setMenuRole(QAction.PreferencesRole)
        self._actionPreferences.triggered.connect(self._slotPreferences)

        self._actionQuit = QAction(self.tr("&Quit"), self)
        self._actionQuit.setObjectName("actionQuit")
        self._actionQuit.setIcon(QIcon.fromTheme("application-exit", QIcon(":/icons/actions/16/application-exit.svg")))
        self._actionQuit.setShortcut(QKeySequence.Quit)
        self._actionQuit.setToolTip(self.tr("Quit the application"))
        self._actionQuit.setMenuRole(QAction.QuitRole)
        self._actionQuit.triggered.connect(self.close)
        self.addAction(self._actionQuit)

        menuApplication = self.menuBar().addMenu(self.tr("&Application"))
        menuApplication.setObjectName("menuApplication")
        menuApplication.addAction(self._actionAbout)
        menuApplication.addAction(self._actionColophon)
        menuApplication.addSeparator()
        menuApplication.addAction(self._actionPreferences)
        menuApplication.addSeparator()
        menuApplication.addAction(self._actionQuit)

        self._toolbarApplication = self.addToolBar(self.tr("Application Toolbar"))
        self._toolbarApplication.setObjectName("toolbarApplication")
        self._toolbarApplication.addAction(self._actionAbout)
        self._toolbarApplication.addAction(self._actionPreferences)
        self._toolbarApplication.addSeparator()
        self._toolbarApplication.addAction(self._actionQuit)


        #
        # File

        self._actionNew = QAction(self.tr("&New"), self)
        self._actionNew.setObjectName("actionNew")
        self._actionNew.setIcon(QIcon.fromTheme("document-new", QIcon(":/icons/actions/16/document-new.svg")))
        self._actionNew.setShortcut(QKeySequence.New)
        self._actionNew.setToolTip(self.tr("Create new document"))
        self._actionNew.triggered.connect(self._slotNew)
        self.addAction(self._actionNew)

        menuFile = self.menuBar().addMenu(self.tr("&File"))
        menuFile.setObjectName("menuFile")
        menuFile.addAction(self._actionNew)

        self._toolbarFile = self.addToolBar(self.tr("File Toolbar"))
        self._toolbarFile.setObjectName("toolbarFile")
        self._toolbarFile.addAction(self._actionNew)


        #
        # Edit

        menuEdit = self.menuBar().addMenu(self.tr("&Edit"))
        menuEdit.setObjectName("menuEdit")

        self._toolbarEdit = self.addToolBar(self.tr("Edit Toolbar"))
        self._toolbarEdit.setObjectName("toolbarEdit")


        #
        # View

        menuView = self.menuBar().addMenu(self.tr("&View"))
        menuView.setObjectName("menuView")

        self._toolbarView = self.addToolBar(self.tr("View Toolbar"))
        self._toolbarView.setObjectName("toolbarView")


        #
        # Format

        menuFormat = self.menuBar().addMenu(self.tr("F&ormat"))
        menuFormat.setObjectName("menuFormat")

        self._toolbarFormat = self.addToolBar(self.tr("Format Toolbar"))
        self._toolbarFormat.setObjectName("toolbarFormat")


        #
        # Tools

        menuTools = self.menuBar().addMenu(self.tr("&Tools"))
        menuTools.setObjectName("menuTools")

        self._toolbarTools = self.addToolBar(self.tr("Tools Toolbar"))
        self._toolbarTools.setObjectName("toolbarTools")


        #
        # Appearance

        self._actionShowMenubar = QAction(self.tr("Show &Menubar"), self)
        self._actionShowMenubar.setObjectName("actionShowMenubar")
        self._actionShowMenubar.setCheckable(True)
        self._actionShowMenubar.setIcon(QIcon.fromTheme("show-menu", QIcon(":/icons/actions/16/show-menu.svg")))
        self._actionShowMenubar.setIconText("Menubar")
        self._actionShowMenubar.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_M))
        self._actionShowMenubar.setToolTip(self.tr("Show the menubar"))
        self._actionShowMenubar.toggled.connect(self.menuBar().setVisible)
        self.addAction(self._actionShowMenubar)

        self._actionShowToolbarApplication = QAction(self.tr("Show &Application Toolbar"), self)
        self._actionShowToolbarApplication.setObjectName("actionShowToolbarApplication")
        self._actionShowToolbarApplication.setCheckable(True)
        self._actionShowToolbarApplication.setToolTip(self.tr("Show the Application toolbar"))

        self._actionShowToolbarFile = QAction(self.tr("Show &File Toolbar"), self)
        self._actionShowToolbarFile.setObjectName("actionShowToolbarFile")
        self._actionShowToolbarFile.setCheckable(True)
        self._actionShowToolbarFile.setToolTip(self.tr("Show the File toolbar"))

        self._actionShowToolbarEdit = QAction(self.tr("Show &Edit Toolbar"), self)
        self._actionShowToolbarEdit.setObjectName("actionShowToolbarEdit")
        self._actionShowToolbarEdit.setCheckable(True)
        self._actionShowToolbarEdit.setToolTip(self.tr("Show the Edit toolbar"))

        self._actionShowToolbarView = QAction(self.tr("Show &View Toolbar"), self)
        self._actionShowToolbarView.setObjectName("actionShowToolbarView")
        self._actionShowToolbarView.setCheckable(True)
        self._actionShowToolbarView.setToolTip(self.tr("Show the View toolbar"))

        self._actionShowToolbarFormat = QAction(self.tr("Show F&ormat Toolbar"), self)
        self._actionShowToolbarFormat.setObjectName("actionShowToolbarFormat")
        self._actionShowToolbarFormat.setCheckable(True)
        self._actionShowToolbarFormat.setToolTip(self.tr("Show the Format toolbar"))

        self._actionShowToolbarTools = QAction(self.tr("Show &Tools Toolbar"), self)
        self._actionShowToolbarTools.setObjectName("actionShowToolbarTools")
        self._actionShowToolbarTools.setCheckable(True)
        self._actionShowToolbarTools.setToolTip(self.tr("Show the Tools toolbar"))

        self._actionShowToolbarAppearance = QAction(self.tr("Show Appea&rance Toolbar"), self)
        self._actionShowToolbarAppearance.setObjectName("actionShowToolbarAppearance")
        self._actionShowToolbarAppearance.setCheckable(True)
        self._actionShowToolbarAppearance.setToolTip(self.tr("Show the Appearance toolbar"))

        self._actionShowToolbarHelp = QAction(self.tr("Show &Help Toolbar"), self)
        self._actionShowToolbarHelp.setObjectName("actionShowToolbarHelp")
        self._actionShowToolbarHelp.setCheckable(True)
        self._actionShowToolbarHelp.setToolTip(self.tr("Show the Help toolbar"))

        actionToolButtonStyleIconOnly = QAction(self.tr("&Icon Only"), self)
        actionToolButtonStyleIconOnly.setObjectName("actionToolButtonStyleIconOnly")
        actionToolButtonStyleIconOnly.setCheckable(True)
        actionToolButtonStyleIconOnly.setToolTip(self.tr("Only display the icon"))
        actionToolButtonStyleIconOnly.setData(Qt.ToolButtonIconOnly)

        actionToolButtonStyleTextOnly = QAction(self.tr("&Text Only"), self)
        actionToolButtonStyleTextOnly.setObjectName("actionToolButtonStyleTextOnly")
        actionToolButtonStyleTextOnly.setCheckable(True)
        actionToolButtonStyleTextOnly.setToolTip(self.tr("Only display the text"))
        actionToolButtonStyleTextOnly.setData(Qt.ToolButtonTextOnly)

        actionToolButtonStyleTextBesideIcon = QAction(self.tr("Text &Beside Icon"), self)
        actionToolButtonStyleTextBesideIcon.setObjectName("actionToolButtonStyleTextBesideIcon")
        actionToolButtonStyleTextBesideIcon.setCheckable(True)
        actionToolButtonStyleTextBesideIcon.setToolTip(self.tr("The text appears beside the icon"))
        actionToolButtonStyleTextBesideIcon.setData(Qt.ToolButtonTextBesideIcon)

        actionToolButtonStyleTextUnderIcon = QAction(self.tr("Text &Under Icon"), self)
        actionToolButtonStyleTextUnderIcon.setObjectName("actionToolButtonStyleTextUnderIcon")
        actionToolButtonStyleTextUnderIcon.setCheckable(True)
        actionToolButtonStyleTextUnderIcon.setToolTip(self.tr("The text appears under the icon"))
        actionToolButtonStyleTextUnderIcon.setData(Qt.ToolButtonTextUnderIcon)

        actionToolButtonStyleDefault = QAction(self.tr("&Default"), self)
        actionToolButtonStyleDefault.setObjectName("actionToolButtonStyleDefault")
        actionToolButtonStyleDefault.setCheckable(True)
        actionToolButtonStyleDefault.setToolTip(self.tr("Follow the theme style"))
        actionToolButtonStyleDefault.setData(Qt.ToolButtonFollowStyle)

        self._actionsToolButtonStyle = QActionGroup(self)
        self._actionsToolButtonStyle.setObjectName("actionsToolButtonStyle")
        self._actionsToolButtonStyle.addAction(actionToolButtonStyleIconOnly)
        self._actionsToolButtonStyle.addAction(actionToolButtonStyleTextOnly)
        self._actionsToolButtonStyle.addAction(actionToolButtonStyleTextBesideIcon)
        self._actionsToolButtonStyle.addAction(actionToolButtonStyleTextUnderIcon)
        self._actionsToolButtonStyle.addAction(actionToolButtonStyleDefault)
        self._actionsToolButtonStyle.triggered.connect(self._slotToolButtonStyle)

        self._actionShowStatusbar = QAction(self.tr("Show Stat&usbar"), self)
        self._actionShowStatusbar.setObjectName("actionShowStatusbar")
        self._actionShowStatusbar.setCheckable(True)
        self._actionShowStatusbar.setToolTip(self.tr("Show the Statusbar"))
        self._actionShowStatusbar.toggled.connect(self.statusBar().setVisible)

        self._actionViewFullScreen = QAction(self)
        self._actionViewFullScreen.setObjectName("actionViewFullScreen")
        self._actionViewFullScreen.setCheckable(True)
        self._actionViewFullScreen.setShortcuts([QKeySequence(Qt.Key_F11), QKeySequence.FullScreen])
        self._actionViewFullScreen.toggled.connect(self._slotViewFullScreen)
        self.addAction(self._actionViewFullScreen)

        menuToolButtonStyle = QMenu(self.tr("Tool Button St&yle"), self)
        menuToolButtonStyle.setObjectName("menuToolButtonStyle")
        menuToolButtonStyle.addSection(self.tr("Text Position"))
        menuToolButtonStyle.addActions(self._actionsToolButtonStyle.actions())

        menuAppearance = self.menuBar().addMenu(self.tr("Appea&rance"))
        menuAppearance.setObjectName("menuAppearance")
        menuAppearance.addAction(self._actionShowMenubar)
        menuAppearance.addSeparator()
        menuAppearance.addAction(self._actionShowToolbarApplication)
        menuAppearance.addAction(self._actionShowToolbarFile)
        menuAppearance.addAction(self._actionShowToolbarEdit)
        menuAppearance.addAction(self._actionShowToolbarView)
        menuAppearance.addAction(self._actionShowToolbarFormat)
        menuAppearance.addAction(self._actionShowToolbarTools)
        menuAppearance.addAction(self._actionShowToolbarAppearance)
        menuAppearance.addAction(self._actionShowToolbarHelp)
        menuAppearance.addMenu(menuToolButtonStyle)
        menuAppearance.addSeparator()
        menuAppearance.addAction(self._actionShowStatusbar)
        menuAppearance.addSeparator()
        menuAppearance.addAction(self._actionViewFullScreen)

        self._toolbarAppearance = self.addToolBar(self.tr("Appearance Toolbar"))
        self._toolbarAppearance.setObjectName("toolbarAppearance")
        self._toolbarAppearance.addAction(self._actionShowMenubar)
        self._toolbarAppearance.addSeparator()
        self._toolbarAppearance.addAction(self._actionViewFullScreen)


        #
        # Help

        menuHelp = self.menuBar().addMenu(self.tr("&Help"))
        menuHelp.setObjectName("menuHelp")

        self._toolbarHelp = self.addToolBar(self.tr("Help Toolbar"))
        self._toolbarHelp.setObjectName("toolbarHelp")


        # Connect toolbars with the corresponding actions
        self._toolbarApplication.visibilityChanged.connect(self._actionShowToolbarApplication.setChecked)
        self._actionShowToolbarApplication.toggled.connect(self._toolbarApplication.setVisible)
        self._toolbarFile.visibilityChanged.connect(self._actionShowToolbarFile.setChecked)
        self._actionShowToolbarFile.toggled.connect(self._toolbarFile.setVisible)
        self._toolbarEdit.visibilityChanged.connect(self._actionShowToolbarEdit.setChecked)
        self._actionShowToolbarEdit.toggled.connect(self._toolbarEdit.setVisible)
        self._toolbarView.visibilityChanged.connect(self._actionShowToolbarView.setChecked)
        self._actionShowToolbarView.toggled.connect(self._toolbarView.setVisible)
        self._toolbarFormat.visibilityChanged.connect(self._actionShowToolbarFormat.setChecked)
        self._actionShowToolbarFormat.toggled.connect(self._toolbarFormat.setVisible)
        self._toolbarTools.visibilityChanged.connect(self._actionShowToolbarTools.setChecked)
        self._actionShowToolbarTools.toggled.connect(self._toolbarTools.setVisible)
        self._toolbarAppearance.visibilityChanged.connect(self._actionShowToolbarAppearance.setChecked)
        self._actionShowToolbarAppearance.toggled.connect(self._toolbarAppearance.setVisible)
        self._toolbarHelp.visibilityChanged.connect(self._actionShowToolbarHelp.setChecked)
        self._actionShowToolbarHelp.toggled.connect(self._toolbarHelp.setVisible)


        #
        # Statusbar

        self.statusBar().showMessage(self.tr("Ready"), 3000)


    def _updateActionsToolButtonStyle(self, style):

        for action in self._actionsToolButtonStyle.actions():
            if Qt.ToolButtonStyle(action.data()) == style:
                action.setChecked(True)
                self._slotToolButtonStyle(action)
                break


    def _updateActionViewFullScreen(self):

        if not self._actionViewFullScreen.isChecked():
            self._actionViewFullScreen.setText(self.tr("Full &Screen Mode"))
            self._actionViewFullScreen.setIcon(QIcon.fromTheme("view-fullscreen", QIcon(":/icons/actions/16/view-fullscreen.svg")))
            self._actionViewFullScreen.setIconText(self.tr("Full Screen"))
            self._actionViewFullScreen.setToolTip(self.tr("Display the window in full screen"))
        else:
            self._actionViewFullScreen.setText(self.tr("Exit Full &Screen Mode"))
            self._actionViewFullScreen.setIcon(QIcon.fromTheme("view-restore", QIcon(":/icons/actions/16/view-restore.svg")))
            self._actionViewFullScreen.setIconText(self.tr("Full Screen"))
            self._actionViewFullScreen.setToolTip(self.tr("Exit full screen mode"))


    def _loadSettings(self):

        settings = QSettings()


        #
        # Application properties

        geometry = settings.value("Application/Geometry", QByteArray())
        if not geometry.isEmpty():
            self.restoreGeometry(geometry)
        else:
            # Default: Center window
            availableGeometry = self.screen().availableGeometry()
            self.resize(availableGeometry.width() * 2/3, availableGeometry.height() * 2/3)
            self.move((availableGeometry.width() - self.width()) / 2, (availableGeometry.height() - self.height()) / 2)

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

        visible = settings.value("Application/ShowMenubar", True, type=bool)
        self.menuBar().setVisible(visible)
        self._actionShowMenubar.setChecked(visible)

        visible = settings.value("Application/ShowStatusbar", True, type=bool)
        self.statusBar().setVisible(visible)
        self._actionShowStatusbar.setChecked(visible)

        style = settings.value("Application/ToolButtonStyle", Qt.ToolButtonFollowStyle, type=int)
        self._updateActionsToolButtonStyle(Qt.ToolButtonStyle(style))


    def _saveSettings(self):

        settings = QSettings()


        #
        # Application properties

        geometry = self.saveGeometry()
        settings.setValue("Application/Geometry", geometry)

        state = self.saveState()
        settings.setValue("Application/State", state)

        visible = self.menuBar().isVisible()
        settings.setValue("Application/ShowMenubar", visible)

        visible = self.statusBar().isVisible()
        settings.setValue("Application/ShowStatusbar", visible)

        # Application property: Tool Button Style
        style = self._actionsToolButtonStyle.checkedAction().data()
        settings.setValue("Application/ToolButtonStyle", style)


    def _createDocument(self):

        document = MdiDocument()

        subWindow = self._documentsArea.addSubWindow(document)
        subWindow.setWindowIcon(QIcon())

        return document


    def _slotAbout(self):

        dialog = AboutDialog(self)
        dialog.open()


    def _slotColophon(self):

        dialog = ColophonDialog(self)
        dialog.open()


    def _slotPreferences(self):

        dialog = PreferencesDialog(self)
        dialog.open()


    def _slotNew(self):

        document = self._createDocument()
        document.show()


    def _slotToolButtonStyle(self, action):

        style = Qt.ToolButtonStyle(action.data())

        self._toolbarApplication.setToolButtonStyle(style)
        self._toolbarFile.setToolButtonStyle(style)
        self._toolbarEdit.setToolButtonStyle(style)
        self._toolbarView.setToolButtonStyle(style)
        self._toolbarFormat.setToolButtonStyle(style)
        self._toolbarTools.setToolButtonStyle(style)
        self._toolbarAppearance.setToolButtonStyle(style)
        self._toolbarHelp.setToolButtonStyle(style)


    def _slotViewFullScreen(self, checked):

        if checked:
            self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        else:
            self.setWindowState(self.windowState() & ~Qt.WindowFullScreen)

        self._updateActionViewFullScreen()
