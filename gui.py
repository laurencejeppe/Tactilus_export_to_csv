import sys
import os

import core as PExport

import pandas as pd
import numpy as np
from PyQt5.QtCore import QPoint, QSize, Qt, QTimer, QRect, pyqtSignal
from PyQt5.QtGui import (QColor, QFontMetrics, QImage, QPainter, QIcon,
                         QOpenGLVersionProfile)
from PyQt5.QtWidgets import (QAction, QApplication, QVBoxLayout, QHBoxLayout,
                             QMainWindow, QMessageBox, QComboBox, QButtonGroup,
                             QOpenGLWidget, QFileDialog, QLabel, QPushButton,
                             QSlider, QWidget, QTableWidget, QTableWidgetItem,
                             QAbstractButton, QCheckBox, QErrorMessage)

class converter_GUI(QMainWindow):

    def __init__(self, parent = None):
        super(converter_GUI, self).__init__()
        self.setWindowTitle("Convert Tactilus Export")
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.createActions()
        self.createMenus()

        self.layout = QVBoxLayout()
        
        self.open_export_btn = QPushButton("Open Text File")
        
        self.layout.addWidget(self.open_export_btn)
        
        self.open_export_btn.clicked.connect(self.chooseOpenFile)
        
        self.hlayout = QHBoxLayout()
        self.hlayout.addStretch()
        
        self.numSensorSelect = QComboBox()
        self.numSensorSelect.addItems(['1','2','3','4','5','6'])
        self.setStyleSheet("QComboBox {text-align: center;}")
        self.numSensorSelect.setPlaceholderText('Number of Sensors')
        
        self.hlayout.addWidget(self.numSensorSelect)
        self.hlayout.addStretch()
        
        self.layout.addLayout(self.hlayout)
        
        self.save_csv_btn = QPushButton("Save CSV File")
        
        self.layout.addWidget(self.save_csv_btn)
        
        self.save_csv_btn.clicked.connect(self.chooseSaveFile)
        
        self.mainWidget.setLayout(self.layout)
        self.resize(200,200)
        self.show()
    
        self.export_file = None
        self.csv_file = None

    def chooseOpenFile(self):
        """
        Handles importing and reading of cdb

        """
        fname = QFileDialog.getOpenFileName(self, 'Open file',filter="Text (*.txt)")
        
        if fname[0] == '':
            return
        self.export_file = fname[0]

    def chooseSaveFile(self):
        fname = QFileDialog.getSaveFileName(self, 'Save file', filter="CSV (*.csv)")
        
        if fname[0] == '':
            return
        self.DF = PExport.PressureExport_to_DF(file=self.export_file,numSensors=int(self.numSensorSelect.currentText()))
        self.csv_file = fname[0]
        #try:
        self.DF.to_csv(self.csv_file,index=None)
        #except AttributeError:
        #    print('')

    def createActions(self):
        self.openFile = QAction(QIcon('open.png'), 'Open', self, 
                                shortcut='Ctrl+O', 
                                triggered=self.chooseOpenFile)
        self.saveFile = QAction(QIcon('open.png'), 'Save', self,
                                shortcut='Ctrl+S',
                                triggered=self.chooseSaveFile)
        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                               triggered=self.close)

    def createMenus(self):
        """
        Numpy style docstring.

        """
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.openFile)
        self.fileMenu.addAction(self.saveFile)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = converter_GUI()
    mainWin.show()
    sys.exit(app.exec_())