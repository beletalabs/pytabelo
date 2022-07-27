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

from PySide2.QtCore import QByteArray, QSettings, QSize, Qt, Signal
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtWidgets import QAction, QActionGroup, QApplication, QFileDialog, QMainWindow, QMenu, QMessageBox, QTabWidget

from about_dialog import AboutDialog
from colophon_dialog import ColophonDialog
from confirmation_dialog import ConfirmationDialog
from document_manager import DocumentManager
from document_widget import DocumentWidget
from document_window import DocumentWindow
from message_box import MessageBox
from preferences_dialog import PreferencesDialog

import icons_rc


class ApplicationWindow(QMainWindow):

    documentCountChanged = Signal(int)


    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowIcon(QIcon(":/icons/apps/16/tabelo.svg"))

        self._documentsArea = DocumentManager()
        self._documentsArea.setViewMode(DocumentManager.TabbedView)
        self._documentsArea.setDocumentMode(True)
        self._documentsArea.setTabsClosable(True)
        self._documentsArea.setTabsMovable(True)
        self.setCentralWidget(self._documentsArea)

        self._documentsArea.tabsVisibleChanged.connect(self._docManagerTabsVisibleChanged)
        self._documentsArea.tabsPositionChanged.connect(self._docManagerTabsPositionChanged)
        self._documentsArea.tabsAutoHideChanged.connect(self._docManagerTabsAutoHideChanged)
        self._documentsArea.subWindowActivated.connect(self._documentActivated)

        self._setupActions()
        self._loadSettings()

        self._documentsArea.initTabsVisible()
        self._documentsArea.initTabsPosition()
        self._documentsArea.initTabsAutoHide()

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

        self._actionOpen = QAction(self.tr("&Open..."), self)
        self._actionOpen.setObjectName("actionOpen")
        self._actionOpen.setIcon(QIcon.fromTheme("document-open", QIcon(":/icons/actions/16/document-open.svg")))
        self._actionOpen.setShortcut(QKeySequence.Open)
        self._actionOpen.setToolTip(self.tr("Open an existing document"))
        self._actionOpen.triggered.connect(self._slotOpen)
        self.addAction(self._actionOpen)

        self._actionCopyPath = QAction(self.tr("Cop&y Path"), self)
        self._actionCopyPath.setObjectName("actionCopyPath")
        self._actionCopyPath.setIcon(QIcon.fromTheme("edit-copy-path", QIcon(":/icons/actions/16/edit-copy-path.svg")))
        self._actionCopyPath.setToolTip(self.tr("Copy document path to clipboard"))
        self._actionCopyPath.triggered.connect(self._slotCopyPath)

        self._actionCopyFilename = QAction(self.tr("Copy &Filename"), self)
        self._actionCopyFilename.setObjectName("actionCopyFilename")
        self._actionCopyFilename.setIcon(QIcon.fromTheme("edit-copy-path", QIcon(":/icons/actions/16/edit-copy-path.svg")))
        self._actionCopyFilename.setToolTip(self.tr("Copy document filename to clipboard"))
        self._actionCopyFilename.triggered.connect(self._slotCopyFilename)

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
        menuFile.addAction(self._actionOpen)
        menuFile.addSeparator()
        menuFile.addAction(self._actionCopyPath)
        menuFile.addAction(self._actionCopyFilename)
        menuFile.addSeparator()
        menuFile.addAction(self._actionClose)
        menuFile.addAction(self._actionCloseOther)
        menuFile.addAction(self._actionCloseAll)

        self._toolbarFile = self.addToolBar(self.tr("File Toolbar"))
        self._toolbarFile.setObjectName("toolbarFile")
        self._toolbarFile.addAction(self._actionNew)
        self._toolbarFile.addAction(self._actionOpen)
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

        self._actionShowPath = QAction(self.tr("Show &Path in Titlebar"), self)
        self._actionShowPath.setObjectName("actionShowPath")
        self._actionShowPath.setCheckable(True)
        self._actionShowPath.setChecked(True)
        self._actionShowPath.setIcon(QIcon.fromTheme("show-path", QIcon(":/icons/actions/16/show-path.svg")))
        self._actionShowPath.setIconText(self.tr("Path"))
        self._actionShowPath.setToolTip(self.tr("Show document path in the window caption"))
        self._actionShowPath.toggled.connect(self._slotShowPath)

        self._actionShowMenubar = QAction(self.tr("Show &Menubar"), self)
        self._actionShowMenubar.setObjectName("actionShowMenubar")
        self._actionShowMenubar.setCheckable(True)
        self._actionShowMenubar.setChecked(True)
        self._actionShowMenubar.setIcon(QIcon.fromTheme("show-menubar", QIcon(":/icons/actions/16/show-menubar.svg")))
        self._actionShowMenubar.setIconText(self.tr("Menubar"))
        self._actionShowMenubar.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_M))
        self._actionShowMenubar.setToolTip(self.tr("Show the menubar"))
        self._actionShowMenubar.toggled.connect(self._slotShowMenubar)
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

        self._actionDocumentTabsVisible = QAction(self.tr("Show &Document Tabs"), self)
        self._actionDocumentTabsVisible.setObjectName("actionDocumentTabsVisible")
        self._actionDocumentTabsVisible.setCheckable(True)
        self._actionDocumentTabsVisible.setChecked(True)
        self._actionDocumentTabsVisible.setIcon(QIcon.fromTheme("show-tabbar", QIcon(":/icons/actions/16/show-tabbar.svg")))
        self._actionDocumentTabsVisible.setIconText(self.tr("Document Tabs"))
        self._actionDocumentTabsVisible.setToolTip(self.tr("Show the document tabs"))
        self._actionDocumentTabsVisible.toggled.connect(self._slotDocumentTabsVisible)

        actionDocumentTabsPositionTop = QAction(self.tr("&Top"), self)
        actionDocumentTabsPositionTop.setObjectName("actionDocumentTabsPositionTop")
        actionDocumentTabsPositionTop.setCheckable(True)
        actionDocumentTabsPositionTop.setToolTip(self.tr("Show tabs above the documents"))
        actionDocumentTabsPositionTop.setData(QTabWidget.North)

        actionDocumentTabsPositionBottom = QAction(self.tr("&Bottom"), self)
        actionDocumentTabsPositionBottom.setObjectName("actionDocumentTabsPositionBottom")
        actionDocumentTabsPositionBottom.setCheckable(True)
        actionDocumentTabsPositionBottom.setToolTip(self.tr("Show tabs below the documents"))
        actionDocumentTabsPositionBottom.setData(QTabWidget.South)

        self._actionsDocumentTabsPosition = QActionGroup(self)
        self._actionsDocumentTabsPosition.setObjectName("actionsDocumentTabsPosition")
        self._actionsDocumentTabsPosition.addAction(actionDocumentTabsPositionTop)
        self._actionsDocumentTabsPosition.addAction(actionDocumentTabsPositionBottom)
        self._actionsDocumentTabsPosition.triggered.connect(self._slotDocumentTabsPosition)

        self._actionDocumentTabsAutoHide = QAction(self.tr("&Auto Hide"), self)
        self._actionDocumentTabsAutoHide.setObjectName("actionDocumentTabsAutoHide")
        self._actionDocumentTabsAutoHide.setCheckable(True)
        self._actionDocumentTabsAutoHide.setToolTip(self.tr("Tabs are automatically hidden if they contain only 1 document"))
        self._actionDocumentTabsAutoHide.toggled.connect(self._slotDocumentTabsAutoHide)

        self._actionSheetTabsVisible = QAction(self.tr("Show &Sheet Tabs"), self)
        self._actionSheetTabsVisible.setObjectName("actionSheetTabsVisible")
        self._actionSheetTabsVisible.setCheckable(True)
        self._actionSheetTabsVisible.setChecked(True)
        self._actionSheetTabsVisible.setIcon(QIcon.fromTheme("show-tabbar-bottom", QIcon(":/icons/actions/16/show-tabbar-bottom.svg")))
        self._actionSheetTabsVisible.setIconText(self.tr("Sheet Tabs"))
        self._actionSheetTabsVisible.setToolTip(self.tr("Show the sheet tabs"))
        self._actionSheetTabsVisible.toggled.connect(self._slotSheetTabsVisible)

        actionSheetTabsPositionTop = QAction(self.tr("&Top"), self)
        actionSheetTabsPositionTop.setObjectName("actionSheetTabsPositionTop")
        actionSheetTabsPositionTop.setCheckable(True)
        actionSheetTabsPositionTop.setToolTip(self.tr("Show tabs above the sheets"))
        actionSheetTabsPositionTop.setData(QTabWidget.North)

        actionSheetTabsPositionBottom = QAction(self.tr("&Bottom"), self)
        actionSheetTabsPositionBottom.setObjectName("actionSheetTabsPositionBottom")
        actionSheetTabsPositionBottom.setCheckable(True)
        actionSheetTabsPositionBottom.setToolTip(self.tr("Show tabs below the sheets"))
        actionSheetTabsPositionBottom.setData(QTabWidget.South)

        self._actionsSheetTabsPosition = QActionGroup(self)
        self._actionsSheetTabsPosition.setObjectName("actionsSheetTabsPosition")
        self._actionsSheetTabsPosition.addAction(actionSheetTabsPositionTop)
        self._actionsSheetTabsPosition.addAction(actionSheetTabsPositionBottom)
        self._actionsSheetTabsPosition.triggered.connect(self._slotSheetTabsPosition)

        self._actionSheetTabsAutoHide = QAction(self.tr("&Auto Hide"), self)
        self._actionSheetTabsAutoHide.setObjectName("actionSheetTabsAutoHide")
        self._actionSheetTabsAutoHide.setCheckable(True)
        self._actionSheetTabsAutoHide.setChecked(True)
        self._actionSheetTabsAutoHide.setToolTip(self.tr("Tabs are automatically hidden if they contain only 1 sheet"))
        self._actionSheetTabsAutoHide.toggled.connect(self._slotSheetTabsAutoHide)

        self._actionShowStatusbar = QAction(self.tr("Show Stat&usbar"), self)
        self._actionShowStatusbar.setObjectName("actionShowStatusbar")
        self._actionShowStatusbar.setCheckable(True)
        self._actionShowStatusbar.setChecked(True)
        self._actionShowStatusbar.setIcon(QIcon.fromTheme("show-statusbar", QIcon(":/icons/actions/16/show-statusbar.svg")))
        self._actionShowStatusbar.setIconText(self.tr("Statusbar"))
        self._actionShowStatusbar.setToolTip(self.tr("Show the statusbar"))
        self._actionShowStatusbar.toggled.connect(self._slotShowStatusbar)

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

        menuDocumentTabsPosition = QMenu(self.tr("Document Tab &Position"), self)
        menuDocumentTabsPosition.setObjectName("menuDocumentTabsPosition")
        menuDocumentTabsPosition.addSection(self.tr("Position"))
        menuDocumentTabsPosition.addActions(self._actionsDocumentTabsPosition.actions())
        menuDocumentTabsPosition.addSection(self.tr("Behavior"))
        menuDocumentTabsPosition.addAction(self._actionDocumentTabsAutoHide)
        self._actionDocumentTabsVisible.toggled.connect(menuDocumentTabsPosition.setEnabled)

        menuSheetTabsPosition = QMenu(self.tr("Sheet Tab P&osition"), self)
        menuSheetTabsPosition.setObjectName("menuSheetTabsPosition")
        menuSheetTabsPosition.addSection(self.tr("Position"))
        menuSheetTabsPosition.addActions(self._actionsSheetTabsPosition.actions())
        menuSheetTabsPosition.addSection(self.tr("Behavior"))
        menuSheetTabsPosition.addAction(self._actionSheetTabsAutoHide)
        self._actionSheetTabsVisible.toggled.connect(menuSheetTabsPosition.setEnabled)

        menuAppearance = self.menuBar().addMenu(self.tr("Appea&rance"))
        menuAppearance.setObjectName("menuAppearance")
        menuAppearance.addAction(self._actionShowPath)
        menuAppearance.addSeparator()
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
        menuAppearance.addAction(self._actionDocumentTabsVisible)
        menuAppearance.addMenu(menuDocumentTabsPosition)
        menuAppearance.addAction(self._actionSheetTabsVisible)
        menuAppearance.addMenu(menuSheetTabsPosition)
        menuAppearance.addSeparator()
        menuAppearance.addAction(self._actionShowStatusbar)
        menuAppearance.addSeparator()
        menuAppearance.addAction(self._actionFullScreen)

        self._toolbarAppearance = self.addToolBar(self.tr("Appearance Toolbar"))
        self._toolbarAppearance.setObjectName("toolbarAppearance")
        self._toolbarAppearance.addAction(self._actionShowMenubar)
        self._toolbarAppearance.addAction(self._actionDocumentTabsVisible)
        self._toolbarAppearance.addAction(self._actionSheetTabsVisible)
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


    def _updateActionDocumentTabsVisible(self, visible):
        """  """
        if visible != self._actionDocumentTabsVisible.isChecked():
            self._actionDocumentTabsVisible.toggle()


    def _updateActionsDocumentTabsPosition(self, position):
        """  """
        for action in self._actionsDocumentTabsPosition.actions():
            if QTabWidget.TabPosition(action.data()) == position:
                action.trigger()
                break


    def _updateActionDocumentTabsAutoHide(self, hide):
        """  """
        if hide != self._actionDocumentTabsAutoHide.isChecked():
            self._actionDocumentTabsAutoHide.toggle()


    def _updateActionSheetTabsVisible(self, visible):
        """  """
        if visible != self._actionSheetTabsVisible.isChecked():
            self._actionSheetTabsVisible.toggle()


    def _updateActionsSheetTabsPosition(self, position):
        """  """
        for action in self._actionsSheetTabsPosition.actions():
            if QTabWidget.TabPosition(action.data()) == position:
                action.trigger()
                break


    def _updateActionSheetTabsAutoHide(self, hide):
        """  """
        if hide != self._actionSheetTabsAutoHide.isChecked():
            self._actionSheetTabsAutoHide.toggle()


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


    def _enableFileActions(self, enabled):

        self._actionCopyPath.setEnabled(enabled)
        self._actionCopyFilename.setEnabled(enabled)


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

        # Show Path
        visible = settings.value("Application/ShowPath", True, type=bool)
        if not visible:  # Default: Visible
            self._actionShowPath.toggle()

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


    def _saveSettings(self):

        settings = QSettings()


        #
        # Application properties

        geometry = self.saveGeometry()
        settings.setValue("Application/Geometry", geometry)

        state = self.saveState()
        settings.setValue("Application/State", state)

        visible = self._actionShowPath.isChecked()
        settings.setValue("Application/ShowPath", visible)

        visible = self._actionShowMenubar.isChecked()
        settings.setValue("Application/ShowMenubar", visible)

        visible = self._actionShowStatusbar.isChecked()
        settings.setValue("Application/ShowStatusbar", visible)

        value = self._actionsToolButtonStyle.checkedAction().data()
        settings.setValue("Application/ToolButtonStyle", value)

        value = self._actionsToolButtonSize.checkedAction().data()
        settings.setValue("Application/ToolButtonSize", value)


    def closeEvent(self, event):

        if self._documentsArea.subWindowCount() >= 1:

            title = self.tr("Quit the application")
            text = self.tr("This will close all open documents and quit the application.\n"
                           "Are you sure you want to continue?")
            buttons = QMessageBox.Yes | QMessageBox.Cancel
            default = QMessageBox.Yes

            if ConfirmationDialog.warning(self, title, text, buttons, default, "ConfirmQuitApplication") == QMessageBox.Cancel:
                event.ignore()
                return None

            self._documentsArea.closeAllSubWindows()

        self._documentsArea.saveSettings()
        self._saveSettings()
        event.accept()


    #
    # Application window
    #

    def _updateWindowModified(self):
        """  """
        docWindow = self._documentsArea.activeSubWindow()
        modified = docWindow.isWindowModified() if docWindow is not None else False
        self.setWindowModified(modified)


    def _updateWindowTitle(self, pathVisible):
        """  """
        docWindow = self._documentsArea.activeSubWindow()
        caption = self.tr("{0} [*]").format(docWindow.windowCaption(pathVisible)) if docWindow is not None else ""
        self.setWindowTitle(caption)


    #
    # Document manager
    #

    def _docManagerTabsVisibleChanged(self, visible):
        """  """
        self._updateActionDocumentTabsVisible(visible)


    def _docManagerTabsPositionChanged(self, position):
        """  """
        self._updateActionsDocumentTabsPosition(position)


    def _docManagerTabsAutoHideChanged(self, hide):
        """  """
        self._updateActionDocumentTabsAutoHide(hide)


    #
    # Document
    #

    def _createDocument(self):

        document = DocumentWidget()

        docWindow = DocumentWindow()
        docWindow.setWidget(document)
        self._documentsArea.addSubWindow(docWindow)

        # Connections: Tabs
        document.tabBarVisibleChanged.connect(self._documentTabsVisibleChanged)
        document.tabBarPositionChanged.connect(self._documentTabsPositionChanged)
        document.tabBarAutoHideChanged.connect(self._documentTabsAutoHideChanged)
        # Connections: Modified
        document.modifiedChanged.connect(docWindow.documentModifiedChanged)
        document.modifiedChanged.connect(self._documentModifiedChanged)
        # Connections: Url
        document.urlChanged.connect(docWindow.documentUrlChanged)
        document.urlChanged.connect(self._documentUrlChanged)
        # Connections: Actions
        docWindow.actionCloseOtherSubWindows.connect(self._documentsArea.closeOtherSubWindows)
        docWindow.actionCopyPath.connect(document.copyPathToClipboard)
        docWindow.actionCopyFilename.connect(document.copyFilenameToClipboard)
        # Connections: Closed
        docWindow.destroyed.connect(self._documentClosed)
        self.documentCountChanged.connect(document.documentCountChanged)
        self.documentCountChanged.connect(docWindow.documentCountChanged)

        # Initialize
        document.initTabBarVisible()
        document.initTabBarPosition()
        document.initTabBarAutoHide()
        document.initModified()
        document.initUrl()

        return document


    def _extractDocument(self, subWindow):

        if subWindow is not None:
            return subWindow.widget()

        return None


    def _activeDocument(self):

        return self._extractDocument(self._documentsArea.activeSubWindow())


    def _hasActiveDocument(self):
        """  """
        return self._activeDocument() is not None


    def openDocument(self, url):

        subWindow = self._documentsArea.findSubWindow(url)
        if subWindow is not None:

            # Given document is already loaded; activate the subwindow
             self._documentsArea.setActiveSubWindow(subWindow)
             return True

        return self._loadDocument(url)


    def _loadDocument(self, url):

        document = self._createDocument()

        if not True:

            # Given document could not be loaded
            document.close()
            return False

        document.show()
        document.setUrl(url)

        self._documentCreated()

        return True


    #
    #
    #

    def _documentCreated(self):
        """  """
        self.documentCountChanged.emit(self._documentsArea.count)
        self._enableActionCloseOther(self._documentsArea.count >= 2)


    def _documentActivated(self, subWindow):

        document = self._extractDocument(subWindow)

        self._updateWindowModified()
        self._updateWindowTitle(self._actionShowPath.isChecked())

        self._updateActionSheetTabsVisible(document.isTabBarVisible() if document is not None else True)
        self._updateActionsSheetTabsPosition(document.getTabBarPosition() if document is not None else QTabWidget.South)
        self._updateActionSheetTabsAutoHide(document.isTabBarAutoHide() if document is not None else True)

        self._enableActions(document is not None)
        self._enableFileActions(not document.getUrl().isEmpty() if document is not None else False)


    def _documentModifiedChanged(self, modified):
        """  """
        if self.sender() == self._activeDocument():
            self._updateWindowModified()


    def _documentUrlChanged(self):
        """  """
        if self.sender() == self._activeDocument():
            self._updateWindowTitle(self._actionShowPath.isChecked())
            self._enableFileActions(not self._activeDocument().getUrl().isEmpty() if self._hasActiveDocument() else False)


    def _documentTabsVisibleChanged(self, visible):
        """  """
        if self.sender() == self._activeDocument():
            self._updateActionSheetTabsVisible(visible)


    def _documentTabsPositionChanged(self, position):
        """  """
        if self.sender() == self._activeDocument():
            self._updateActionsSheetTabsPosition(position)


    def _documentTabsAutoHideChanged(self, hide):
        """  """
        if self.sender() == self._activeDocument():
            self._updateActionSheetTabsAutoHide(hide)


    def _documentClosed(self):
        """  """
        self.documentCountChanged.emit(self._documentsArea.count)
        self._enableActionCloseOther(self._documentsArea.count >= 2)


    #
    # Action slots
    #

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


    def _slotOpen(self):

        urls, _ = QFileDialog.getOpenFileUrls(self, self.tr("Open Document"))
        for url in urls:
            self.openDocument(url)


    def _slotCopyPath(self):
        """  """
        if self._hasActiveDocument():
            self._activeDocument().copyPathToClipboard()


    def _slotCopyFilename(self):
        """  """
        if self._hasActiveDocument():
            self._activeDocument().copyFilenameToClipboard()


    def _slotCloseOther(self):

        if self._documentsArea.subWindowCount() >= 2:

            title = self.tr("Close all documents beside current one")
            text = self.tr("This will close all open documents beside the current one.\n"
                           "Are you sure you want to continue?")
            buttons = QMessageBox.Yes | QMessageBox.Cancel
            default = QMessageBox.Yes

            if ConfirmationDialog.warning(self, title, text, buttons, default, "ConfirmCloseOtherDocuments") != QMessageBox.Cancel:
                self._documentsArea.closeOtherSubWindows(self._documentsArea.activeSubWindow())


    def _slotCloseAll(self):

        if self._documentsArea.subWindowCount() >= 1:

            title = self.tr("Close all documents")
            text = self.tr("This will close all open documents.\n"
                           "Are you sure you want to continue?")
            buttons = QMessageBox.Yes | QMessageBox.Cancel
            default = QMessageBox.Yes

            if ConfirmationDialog.warning(self, title, text, buttons, default, "ConfirmCloseAllDocuments") != QMessageBox.Cancel:
                self._documentsArea.closeAllSubWindows()


    def _slotShowPath(self, checked):
        """  """
        self._updateWindowTitle(checked)


    def _slotShowMenubar(self, checked):

        self.menuBar().setVisible(checked)


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


    def _slotDocumentTabsVisible(self, checked):
        """  """
        self._documentsArea.setTabsVisible(checked)


    def _slotDocumentTabsPosition(self, action):
        """  """
        self._documentsArea.setTabsPosition(QTabWidget.TabPosition(action.data()))


    def _slotDocumentTabsAutoHide(self, checked):
        """  """
        self._documentsArea.setTabsAutoHide(checked)


    def _slotSheetTabsVisible(self, checked):
        """  """
        if self._hasActiveDocument():
            self._activeDocument().setTabBarVisible(checked)


    def _slotSheetTabsPosition(self, action):
        """  """
        if self._hasActiveDocument():
            self._activeDocument().setTabBarPosition(QTabWidget.TabPosition(action.data()))


    def _slotSheetTabsAutoHide(self, checked):
        """  """
        if self._hasActiveDocument():
            self._activeDocument().setTabBarAutoHide(checked)


    def _slotShowStatusbar(self, checked):

        self.statusBar().setVisible(checked)


    def _slotFullScreen(self, checked):

        if checked:
            self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        else:
            self.setWindowState(self.windowState() & ~Qt.WindowFullScreen)

        self._updateActionFullScreen()
