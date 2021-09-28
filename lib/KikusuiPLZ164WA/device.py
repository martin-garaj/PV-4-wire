# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 14:14:59 2020

@author: Martin Garaj

This is script representing the Kikusui PLZ 164 WA as a software object. 
"""

#%%############################################################################
################################### IMPORTS ###################################
###############################################################################
import numpy as np

#%%############################################################################
############################## OBJECT DEFINITION ##############################
###############################################################################
class KikusuiPLZ164WA(object):
    """A class representing Kikusui PLZ 164 WA Electronic load."""

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
        self._inst.write('*WAI')
        self._inst.write('*CLS')
        self._inst.write('*WAI')
        self._inst.write('*SRE 0')
        self._inst.write('*WAI')
        self._inst.write('*ESE 0')
        self._inst.write('*WAI')

    #%% Wait
    def wait(self):
        self._inst.write('*WAI')
        
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
    
    #%% Measure voltage
    def measureVolatge(self):
        return float( self._inst.query('MEASure:VOLTage?') )

    #%% Measure current
    def measureCurrent(self):
        return float( self._inst.query('MEASure:CURRent?') )        
        
    #%% Measure power
    def measurePower(self):
        return float( self._inst.query('MEASure:POWer?') )      
    
    #%% Configure Device
    #   This function hides all details, that are not necessary for performing
    def configDeviceRemote(self, remoteSense='OFF', voltageRange='HIGH', currentRange='HIGH', outputFunc='CC', debugMode=False):
        # remoteSense
        #   Use remote sensing (4-wire connection) to measure voltage (max 2[V] compensation)
        # voltageRange
        #   {LOW|MEDium|HIGH} = {33[A]|3.3[A]|0.33[A]}
        # currentRange
        #   {LOW|HIGH} = {150[V]|15[V]}
        # outputFunc
        #    CC	     Constant current mode
        #    CV	     Constant voltage mode
        #    CP	     Constant power mode
        #    CR	     Constant resistance mode
        #    CCCV	 Constant current mode + constant voltage mode
        #    CRCV	 Constant resistance mode + constant voltage mode
                
        # enable remote control
        self._inst.write('SYSTem:RENable ON') # same as SYSTem:REMote but specifically over USB for PLZW
        # set load on/off condition
        self._inst.write('PROGram:LINPut OFF') # the same as PROGram:LOUTput OFF
        ### DEBUG
        if(debugMode):
            print(self.getErrorQueue())
        # set mode
        self._inst.write('SOURce:FUNCtion ' + outputFunc)
        ### DEBUG
        if(debugMode):
            print('SOURce:FUNCtion '+self._inst.query('SOURce:FUNCtion?'))
            print(self.getErrorQueue())
        # set range
        self._inst.write('SOURce:CURRent:RANGe ' + currentRange)
        ### DEBUG
        if(debugMode):
            print('SOURce:CURRent:RANGe '+self._inst.query('SOURce:CURRent:RANGe?'))
            print(self.getErrorQueue())
        self._inst.write('SOURce:VOLTage:RANGe ' + voltageRange)
        ### DEBUG
        if(debugMode):
            print('SOURce:VOLTage:RANGe '+self._inst.query('SOURce:VOLTage:RANGe?'))
            print(self.getErrorQueue())

        
    #%% Configure Sweep
    def configSweep(self, idleValue, seqID=1, rampBool=True, seqName='NONE', seqOutputFunc='NCC', 
                    seqVoltageRange='HIGH', seqCurrentRange='HIGH', seqLoop=1, 
                    seqValues=np.array([0]), seqTimeSteps=np.array([1]),
                    debugMode=False):
        ### DESCRIPTION
        #   This function configures a sweep of a given variable (preferably 
        #   voltage, but current, power and resistance are allowed), where the 
        #   steps are given as an array, together with the time the steps will 
        #   take to perform. The transition from one step to another is RAMP.
        ### INPUTS:
        # idleValue
        #   CAREFUL, this is the value that the el. load is set to when not doing anything (although at this state the output of the load should be OFF)
        # seqID
        #   number from 1 to 10 (11 is reseved for FAST sequence)
        # rampBool
        #   boolean on whether the current in between the steps is ramp-ing up/down (True), or is a step/stair (False)
        # seqName
        #   arbitrary string of up to 11 characters
        # seqOutputFunc
        #    NCC	    Nomal sequence, CC mode
        #    NCR	    Nomal sequence, CR mode
        #    NCV	    Nomal sequence, CV mode
        #    NCP	    Nomal sequence, CP mode
        #    FCC	    Fast sequence, CC mode
        #    FCR	    Fast sequence, CR mode
        # seqVoltageRange
        #   {LOW|MEDium|HIGH} = {33[A]|3.3[A]|0.33[A]}
        # seqCurrentRange
        #   {LOW|HIGH} = {150[V]|15[V]}
        # seqLoop
        #   number of times, the program/sequence is looped
        # seqValues
        #   array of values that the device will follow
        # seqTimeSteps
        #   array of times, that the values will ramp from one step to another
        # debugMode
        #   True - check every step, print error queue, False - just send commands, no checking, no error printing
        
        #%% 1) Program operation
        ### DEBUG
        if(debugMode): 
            print('configSweep: 1) Program operation')
        # clear existing sequence 
        self._inst.write('PROGram:CLEar')
        # set the sequence ID
        self._inst.write('PROGram:NAME '+str(seqID))

        # set 
        self._inst.write('PROGram:MEMO "'+str(seqName[0:11])+'"')
        ### DEBUG
        if(debugMode):
            print('PROGram:MEMO '+self._inst.query('PROGram:MEMO?'))
            print(self.getErrorQueue())
            
        self.wait()            
            
        # set normal mode output
        self._inst.write('PROGram:MODE '+seqOutputFunc)
        ### DEBUG
        if(debugMode):
            print('PROGram:MODE '+self._inst.query('PROGram:MODE?') ) # {NCC|NCR|NCV|NCP|FCC|FCR}
            
        # set voltage range
        self._inst.write('PROGram:VRANge '+seqVoltageRange) 
        ### DEBUG
        if(debugMode):
            print('PROGram:VRANge '+self._inst.query('PROGram:VRANge?'))
            print(self.getErrorQueue())
        
        # set current range
        self._inst.write('PROGram:CRANge '+seqCurrentRange) 
        ### DEBUG
        if(debugMode):
            print('PROGram:CRANge '+self._inst.query('PROGram:CRANge?'))
        
        # set number of loops
        self._inst.write('PROGram:LOOP '+str(seqLoop)) 
        ### DEBUG
        if(debugMode):
            print('PROGram:LOOP '+self._inst.query('PROGram:LOOP?'))
            print(self.getErrorQueue())
    
        self.wait()        
    
        #%% 2) Operation after end of program
        ### DEBUG
        if(debugMode):
            print('2) Operation after end of program')

        # set load on/off condition
        self._inst.write('PROGram:LINPut OFF') # the same as PROGram:LOUTput OFF
        ### DEBUG
        if(debugMode):
            print('PROGram:LINPut '+self._inst.query('PROGram:LINPut?') ) 
            print(self.getErrorQueue())
            
        # continue with another sequence/program
        self._inst.write('PROGram:CHAin 0') # the same as PROGram:LOUTput OFF
        ### DEBUG
        if(debugMode):
            print('PROGram:CHAin '+self._inst.query('PROGram:CHAin?') ) 
            print(self.getErrorQueue())
            
        self.wait()                

        #%% 3) Operation after end of program
        ### DEBUG
        if(debugMode):
            print('3) Operation after end of program')

        # delete all existing steps
        self._inst.write('PROGram:NSPeed:DELete:ALL')
        
        ### DEBUG
        if(debugMode):
            # count the number of existing steps
            print('PROGram:NSPeed:COUNt '+self._inst.query('PROGram:NSPeed:COUNt?'))
            print(self.getErrorQueue())
        
        # load sequence onto the device
        seqValues = np.array(seqValues)
        seqTimeSteps  = np.array(seqTimeSteps)
        seqNumStep = len(seqValues)
        ### DEBUG
        if(debugMode):
            # count the number of existing steps
            print('Given sequence has ' + str(seqNumStep) + ' steps')    
            print('Given sequence seqValues: ')
            print(seqValues)
            print('Given sequence seqTimeSteps: ')
            print(seqTimeSteps)
        
        # default values for every step of the sequence
        _load_bool   = 'ON'
        if(rampBool):
            _ramp_bool   = 'ON' 
        else:
            _ramp_bool   = 'OFF'
        _trig_bool   = 'OFF'
        _pause_bool  = 'OFF'
        
        # trigger ON for the first step
        self._inst.write('PROGram:NSPeed:ADD '+str(seqValues[0])+','+str(0.01)+',OFF,OFF,OFF,'+_pause_bool)
        ### DEBUG
        if(debugMode):
            print('PROGram:NSPeed:ADD '+str(seqValues[0])+','+str(0.01)+',OFF,OFF,OFF,'+_pause_bool)
            print(self.getErrorQueue())
        
        # load steps
        for ii in range(0,seqNumStep):
            if(ii==0):
                # trigger ON for the first step
                self._inst.write('PROGram:NSPeed:ADD '+str(seqValues[ii])+','+str(seqTimeSteps[ii])+','+_load_bool+',ON,ON,'+_pause_bool)
                ### DEBUG
                if(debugMode):
                    print('PROGram:NSPeed:ADD '+str(seqValues[ii])+','+str(seqTimeSteps[ii])+','+_load_bool+',ON,ON,'+_pause_bool)
                    print(self.getErrorQueue())
            else:
                # trigger = trig_bool
                self._inst.write('PROGram:NSPeed:ADD '+str(seqValues[ii])+','+str(seqTimeSteps[ii])+','+_load_bool+','+_ramp_bool+','+_trig_bool+','+_pause_bool)
                ### DEBUG
                if(debugMode):
                    print('PROGram:NSPeed:ADD '+str(seqValues[ii])+','+str(seqTimeSteps[ii])+','+_load_bool+','+_ramp_bool+','+_trig_bool+','+_pause_bool)
                    print(self.getErrorQueue())
            self.wait()    
        # last step
        ii = seqNumStep
        self._inst.write('PROGram:NSPeed:ADD '+str(idleValue)+','+str(0.01)+',OFF,'+_ramp_bool+',ON,'+_pause_bool)
        
        ### DEBUG
        if(debugMode):
            # count the number of existing steps
            print('PROGram:NSPeed:ADD '+str(idleValue)+','+str(0.01)+',OFF,'+_ramp_bool+',ON,'+_pause_bool)
            print('PROGram:NSPeed:COUNt '+self._inst.query('PROGram:NSPeed:COUNt?'))
            print(self.getErrorQueue())
            
        return self._inst.query('PROGram:NSPeed:COUNt?')

    #%% Configure Sweep
    def executeSweep(self, debugMode=False):
        ### DESCRIPTION
        #   Execute the sweep previously configured by configSweep(...)
        ### INPUTS:
        # debugMode
        #   True - check every step, print error queue, False - just send commands, no checking, no error printing
        
        # execute the sequence
        self._inst.write('PROGram:STATe RUN') # {TRUN|RUN|STOP|PAUSe|CONTinue}
        ### DEBUG
        if(debugMode):
            # count the number of existing steps
            print('executeSweep: Execute NOW')

    #%% cCheck currently executing program
    def checkProgramExec(self):
        ### DESCRIPTION
        #   Return currently executing program
        return self._inst.query('PROGram:EXECuting?')

