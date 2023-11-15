# -*- coding: utf-8 -*-
"""Gui code for converting Tactilus export.txt files to .csv file

This module generates a gui application for converting text files exported 
from Tactilus software to a .csv file format. 

Example:
    $ python gui.py

Todo:
    * TODO: Include some more documentation.
"""

import sys
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QVBoxLayout, QHBoxLayout,
                             QMainWindow, QComboBox, QFileDialog, QLabel, 
                             QPushButton, QWidget)
import core as PExport

class ConverterGUI(QMainWindow):
    """ This class is the main window for the gui application. """
    def __init__(self):
        super(ConverterGUI, self).__init__()
        self.setWindowTitle("Convert Tactilus Export")
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.create_actions()
        self.create_menus()

        self.layout = QVBoxLayout()

        self.open_export_btn = QPushButton("Open Text File")

        self.layout.addWidget(self.open_export_btn)

        self.open_export_btn.clicked.connect(self.choose_open_file)

        self.file_label = QLabel()
        self.file_label.setText('Files:\t')
        self.file_label.setAlignment(Qt.AlignTop)
        self.layout.addWidget(self.file_label)

        self.hlayout = QHBoxLayout()
        self.hlayout.addStretch()

        self.num_sensor_select = QComboBox()
        self.num_sensor_select.addItems(['1','2','3','4','5','6'])

        self.num_sensor_label = QLabel()
        self.num_sensor_label.setText('Select Number of Sensors')

        self.hlayout.addWidget(self.num_sensor_label)
        self.hlayout.addWidget(self.num_sensor_select)
        self.hlayout.addStretch()

        self.layout.addLayout(self.hlayout)

        self.save_csv_btn = QPushButton("Save CSV File 1.")

        self.layout.addWidget(self.save_csv_btn)

        self.save_csv_btn.clicked.connect(self.choose_save_file)

        self.main_widget.setLayout(self.layout)
        self.resize(200,200)
        self.show()

        self.export_files = []
        self.csv_files = []

    def choose_open_file(self):
        """
        Handles importing and reading of cdb
        """
        os.chdir('..')
        fname = QFileDialog.getOpenFileNames(self, 'Open file', filter="Text (*.txt)")

        if fname[0] == '':
            return

        for file in fname[0]:
            self.export_files.append(file)

        self.update_file_list_label()


    def choose_save_file(self):
        """
        Handles saving the inp files
        """
        file = self.export_files[0]
        fname = QFileDialog.getSaveFileName(self, f'Save file: {file}', filter="CSV (*.csv)")

        if fname[0] == '':
            return

        df = PExport.PressureExport_to_DF(file=file,
                                          numSensors=int(self.num_sensor_select.currentText()))
        csv_file = fname[0]

        df.to_csv(csv_file,index=None)

        self.export_files.remove(file)

        self.update_file_list_label()


    def update_file_list_label(self):
        """
        Handles deleting and adding items to the list of files that appears on the GUI
        """
        label = 'Files:\t'
        for i, fname in enumerate(self.export_files):
            label += f"{i+1}. {fname.split('/')[-1]}\n\t"
        self.file_label.setText(label)


    def create_actions(self):
        """
        Initiates the GUI actions
        """
        self.open_file = QAction(QIcon('open.png'), 'Open', self,
                                shortcut='Ctrl+O',
                                triggered=self.choose_open_file)
        self.save_file = QAction(QIcon('open.png'), 'Save', self,
                                shortcut='Ctrl+S',
                                triggered=self.choose_save_file)
        self.exit_act = QAction("E&xit", self, shortcut="Ctrl+Q",
                               triggered=self.close)


    def create_menus(self):
        """
        Numpy style docstring.
        """
        self.file_menu = self.menuBar().addMenu("&File")
        self.file_menu.addAction(self.open_file)
        self.file_menu.addAction(self.save_file)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_act)
        self.help_menu = self.menuBar().addMenu("&Help")
        self.help_menu.addAction(self.exit_act)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    CSS = "styles.css"
    with open(CSS,"r",encoding='UTF-8') as stylesheet:
        app.setStyleSheet(stylesheet.read())
    mainWin = ConverterGUI()
    mainWin.show()
    sys.exit(app.exec_())
