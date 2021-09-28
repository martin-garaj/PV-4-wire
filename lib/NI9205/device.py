# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 14:14:59 2020

@author: Martin Garaj

This is script representing the NI9205 as a software object. 
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
class NI9205(object):
    """A class representing NI9205 module."""

    #%% Class varables
    _deviceName = None # device name as seen by NI MAX

    #%% Constructor
    def __init__(self, deviceName, debugMode=False):
        self._deviceName = deviceName
        
    #%% Measure channels
    def measure(self, channels, maxVals, samplingRate=10000, samples=10000, debugMode=False):
        #%% Task
        with nidaqmx.Task() as task:
            # register aalog channels with their respective limits
            for channel, maxVal in zip(channels, maxVals):
                task.ai_channels.add_ai_voltage_chan(self._deviceName+"/"+channel, max_val=abs(maxVal), min_val=-abs(maxVal))
            # set timing (sampling) for all the channels
            task.timing.cfg_samp_clk_timing(rate=samplingRate, 
                                            active_edge=nidaqmx.constants.Edge.RISING,
                                            sample_mode=nidaqmx.constants.AcquisitionType.FINITE, 
                                            samps_per_chan=samples)
            if(debugMode):
                print('NI9205.measure(): start')
            # perform the measuremnt
            data = task.read(number_of_samples_per_channel=samples)
            if(debugMode):
                print('NI9205.measure(): end')
            return data
