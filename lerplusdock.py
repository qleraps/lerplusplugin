# -*- coding: utf-8 -*-
from qgis.PyQt.QtGui import QIcon
"""
/***************************************************************************
 LerPlusDock
                                 A QGIS plugin
 Nem adgang til LER2 forespørgsler
                              -------------------
        begin                : 2023-10-09
        git sha              : $Format:%H$
        copyright            : (C) 2023 by qLER ApS
        email                : morten@qler.dk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtWidgets import QDockWidget, QAction, QHBoxLayout, QVBoxLayout
# Initialize Qt resources from file resources.py
#from .resources import *
#from .config import Settings, OptionsFactory
from qgis.gui import QgsOptionsWidgetFactory, QgsOptionsPageWidget
from qgis.core import *
# Import the code for the DockWidget
from .lerpluswidget import LerPlusWidget
import os.path
from PyQt5 import QtCore, QtWidgets

SETTINGS_WIDGET, BASE  = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'lerplussettings.ui'))
class LerPlusDock:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        #locale = QSettings().value('locale/userLocale')[0:2]
        #locale_path = os.path.join(
        #    self.plugin_dir,
        #    'i18n',
        #    'LerPlusDock_{}.qm'.format(locale))

        #if os.path.exists(locale_path):
        #    self.translator = QTranslator()
        #    self.translator.load(locale_path)
        #    QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        #self.actions = []
        #self.menu = self.tr(u'&LER+')
        self.menu='LER+'

        # TODO: We are going to let the user set this up in a future iteration
        #self.toolbar = self.iface.addToolBar(u'LerPlusDock')
        #self.toolbar.setObjectName(u'LerPlusDock')

        #print "** INITIALIZING LerPlusDock"

        #self.pluginIsActive = False
        #self.dockwidget = None

        #self.settings = Settings()
        #self.options_factory = OptionsFactory(self.settings)



    # noinspection PyMethodMayBeStatic
    #def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
     #   return QCoreApplication.translate('LerPlusDock', message)




    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/lerplusdock/icon.png'
        """self.add_action(
            icon_path,
            text=self.tr(u'LER+'),
            callback=self.run,
            parent=self.iface.mainWindow()
        )"""

        self.lerpluswidget = LerPlusWidget(self.iface) #, self.settings

        # create the dockwidget with the correct parent and add the valuewidget
        self.lerplusdockwidget = QDockWidget(
            "LER+", self.iface.mainWindow()
        )
        self.lerplusdockwidget.setObjectName("LER+")
        self.lerplusdockwidget.setWidget(self.lerpluswidget)
        # add the dockwidget to iface
        self.iface.addDockWidget(
            Qt.TopDockWidgetArea, self.lerplusdockwidget
        )

        self.options_factory = lerplusOptionsFactory()
        self.options_factory.setTitle('LER+')
        self.iface.registerOptionsWidgetFactory(self.options_factory)

        #self.settings.settings_updated.connect(self.lerpluswidget.readconfig)


    #--------------------------------------------------------------------------


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        #self.lerpluswidget.unload() # try to avoid processing events, when QGIS is closing
        self.iface.removeDockWidget(self.lerplusdockwidget)
        self.iface.unregisterOptionsWidgetFactory(self.options_factory)
        #print("** UNLOAD LerPlusDock")
        # remove the toolbar
        #del self.toolbar



    #--------------------------------------------------------------------------
    """
    #def run(self):
        #Run method that loads and starts the plugin



       if not self.pluginIsActive:
            self.pluginIsActive = True

            #print "** STARTING LerPlusDock"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = LerPlusDockWidget()
                self.dockwidget.setIface(self.iface)
                settings = QSettings()
                geometry = settings.value("lerplusdock/geometry")

                if geometry:
                    # Restore the dock widget's state
                    self.dockwidget.restoreGeometry(geometry)

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.BottomDockWidgetArea, self.dockwidget)
            self.dockwidget.show()
    """

class lerplusOptionsFactory(QgsOptionsWidgetFactory):

    def __init__(self):
        super().__init__()

    def icon(self):
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.png')
        return QIcon(icon_path)

    def createWidget(self, parent):
        return lerplusConfigOptionsPage(parent)


class lerplusConfigOptionsPage(QgsOptionsPageWidget, SETTINGS_WIDGET):

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

        settings = QgsSettings()

        self.apitokenEdit.setText(settings.value("lerplusdock/apitoken"))
        if settings.value("lerplusdock/debugmode") == "1":
            #print('s1')
            self.debugCheckbox.setChecked(True)
        else:

            #print(settings.value("lerplusdock/debugmode"))
            self.debugCheckbox.setChecked(False)

        self.config_widget = lerplusConfigOptionsDialog()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setMargin(0)
        self.setLayout(layout)
        layout.addWidget(self.config_widget)
        #layout = QHBoxLayout()
        #layout.setContentsMargins(0, 0, 0, 0)
        #self.setLayout(layout)

    def apply(self):

        #        self.config_widget.saveoptions()
        settings = QgsSettings()
        token = self.apitokenEdit.text()
        settings.setValue("lerplusdock/apitoken", token)
        if self.debugCheckbox.checkState() == QtCore.Qt.Checked:
            #print('1')
            settings.setValue("lerplusdock/debugmode", "1")
        else:
            #print('0')
            settings.setValue("lerplusdock/debugmode", "0")
        # QMessageBox.information(self, 'API-response', check.str())
        #self.iface.messageBar().pushMessage("Success", "settings saved", level=Qgis.Info, duration=5)

        #QgsMessageLog.logMessage("Your settings was saved!", level=Qgis.Info)
        #self.settings.emit_updated()


class lerplusConfigOptionsDialog(SETTINGS_WIDGET, BASE):
    def __init__(self):
        super(lerplusConfigOptionsDialog, self).__init__(None)
