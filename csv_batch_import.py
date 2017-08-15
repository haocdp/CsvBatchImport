# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CsvBatchImport
                                 A QGIS plugin
 Batch Import .csv Files in a Dictionary 
                              -------------------
        begin                : 2017-08-09
        git sha              : $Format:%H$
        copyright            : (C) 2017 by haoc
        email                : haoc_dp@163.com
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QFileDialog
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from csv_batch_import_dialog import CsvBatchImportDialog
import os.path
import os
# from qgis.core import *
import qgis
from qgis._core import QgsApplication, QgsVectorLayer, QgsMapLayerRegistry, QgsProject, QgsMarkerSymbolV2


class CsvBatchImport:
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
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'CsvBatchImport_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
        
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Csv Batch Import')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'CsvBatchImport')
        self.toolbar.setObjectName(u'CsvBatchImport')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('CsvBatchImport', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = CsvBatchImportDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/CsvBatchImport/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'batch import csv files'),
            callback=self.run,
            parent=self.iface.mainWindow())
        
        self.dlg.lineEdit.clear()
        self.dlg.pushButton.clicked.connect(self.select_dictionary)
        
        self.dlg.button_box.accepted.connect(self.loadCsvFiles)


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Csv Batch Import'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def select_dictionary(self):
        filepath = QFileDialog.getExistingDirectory(self.dlg, self.tr(u'select a dictionary'),
                                                    "C:\Users",
                                                    QFileDialog.ShowDirsOnly 
                                                    | QFileDialog.DontResolveSymlinks)
        # print filepath
        if filepath.strip():
            self.dlg.lineEdit.setText(filepath)
            
            
    def loadCsvFiles(self):
        # 清除画布上的所有图层
        # QgsMapLayerRegistry.instance().removeAllMapLayers()
        
        # 图标样式，圆，大小设为1
        # symbol = QgsMarkerSymbolV2.createSimple({'name':'circle', 'size':'1'})
        
        filepath = self.dlg.lineEdit.text()
        
        # 获取文件夹中的所有文件，并过滤不是csv格式的文件
        files = os.listdir(filepath)
        for file in files:
            if not os.path.isdir(file) and os.path.splitext(file)[1] == '.csv' and not file.startswith('.') :
                uri = "file:///" + filepath + "/" + file + "?delimiter=%s&crs=epsg:4326&xField=%s&yField=%s" % (",", "longitude", "latitude")
                vlayer = QgsVectorLayer(uri, os.path.splitext(file)[0], "delimitedtext")
                vlayer.rendererV2().symbol().setSize(1.3);
                if vlayer.isValid():
                    QgsMapLayerRegistry.instance().addMapLayer(vlayer)
                
        