# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 14:14:59 2020

@author: Martin Garaj

This is script representing the NI9217 as a software object. 
"""

#%%############################################################################
################################### IMPORTS ###################################
###############################################################################
import pyvisa as visa
import nidaqmx
import numpy as np


#%%############################################################################
############################## OBJECT DEFINITION ##############################
###############################################################################
class NI9217(object):
    """A class representing NI9217 module."""

    #%% Class varables
    _deviceName = None # device name as seen by NI MAX

    #%% Constructor
    def __init__(self, deviceName, debugMode=False):
        self._deviceName = deviceName

    #%% Measure channels
    def measure(self, channel, samples=1, debugMode=False):
        #%% Task
        with nidaqmx.Task() as task:
            # perform a simple measurement using PT100 4-wire temperature measurement
            task.ai_channels.add_ai_rtd_chan(
                    self._deviceName+"/"+channel, name_to_assign_to_channel="", min_val=0.0,
                    max_val=100.0, units=nidaqmx.constants.TemperatureUnits.DEG_C,
                    rtd_type=nidaqmx.constants.RTDType.PT_3750,
                    resistance_config=nidaqmx.constants.ResistanceConfiguration.FOUR_WIRE,
                    current_excit_source=nidaqmx.constants.ExcitationSource.INTERNAL,
                    current_excit_val=0.001, r_0=100.0)
    
            if(debugMode):
                print('NI9217.measure(): start')
            # perform the measuremnt
            data = task.read(number_of_samples_per_channel=samples)
            if(debugMode):
                print('NI9217.measure(): end')
            return data
