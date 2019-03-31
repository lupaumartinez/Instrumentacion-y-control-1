# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 17:18:06 2019

@author: Luciana
"""

# %%

from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import DockArea, Dock


# %%
class Spectrum(QtGui.QFrame):

    def __init__(self):  
        super().__init__()

# %% Buttons       
 
        self.spectrum_button = QtGui.QPushButton('Spectrum')
        self.spectrum_button.setCheckable(True)
        self.spectrum_button.clicked.connect(self.measurment_spectrum)

    # parameters

        self.first_lambda_Label = QtGui.QLabel('Start ... (nm):')
        self.first_lambda_Edit = QtGui.QLineEdit('450')
        
        self.last_lambda_Label = QtGui.QLabel('Finish ... (nm):')
        self.last_lambda_Edit = QtGui.QLineEdit('850')

        self.ganancia_Label = QtGui.QLabel('Ganancia:')
        self.ganancia_Edit = QtGui.QLineEdit('1')

        self.time_Label = QtGui.QLabel('Time integration (s):')
        self.time_Edit = QtGui.QLineEdit('2')

# %% Interface

        self.spectrum = QtGui.QWidget()
        spectrum_parameters_layout = QtGui.QGridLayout()
        self.spectrum.setLayout(spectrum_parameters_layout)

        spectrum_parameters_layout.addWidget(self.first_lambda_Label, 1, 1)
        spectrum_parameters_layout.addWidget(self.first_lambda_Edit,  2, 1)
        spectrum_parameters_layout.addWidget(self.last_lambda_Label,  1, 2)
        spectrum_parameters_layout.addWidget(self.last_lambda_Edit,   2, 2)
        spectrum_parameters_layout.addWidget(self.time_Label,         1, 3)
        spectrum_parameters_layout.addWidget(self.time_Edit,          2, 3)
        spectrum_parameters_layout.addWidget(self.ganancia_Label,     1, 4)
        spectrum_parameters_layout.addWidget(self.ganacia_Edit,       2, 4)
        spectrum_parameters_layout.addWidget(self.spectrum_button,    3, 6)
   
#%%  DOCKs

        hbox = QtGui.QHBoxLayout(self)
        dockArea = DockArea()
        
        spectrum_dock = Dock('Spectrum')
        spectrum_dock.addWidget(self.spectrum)

        dockArea.addDock(spectrum_dock)
        hbox.addWidget(dockArea)
        self.setLayout(hbox)

    def measurment_spectrum(self):
        if self.spectrum_button.isChecked():
           self.start_spectrum()
        else:
           self.stop_spectrum()
    
    def start_spectrum(self):  
           print('Start measurment spectrum')

    def stop_spectrum(self):  
           print('Stop measurment spectrum')

    def parameters_spectrum(self):
           first_lambda = float(self.first_lambda_Edit.text())
           last_lambda = float(self.last_lambda_Edit.text())
           time = float(self.time_Edit.text())
           ganancia = float(self.ganancia_Edit.text())

#%%

app = QtGui.QApplication([])
win = Spectrum()
win.show()
app.exec_()
    
    