# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 14:14:59 2020

@author: Martin Garaj

This is script representing the BK Precision 9202 Voltage source.
"""

#%%############################################################################
################################### IMPORTS ###################################
###############################################################################
import numpy as np

#%%############################################################################
############################## OBJECT DEFINITION ##############################
###############################################################################
class BKPrecision9202(object):
    """A class representing DK Precision 8600 Electronic load."""

    #%% Class varables
    _addr = None # address of the device
    _inst = None # instance of the opened device
    _errQ = list() # error queue
    
    #%% Constructor
    def __init__(self, VISAresourceManager, deviceAddress, timeout=3000, debugMode=False):
        # instance of the device
        self._inst = VISAresourceManager.open_resource(deviceAddress) # write_termination= '\n', read_termination='\x00'
        # check whether the session is obtained
        if(self._inst.session):
            # get the device information
            response = self._inst.query('*IDN?')
            message = (self.__class__.__name__ + ': Session for device instance with address '+str(deviceAddress)+' is running\n') \
                    + (self.__class__.__name__ + ': Device identification:\n') \
                    + (self.__class__.__name__ + ': ' + response)
            self._inst.timeout = timeout
            ### DEBUG
            if(debugMode):
                print(message)
        else:
            message = (self.__class__.__name__ + ': Session for device instance with address '+str(deviceAddress)+' is NOT running\n')
            self._inst.close() # assure the device is closed
            ### DEBUG
            if(debugMode):
                print(message)
        # keep 
        self._addr = deviceAddress
        
    #%% Destructor
    def __del__(self):
        # close the instance of the device
        self._inst.close() # assure the device is closed
        
    #%% Reset
    def reset(self):
        self._inst.write('*RST')
        self._inst.write('*CLS')
        self._inst.write('*SRE 0')
        self._inst.write('*ESE 0')
        self._inst.write('*OPC')

    #%% Wait
    def wait(self):
        self._inst.write('*OPC')
        
    #%% getErrorQueue
    def getErrorQueue(self):
        # Check error queue
        errQempty = False
        _errQ = list()
        while(not errQempty):
            err = self._inst.query('SYSTem:ERRor?')
            if(err[0] == '0'):
                errQempty = True
            else:
                _errQ.append(err)
        return _errQ
    
    #%% Configure Device
    #   This function hides all details, that are not necessary for performing
    def configDeviceRemote(self, debugMode=False):
        # set remote control
        self._inst.write('SYSTem:REMote')
        # set communication interface
        self._inst.write('SYSTem:INTerface USB')
        # set output OFF
        self._inst.write('SOURce:OUTPut:STATe OFF')
        ### DEBUG
        if(debugMode):
            print('SOURce:OUTPut:STATe '+self._inst.query('SOURce:OUTPut:STATe?'))
            print(self.getErrorQueue())

    #%% Set limit            
    def setCurrentLimit(self, currentLimit, debugMode=False):
        # set output OFF
        self._inst.write('SOURce:CURRent:PROTection '+str(currentLimit))
        self._inst.write('SOURce:CURRent:PROTection:STATe ON')
        self._inst.write('SOURce:CURRent:LEVel:IMMediate:AMPLitude '+str(currentLimit))
        ### DEBUG
        if(debugMode):
            print('SOURce:CURRent:PROTection '+self._inst.query('SOURce:CURRent:PROTection?'))
            print('SOURce:CURRent:PROTection:STATe '+self._inst.query('SOURce:CURRent:PROTection:STATe?'))
            print('SOURce:CURRent:LEVel:IMMediate:AMPLitude '+str(self._inst.query('SOURce:CURRent:LEVel:IMMediate:AMPLitude?')))
            print(self.getErrorQueue())
            
    #%% Enable output           
    def enableOutput(self, outputBool, debugMode=False):
        if(outputBool):
            # set output ON
            self._inst.write('SOURce:OUTPut:STATe ON')
        else:
            # set output OFF
            self._inst.write('SOURce:OUTPut:STATe OFF')
        ### DEBUG
        if(debugMode):
            print('SOURce:OUTPut:STATe '+self._inst.query('SOURce:OUTPut:STATe?'))
            print(self.getErrorQueue())
    
    #%% Set vVoltage
    def setVoltage(self, outputValue, debugMode=False):
        # set output ON
        self._inst.write('SOURce:VOLTage '+str(outputValue))
        ### DEBUG
        if(debugMode):
            print('SOURce:VOLTage '+self._inst.query('SOURce:VOLTage?'))
            print(self.getErrorQueue())
    
    #%% Measure voltage
    def measureVolatge(self):
        return float( self._inst.query('MEASure:VOLTage?') )

    #%% Measure current
    def measureCurrent(self):
        return float( self._inst.query('MEASure:CURRent?') )        
        
    #%% Measure power
    def measurePower(self):
        return float( self._inst.query('MEASure:POWer?') )     
    
    #%% Display control - has to be done MANUALLY
#    def displayDVM(self, boolDisplay, debugMode=False):
#        if(boolDisplay):
#            # set output ON
#            self._inst.write('MEASure:SCALar:STATus DVM')
#        else:
#            # set output OFF
#            self._inst.write('MEASure:SCALar:STATus NORMAL')
#            
#        ### DEBUG
#        if(debugMode):
#            self.wait()
##            print('MEASure:STATus '+self._inst.query('MEASure:STATus?')) # this query is not implemented on the device
#            print(self.getErrorQueue())

        
    