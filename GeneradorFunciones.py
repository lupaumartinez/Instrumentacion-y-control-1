# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 19:16:28 2019

@author: nicon
"""
import pyvisa
import numpy as np
import time

from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import DockArea, Dock

#%%

class Generadordefunciones(QtGui.QFrame):

    def __init__(self, instrument = 0):  
        super().__init__()
        
        self.rm = pyvisa.ResourceManager()
        if len(self.rm.list_resources()) > 0:
            self.inst = self.rm.open_resource(self.rm.list_resources()[instrument])
        else:
            self.inst = []
            print('No se detectó ningún instrumento')
        if self.inst != []:
            try:
                print('El IDN del instrumento es ', self.inst.query("*IDN?"))
            except:
                print('El instrumento no respondió cuando se le preguntó el nombre.')
                
  # %% Buttons       
 
        self.set_button = QtGui.QPushButton('Setear')
        self.set_button.clicked.connect(self.set)

        self.frecuencia_Label = QtGui.QLabel('Frecuencia:')
        self.frecuencia_lambda_Edit = QtGui.QLineEdit('5000')
        
        self.voltaje_Label = QtGui.QLabel('Voltaje:')
        self.voltaje_lambda_Edit = QtGui.QLineEdit('10')

        self.offset_Label = QtGui.QLabel('Offset:')
        self.offset_Edit = QtGui.QLineEdit('0')

        self.shape_Label = QtGui.QLabel('Forma:')
        self.shape_Edit = QtGui.QLineEdit('SIN')

# %% Interface

        self.generador = QtGui.QWidget()
        generadors_layout = QtGui.QGridLayout()
        self.generador.setLayout(generador_layout)

        generador_layout.addWidget(self.frecuecia_Label, 1, 1)
        generador_layout.addWidget(self.frecuecia_Edit,  2, 1)
        generador_layout.addWidget(self.voltaje_Label,  1, 2)
        generador_layout.addWidget(self.voltaje_Edit,   2, 2)
        generador_layout.addWidget(self.offset_Label,   1, 3)
        generador_layout.addWidget(self.offset_Edit,    2, 3)
        generador_layout.addWidget(self.shape_Label,    1, 4)
        generador_layout.addWidget(self.shape_Edit,     2, 4)
        generador_layout.addWidget(self.set_button,     3, 6)
   
#%%  docks

        hbox = QtGui.QHBoxLayout(self)
        dockArea = DockArea()
        
        generador_dock = Dock('Generador de funciones')
        generador_dock.addWidget(self.generador)

        dockArea.addDock(generador_dock)
        hbox.addWidget(dockArea)
        self.setLayout(hbox)
       
#%% Backend
    
    def TurnOn(self, channel = 1):
        self.inst.write("OUTPut{}:STATe ON".format(channel))
        
    def TurnOff(self, channel = 1):
        self.inst.write("OUTPut{}:STATe OFF".format(channel))
        
    def GetFrequency(self, channel = 1):
        self.inst.query('SOURce{}:FUNCtion:FREQuency?'.format(channel))
        
    def SetFrequency(self, freq, channel = 1):
        self.inst.write("SOURce{}:FREQuency {}".format(channel,freq))
    
    def GetShape(self, channel = 1):
        self.inst.query('SOURce{}:FUNCtion:SHAPe?'.format(channel))
    
    def SetShape(self, shape, channel = 1):
        self.inst.write('SOURce{}:FUNCtion {}'.format(channel, shape))
    
    def GetVoltage(self, channel = 1):
        self.inst.query('SOURce{}:VOLTage:LEVel:IMMediate:AMPLitude?'.format(channel))
    
    def SetVoltage(self, voltage, channel = 1):
        self.inst.write('SOURce{}:VOLTage:LEVel:IMMediate:AMPLitude {}'.format(channel, voltage))
        
    def GetOffset(self, channel = 1):
        self.inst.query('SOURce{}:VOLTage:LEVel:IMMediate:OFFSet?'.format(channel))        
    
    def SetOffset(self, offset, channel = 1):
        self.inst.write('SOURce{}:VOLTage:LEVel:IMMediate:OFFSet {}'.format(channel, offset))        
    
    def GeneralSet(self, freq, voltage, offset = '0 V', shape = 'SIN', channel = 1):
        self.SetFrequency(freq, channel)
        self.SetVoltage(voltage, channel)
        self.SetOffset(offset, channel)
        self.SetShape(shape, channel)
    
    def DiscreteSweep(self, freqini, frecfin, step, timeoff = 1,  channel = 1):
        Frequencies = np.array(float(freqini.split(" ")[0]), float(frecfin.split(" ")[0]), float(step.split(" ")[0]))
        #esto es por si el input lo consideramos como "2 kHz" o algo así. el split separa un string
        #en partes, dependiendo del separador (en este caso el separador es un espacio).
        for Fr in Frequencies:
            self.inst.write("SOURce{}:FREQuency {} {}".format(channel, Fr, freqini.split(" ")[1]))
            time.sleep(timeoff)
        
    def ContinuosSweep(self, freqini, freqfin, sweeptime, sweeptype = "LINear", channel = 1):
        self.inst.write('SOURce{}:SWEep:SPACing {}'.format(channel, sweeptype))
        self.inst.write('SOURce{}:SWEep:TIME {}'.format(channel, sweeptime))    
        self.inst.write('SOURce{}:FREQuency:STARt {}'.format(channel, freqini))
        self.inst.write('SOURce{}:FREQuency:STOP {}'.format(channel, freqfin))
        pass
    
    def set_parameters(self):
        self.frecuencia = float(self.frecuencia_Edit.text())
        self.voltaje = float(self.voltaje_Edit.text()) 
        self.offset = float(self.offset_Edit.text())
        self.shape = float(self.shape_Edit.text())
        
    def set(self):
        self.set_parameters()
        self.GeneralSet(self.frecuencia, self.voltaje, set.offset, set.shape, channel = 1)        
#%%

app = QtGui.QApplication([])
win = Generadordefunciones()
win.show()
app.exec_()
    
