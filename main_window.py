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

from PySide2.QtCore import QByteArray, QSettings, QSize, Qt, Signal
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtWidgets import QAction, QActionGroup, QApplication, QMainWindow, QMenu, QMessageBox, QTabWidget

from about_dialog import AboutDialog
from colophon_dialog import ColophonDialog
from confirmation_dialog import ConfirmationDialog
from mdi_area import MdiArea
from mdi_document import MdiDocument
from mdi_window import MdiWindow
from message_box import MessageBox
from preferences_dialog import PreferencesDialog

import icons_rc


class MainWindow(QMainWindow):

    documentCountChanged = Signal(int)


    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowIcon(QIcon(":/icons/apps/16/tabelo.svg"))

        self._documentsArea = MdiArea()
        self._documentsArea.setViewMode(MdiArea.TabbedView)
        self._documentsArea.setDocumentMode(True)
        self._documentsArea.setTabsClosable(True)
        self._documentsArea.setTabsMovable(True)
        self._documentsArea.subWindowActivated.connect(self._documentActivated)
        self.setCentralWidget(self._documentsArea)

        self._setupActions()

        self._loadSettings()

        self._documentCreated()
        self._documentActivated(None)


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

        self._actionClose = QAction(self.tr("&Close"), self)
        self._actionClose.setObjectName("actionClose")
        self._actionClose.setIcon(QIcon.fromTheme("document-close", QIcon(":/icons/actions/16/document-close.svg")))
        self._actionClose.setShortcut(QKeySequence.Close)
        self._actionClose.setToolTip(self.tr("Close document"))
        self._actionClose.triggered.connect(self._documentsArea.closeActiveSubWindow)
        self.addAction(self._actionClose)

        self._actionCloseOther = QAction(self.tr("Close Ot&her"), self)
        self._actionCloseOther.setObjectName("actionCloseOther")
        self._actionCloseOther.setToolTip(self.tr("Close other open documents"))
        self._actionCloseOther.triggered.connect(self._slotCloseOther)

        self._actionCloseAll = QAction(self.tr("Clos&e All"), self)
        self._actionCloseAll.setObjectName("actionCloseAll")
        self._actionCloseAll.setToolTip(self.tr("Close all open documents"))
        self._actionCloseAll.triggered.connect(self._slotCloseAll)

        menuFile = self.menuBar().addMenu(self.tr("&File"))
        menuFile.setObjectName("menuFile")
        menuFile.addAction(self._actionNew)
        menuFile.addSeparator()
        menuFile.addAction(self._actionClose)
        menuFile.addAction(self._actionCloseOther)
        menuFile.addAction(self._actionCloseAll)

        self._toolbarFile = self.addToolBar(self.tr("File Toolbar"))
        self._toolbarFile.setObjectName("toolbarFile")
        self._toolbarFile.addAction(self._actionNew)
        self._toolbarFile.addSeparator()
        self._toolbarFile.addAction(self._actionClose)


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

        self._actionShowMenubar = QAction(self)
        self._actionShowMenubar.setObjectName("actionShowMenubar")
        self._actionShowMenubar.setCheckable(True)
        self._actionShowMenubar.setChecked(True)
        self._actionShowMenubar.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_M))
        self._actionShowMenubar.toggled.connect(self._slotShowMenubar)
        self.addAction(self._actionShowMenubar)
        self._updateActionShowMenubar()

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

        actionToolButtonSizeSmall = QAction(self.tr("&Small (16x16)"), self)
        actionToolButtonSizeSmall.setObjectName("actionToolButtonSizeSmall")
        actionToolButtonSizeSmall.setCheckable(True)
        actionToolButtonSizeSmall.setToolTip(self.tr("Show icons in small size"))
        actionToolButtonSizeSmall.setData(16)

        actionToolButtonSizeMedium = QAction(self.tr("&Medium (22x22)"), self)
        actionToolButtonSizeMedium.setObjectName("actionToolButtonSizeMedium")
        actionToolButtonSizeMedium.setCheckable(True)
        actionToolButtonSizeMedium.setToolTip(self.tr("Show icons in medium size"))
        actionToolButtonSizeMedium.setData(22)

        actionToolButtonSizeLarge = QAction(self.tr("&Large (32x32)"), self)
        actionToolButtonSizeLarge.setObjectName("actionToolButtonSizeLarge")
        actionToolButtonSizeLarge.setCheckable(True)
        actionToolButtonSizeLarge.setToolTip(self.tr("Show icons in large size"))
        actionToolButtonSizeLarge.setData(32)

        actionToolButtonSizeHuge = QAction(self.tr("&Huge (48x48)"), self)
        actionToolButtonSizeHuge.setObjectName("actionToolButtonSizeHuge")
        actionToolButtonSizeHuge.setCheckable(True)
        actionToolButtonSizeHuge.setToolTip(self.tr("Show icons in huge size"))
        actionToolButtonSizeHuge.setData(48)

        actionToolButtonSizeDefault = QAction(self.tr("De&fault"), self)
        actionToolButtonSizeDefault.setObjectName("actionToolButtonSizeDefault")
        actionToolButtonSizeDefault.setCheckable(True)
        actionToolButtonSizeDefault.setToolTip(self.tr("Show icons in theme size"))
        actionToolButtonSizeDefault.setData(0)

        self._actionsToolButtonSize = QActionGroup(self)
        self._actionsToolButtonSize.setObjectName("actionsToolButtonSize")
        self._actionsToolButtonSize.addAction(actionToolButtonSizeSmall)
        self._actionsToolButtonSize.addAction(actionToolButtonSizeMedium)
        self._actionsToolButtonSize.addAction(actionToolButtonSizeLarge)
        self._actionsToolButtonSize.addAction(actionToolButtonSizeHuge)
        self._actionsToolButtonSize.addAction(actionToolButtonSizeDefault)
        self._actionsToolButtonSize.triggered.connect(self._slotToolButtonSize)

        self._actionShowDocumentTabs = QAction(self)
        self._actionShowDocumentTabs.setObjectName("actionShowDocumentbar")
        self._actionShowDocumentTabs.setCheckable(True)
        self._actionShowDocumentTabs.setChecked(True)
        self._actionShowDocumentTabs.toggled.connect(self._slotShowDocumentTabs)
        self._updateActionShowDocumentTabs()

        actionDocumentTabPositionTop = QAction(self.tr("&Top"), self)
        actionDocumentTabPositionTop.setObjectName("actionDocumentTabPositionTop")
        actionDocumentTabPositionTop.setCheckable(True)
        actionDocumentTabPositionTop.setToolTip(self.tr("Show tabs above the documents"))
        actionDocumentTabPositionTop.setData(QTabWidget.North)

        actionDocumentTabPositionBottom = QAction(self.tr("&Bottom"), self)
        actionDocumentTabPositionBottom.setObjectName("actionDocumentTabPositionBottom")
        actionDocumentTabPositionBottom.setCheckable(True)
        actionDocumentTabPositionBottom.setToolTip(self.tr("Show tabs below the documents"))
        actionDocumentTabPositionBottom.setData(QTabWidget.South)

        self._actionsDocumentTabPosition = QActionGroup(self)
        self._actionsDocumentTabPosition.setObjectName("actionsDocumentTabPosition")
        self._actionsDocumentTabPosition.addAction(actionDocumentTabPositionTop)
        self._actionsDocumentTabPosition.addAction(actionDocumentTabPositionBottom)
        self._actionsDocumentTabPosition.triggered.connect(self._slotDocumentTabPosition)

        self._actionDocumentTabAutoHide = QAction(self.tr("&Auto Hide"), self)
        self._actionDocumentTabAutoHide.setObjectName("actionDocumentTabAutoHide")
        self._actionDocumentTabAutoHide.setCheckable(True)
        self._actionDocumentTabAutoHide.setToolTip(self.tr("Tabs are automatically hidden if they contain only 1 document"))
        self._actionDocumentTabAutoHide.toggled.connect(self._documentsArea.setTabBarAutoHide)

        self._actionShowStatusbar = QAction(self)
        self._actionShowStatusbar.setObjectName("actionShowStatusbar")
        self._actionShowStatusbar.setCheckable(True)
        self._actionShowStatusbar.setChecked(True)
        self._actionShowStatusbar.toggled.connect(self._slotShowStatusbar)
        self._updateActionShowStatusbar()

        self._actionFullScreen = QAction(self)
        self._actionFullScreen.setObjectName("actionFullScreen")
        self._actionFullScreen.setCheckable(True)
        self._actionFullScreen.setShortcuts([QKeySequence(Qt.Key_F11), QKeySequence.FullScreen])
        self._actionFullScreen.toggled.connect(self._slotFullScreen)
        self.addAction(self._actionFullScreen)
        self._updateActionFullScreen()

        menuToolButtonStyle = QMenu(self.tr("Tool Button St&yle"), self)
        menuToolButtonStyle.setObjectName("menuToolButtonStyle")
        menuToolButtonStyle.addSection(self.tr("Text Position"))
        menuToolButtonStyle.addActions(self._actionsToolButtonStyle.actions())
        menuToolButtonStyle.addSection(self.tr("Icon Size"))
        menuToolButtonStyle.addActions(self._actionsToolButtonSize.actions())

        menuDocumentTabPosition = QMenu(self.tr("Document Tab &Position"), self)
        menuDocumentTabPosition.setObjectName("menuDocumentTabPosition")
        menuDocumentTabPosition.addSection(self.tr("Position"))
        menuDocumentTabPosition.addActions(self._actionsDocumentTabPosition.actions())
        menuDocumentTabPosition.addSection(self.tr("Behavior"))
        menuDocumentTabPosition.addAction(self._actionDocumentTabAutoHide)
        self._actionShowDocumentTabs.toggled.connect(menuDocumentTabPosition.setEnabled)

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
        menuAppearance.addAction(self._actionShowDocumentTabs)
        menuAppearance.addMenu(menuDocumentTabPosition)
        menuAppearance.addSeparator()
        menuAppearance.addAction(self._actionShowStatusbar)
        menuAppearance.addSeparator()
        menuAppearance.addAction(self._actionFullScreen)

        self._toolbarAppearance = self.addToolBar(self.tr("Appearance Toolbar"))
        self._toolbarAppearance.setObjectName("toolbarAppearance")
        self._toolbarAppearance.addAction(self._actionShowMenubar)
        self._toolbarAppearance.addAction(self._actionShowDocumentTabs)
        self._toolbarAppearance.addAction(self._actionShowStatusbar)
        self._toolbarAppearance.addSeparator()
        self._toolbarAppearance.addAction(self._actionFullScreen)


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
                action.trigger()
                break


    def _updateActionsToolButtonSize(self, pixel):

        for action in self._actionsToolButtonSize.actions():
            if action.data() == pixel:
                action.trigger()
                break


    def _updateActionsDocumentTabPosition(self, position):

        for action in self._actionsDocumentTabPosition.actions():
            if QTabWidget.TabPosition(action.data()) == position:
                action.trigger()
                break


    def _updateActionShowMenubar(self):

        if not self._actionShowMenubar.isChecked():
            self._actionShowMenubar.setText(self.tr("Show &Menubar"))
            self._actionShowMenubar.setIcon(QIcon.fromTheme("show-menubar", QIcon(":/icons/actions/16/show-menubar.svg")))
            self._actionShowMenubar.setIconText(self.tr("Menubar"))
            self._actionShowMenubar.setToolTip(self.tr("Show the menubar"))
        else:
            self._actionShowMenubar.setText(self.tr("Hide &Menubar"))
            self._actionShowMenubar.setIcon(QIcon.fromTheme("hide-menubar", QIcon(":/icons/actions/16/hide-menubar.svg")))
            self._actionShowMenubar.setIconText(self.tr("Menubar"))
            self._actionShowMenubar.setToolTip(self.tr("Hide the menubar"))


    def _updateActionShowDocumentTabs(self):

        if not self._actionShowDocumentTabs.isChecked():
            self._actionShowDocumentTabs.setText(self.tr("Show &Document Tabs"))
            self._actionShowDocumentTabs.setIcon(QIcon.fromTheme("show-tabbar", QIcon(":/icons/actions/16/show-tabbar.svg")))
            self._actionShowDocumentTabs.setIconText(self.tr("Document Tabs"))
            self._actionShowDocumentTabs.setToolTip(self.tr("Show the document tabs"))
        else:
            self._actionShowDocumentTabs.setText(self.tr("Hide &Document Tabs"))
            self._actionShowDocumentTabs.setIcon(QIcon.fromTheme("hide-tabbar", QIcon(":/icons/actions/16/hide-tabbar.svg")))
            self._actionShowDocumentTabs.setIconText(self.tr("Document Tabs"))
            self._actionShowDocumentTabs.setToolTip(self.tr("Hide the document tabs"))


    def _updateActionShowStatusbar(self):

        if not self._actionShowStatusbar.isChecked():
            self._actionShowStatusbar.setText(self.tr("Show Stat&usbar"))
            self._actionShowStatusbar.setIcon(QIcon.fromTheme("show-statusbar", QIcon(":/icons/actions/16/show-statusbar.svg")))
            self._actionShowStatusbar.setIconText(self.tr("Statusbar"))
            self._actionShowStatusbar.setToolTip(self.tr("Show the statusbar"))
        else:
            self._actionShowStatusbar.setText(self.tr("Hide Stat&usbar"))
            self._actionShowStatusbar.setIcon(QIcon.fromTheme("hide-statusbar", QIcon(":/icons/actions/16/hide-statusbar.svg")))
            self._actionShowStatusbar.setIconText(self.tr("Statusbar"))
            self._actionShowStatusbar.setToolTip(self.tr("Hide the statusbar"))


    def _updateActionFullScreen(self):

        if not self._actionFullScreen.isChecked():
            self._actionFullScreen.setText(self.tr("Full &Screen Mode"))
            self._actionFullScreen.setIcon(QIcon.fromTheme("view-fullscreen", QIcon(":/icons/actions/16/view-fullscreen.svg")))
            self._actionFullScreen.setIconText(self.tr("Full Screen"))
            self._actionFullScreen.setToolTip(self.tr("Display the window in full screen"))
        else:
            self._actionFullScreen.setText(self.tr("Exit Full &Screen Mode"))
            self._actionFullScreen.setIcon(QIcon.fromTheme("view-restore", QIcon(":/icons/actions/16/view-restore.svg")))
            self._actionFullScreen.setIconText(self.tr("Full Screen"))
            self._actionFullScreen.setToolTip(self.tr("Exit full screen mode"))


    def _enableActions(self, enabled):

        self._actionClose.setEnabled(enabled)
        self._actionCloseAll.setEnabled(enabled)


    def _enableActionCloseOther(self, enabled):

        self._actionCloseOther.setEnabled(enabled)


    def _loadSettings(self):

        settings = QSettings()


        #
        # Application properties

        # Geometry
        geometry = settings.value("Application/Geometry", QByteArray())
        if not geometry.isEmpty():
            self.restoreGeometry(geometry)
        else:
            # Default: Center window
            availableGeometry = self.screen().availableGeometry()
            self.resize(availableGeometry.width() * 2/3, availableGeometry.height() * 2/3)
            self.move((availableGeometry.width() - self.width()) / 2, (availableGeometry.height() - self.height()) / 2)

        # State
        state = settings.value("Application/State", QByteArray())
        if not state.isEmpty():
            self.restoreState(state)

            if self.isFullScreen():
                self._actionFullScreen.toggle()
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

        # Show Menubar
        visible = settings.value("Application/ShowMenubar", True, type=bool)
        if not visible:  # Default: Visible
            self._actionShowMenubar.toggle()

        # Show Statusbar
        visible = settings.value("Application/ShowStatusbar", True, type=bool)
        if not visible:  # Default: Visible
            self._actionShowStatusbar.toggle()

        # Tool Button Style
        value = settings.value("Application/ToolButtonStyle", Qt.ToolButtonFollowStyle, type=int)
        style = Qt.ToolButtonStyle(value) if Qt.ToolButtonStyle(value) in Qt.ToolButtonStyle.values.values() else Qt.ToolButtonFollowStyle
        self._updateActionsToolButtonStyle(style)

        # Tool Button Size
        value = settings.value("Application/ToolButtonSize", 0, type=int)
        pixel = value if value in [0, 16, 22, 32, 48] else 0
        self._updateActionsToolButtonSize(pixel)

        # Show Document Tabs
        visible = settings.value("Application/ShowDocumentTabs", True, type=bool)
        if not visible:  # Default: Visible
            self._actionShowDocumentTabs.toggle()

        # Document Tab Position
        value = settings.value("Application/DocumentTabPosition", QTabWidget.North, type=int)
        position = QTabWidget.TabPosition(value) if QTabWidget.TabPosition(value) in [QTabWidget.North, QTabWidget.South] else QTabWidget.North
        self._updateActionsDocumentTabPosition(position)

        # Document Tab Auto Hide
        checked = settings.value("Application/DocumentTabAutoHide", False, type=bool)
        if checked:  # Default: Unchecked
            self._actionDocumentTabAutoHide.toggle()


    def _saveSettings(self):

        settings = QSettings()


        #
        # Application properties

        geometry = self.saveGeometry()
        settings.setValue("Application/Geometry", geometry)

        state = self.saveState()
        settings.setValue("Application/State", state)

        visible = self._actionShowMenubar.isChecked()
        settings.setValue("Application/ShowMenubar", visible)

        visible = self._actionShowStatusbar.isChecked()
        settings.setValue("Application/ShowStatusbar", visible)

        value = self._actionsToolButtonStyle.checkedAction().data()
        settings.setValue("Application/ToolButtonStyle", value)

        value = self._actionsToolButtonSize.checkedAction().data()
        settings.setValue("Application/ToolButtonSize", value)

        visible = self._actionShowDocumentTabs.isChecked()
        settings.setValue("Application/ShowDocumentTabs", visible)

        value = self._actionsDocumentTabPosition.checkedAction().data()
        settings.setValue("Application/DocumentTabPosition", value)

        checked = self._actionDocumentTabAutoHide.isChecked()
        settings.setValue("Application/DocumentTabAutoHide", checked)


    def closeEvent(self, event):

        if self._documentsArea.subWindowCount() >= 1:

            title = self.tr("Quit the application")
            text = self.tr("This will close all open documents and quit the application.\n"
                           "Are you sure you want to continue?")
            buttons = QMessageBox.Yes | QMessageBox.Cancel
            default = QMessageBox.Yes

            if ConfirmationDialog.warning(self, title, text, buttons, default, "ConfirmQuit") is QMessageBox.Cancel:
                event.ignore()
                return

            self._documentsArea.closeAllSubWindows()

        self._saveSettings()

        event.accept()


    def _createDocument(self):

        document = MdiDocument()

        docWindow = MdiWindow()
        docWindow.setWidget(document)
        self._documentsArea.addSubWindow(docWindow)

        document.urlChanged.connect(docWindow.documentUrlChanged)

        docWindow.closeOtherSubWindows.connect(self._documentsArea.closeOtherSubWindows)
        docWindow.destroyed.connect(self._documentDestroyed)

        self.documentCountChanged.connect(docWindow.subWindowCountChanged)

        # Initialize
        document.initUrl()

        return document


    def _documentCreated(self):

        count = self._documentsArea.subWindowCount()

        self._enableActionCloseOther(count >= 2)

        self.documentCountChanged.emit(count)


    def _documentActivated(self, subWindow):

        self._enableActions(subWindow is not None)


    def _documentDestroyed(self):

        count = self._documentsArea.subWindowCount()

        self._enableActionCloseOther(count >= 2)

        self.documentCountChanged.emit(count)


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

        self._documentCreated()


    def _slotCloseOther(self):

        if self._documentsArea.subWindowCount() >= 2:

            title = self.tr("Close all documents beside current one")
            text = self.tr("This will close all open documents beside the current one.\n"
                           "Are you sure you want to continue?")
            buttons = QMessageBox.Yes | QMessageBox.Cancel
            default = QMessageBox.Yes

            if ConfirmationDialog.warning(self, title, text, buttons, default, "ConfirmCloseOther") is not QMessageBox.Cancel:
                self._documentsArea.closeOtherSubWindows(self._documentsArea.activeSubWindow())


    def _slotCloseAll(self):

        if self._documentsArea.subWindowCount() >= 1:

            title = self.tr("Close all documents")
            text = self.tr("This will close all open documents.\n"
                           "Are you sure you want to continue?")
            buttons = QMessageBox.Yes | QMessageBox.Cancel
            default = QMessageBox.Yes

            if ConfirmationDialog.warning(self, title, text, buttons, default, "ConfirmCloseAll") is not QMessageBox.Cancel:
                self._documentsArea.closeAllSubWindows()


    def _slotShowMenubar(self, checked):

        self.menuBar().setVisible(checked)

        self._updateActionShowMenubar()


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


    def _slotToolButtonSize(self, action):

        pixel = action.data()
        size = QSize(pixel, pixel) if pixel else QSize(-1, -1)

        self._toolbarApplication.setIconSize(size)
        self._toolbarFile.setIconSize(size)
        self._toolbarEdit.setIconSize(size)
        self._toolbarView.setIconSize(size)
        self._toolbarFormat.setIconSize(size)
        self._toolbarTools.setIconSize(size)
        self._toolbarAppearance.setIconSize(size)
        self._toolbarHelp.setIconSize(size)


    def _slotShowDocumentTabs(self, checked):

        self._documentsArea.setTabBarVisible(checked)

        self._updateActionShowDocumentTabs()


    def _slotDocumentTabPosition(self, action):

        position = QTabWidget.TabPosition(action.data())

        self._documentsArea.setTabPosition(position)


    def _slotShowStatusbar(self, checked):

        self.statusBar().setVisible(checked)

        self._updateActionShowStatusbar()


    def _slotFullScreen(self, checked):

        if checked:
            self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        else:
            self.setWindowState(self.windowState() & ~Qt.WindowFullScreen)

        self._updateActionFullScreen()
