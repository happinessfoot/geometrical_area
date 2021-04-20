# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeometricalArea
                                 A QGIS plugin
 Плагин для расчета геометрической площади объектов внутри шейп фйла
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-03-22
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Шамсутдинов Р.
        email                : test@test.com
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
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction,QLineEdit,QComboBox,QTableWidgetItem
from qgis.core import  QgsVectorLayer
from qgis.gui import QgisInterface

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .geometrical_area_dialog import GeometricalAreaDialog
import os.path


class GeometricalArea:
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
            'GeometricalArea_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Setup GeoArea')
        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None
        self.layer = QgsVectorLayer()

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
        return QCoreApplication.translate('GeometricalArea', message)


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

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/geometrical_area/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Set up geometrical area in *.shape files'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Setup GeoArea'),
                action)
            self.iface.removeToolBarIcon(action)

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = GeometricalAreaDialog()

        # show the dialog
        self.layer = self.iface.activeLayer()
        if self.layer:
            self.dlg.setWindowTitle(u'Выбранный слой: ' + self.layer.name())
            self.dlg.show()

            self.initInterface()

            # Run the dialog event loop
            result = self.dlg.exec_()
            # See if OK was pressed
            if result:
                # Do something useful here - delete the line containing pass and
                # substitute with your code.
                self.saveResult()
                pass

    #Инициализация интерфейса
    def initInterface(self):
        
        self.btnCalculateInit()
        self.dlg.tableWidget.setColumnCount(3)
        self.dlg.tableWidget.setRowCount(0)
        self.dlg.tableWidget.setColumnHidden(0,True)
        self.dlg.tableWidget.setHorizontalHeaderItem(1,QTableWidgetItem('FeatureID'))
        self.dlg.tableWidget.setHorizontalHeaderItem(2,QTableWidgetItem('Гео. площадь'))
        self.cbPrimarykeyInitialize()

    def btnCalculateInit(self):
        self.dlg.btnCalculate.clicked.connect(self.calculate)

    def cbPrimarykeyInitialize(self):
        self.dlg.cbPrimarykey.currentIndexChanged.connect(self.cbPrimarykey_currentIndexChanged)
        self.dlg.cbPrimarykey.view().setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.cbPrimarykeyFill()

    def cbPrimarykeyFill(self):
        self.dlg.cbPrimarykey.clear()
        fields = ['FeatureID']
        for i in self.layer.fields():
            fields.append(i.name())
        self.dlg.cbPrimarykey.addItems(fields)

    #Остальные методы
    def saveResult(self):
        if not self.layer.isEditable():
            self.layer.startEditing()
        provider = self.layer.dataProvider()
        fieldIdx = provider.fields().indexFromName('AreaGeom')
        for i in range(self.dlg.tableWidget.rowCount()):
            featureId = self.dlg.tableWidget.item(i,0).text()
            self.layer.changeAttributeValue(int(featureId),fieldIdx,float(self.dlg.tableWidget.item(i,2).text()))
        #self.layer.commitChanges()

    #Сигналы
    def cbPrimarykey_currentIndexChanged(self):
        self.dlg.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem(self.dlg.cbPrimarykey.currentText()))
        pk = self.dlg.cbPrimarykey.currentText()
        if(self.dlg.tableWidget.rowCount()>0):
            for i in range(self.dlg.tableWidget.rowCount()):
                feature = self.layer.getFeature(int(self.dlg.tableWidget.item(i,0).text()))
                if pk == 'FeatureID':
                    self.dlg.tableWidget.item(i, 1).setText(str(feature.id()))
                else:
                    self.dlg.tableWidget.item(i, 1).setText(str(feature[self.dlg.cbPrimarykey.currentText()]))
    def calculate(self):
        self.dlg.tableWidget.setRowCount(0)
        selectedFeatures = self.layer.selectedFeatures()
        rowIndex = 0;
        for feature in selectedFeatures:
            self.dlg.tableWidget.insertRow(rowIndex)
            item1 = QTableWidgetItem(str(feature.id()))
            item1.setFlags(QtCore.Qt.ItemIsEnabled)
            item2 = QTableWidgetItem(str(round((feature.geometry().area()/10000),1)))
            item2.setFlags(QtCore.Qt.ItemIsEnabled)
            pk = self.dlg.cbPrimarykey.currentText()
            if pk =='FeatureID':
                item3 = QTableWidgetItem(str(feature.id()))
            else:
                item3 = QTableWidgetItem(str(feature[pk]))
            item3.setFlags(QtCore.Qt.ItemIsEnabled)
            self.dlg.tableWidget.setItem(rowIndex,0,item1)
            self.dlg.tableWidget.setItem(rowIndex,1,item3)
            self.dlg.tableWidget.setItem(rowIndex,2,item2)
            rowIndex += 1