# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 14:14:59 2020

@author: Martin Garaj

This is a simple testing script for testing communication with 
Kikusui PLZ 164 WA. 
"""
#%%############################################################################
################################### IMPORTS ###################################
###############################################################################
import pyvisa as visa
import matplotlib.pyplot as plt # plotting
import device as libKikusuiPLZ164WA


#%%############################################################################
################################# TEST SCRIPT #################################
###############################################################################

# resource manager
RM = visa.ResourceManager()
RM.list_resources()

KikusuiPLZ = libKikusuiPLZ164WA.KikusuiPLZ164WA(RM, 'USB0::0x0B3E::0x1005::LA001385::INSTR', debugMode=True)

try:
    # Prepare KikusuiPLZ
    KikusuiPLZ.reset()
    KikusuiPLZ.configDeviceRemote(remoteSense=1, voltageRange='HIGH', currentRange='HIGH', outputFunc='CV', debugMode=False)
    KikusuiPLZ.wait()
    # Prepare voltage sweep
    KikusuiPLZ.configSweep(idleValue=6.0, seqID=1, seqName='perturb V', seqOutputFunc='NCV', 
                    seqVoltageRange='LOW', seqCurrentRange='HIGH', seqLoop=1, 
                    seqValues=[5.5,5.0,4.5], seqTimeSteps=[1,1,1],
                    debugMode=False)
    KikusuiPLZ.wait()
    errors = KikusuiPLZ.getErrorQueue()
    print(errors)
    # Execute the sweep
    KikusuiPLZ.executeSweep(debugMode=True)   

    del KikusuiPLZ
    RM.close()  
    
except visa.VisaIOError as e:
    #%% Visa - disconect
    del KikusuiPLZ
    RM.close()
    # print exception handling
    print(e.args)
    print(RM.last_status)
    print(RM.visalib.last_status)
