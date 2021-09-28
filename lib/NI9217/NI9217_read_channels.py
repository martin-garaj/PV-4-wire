# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 14:14:59 2020

@author: Martin Garaj

INFO:
    Simple test script to retrieve the values from given channels of NI9205. 
    This is to test whether the connections, 
    channel mappings and polarity are correct. 
"""

#%%############################################################################
################################### IMPORTS ###################################
###############################################################################
import pyvisa as visa
import nidaqmx
import matplotlib.pyplot as plt # plotting
import numpy as np


#%%############################################################################
################################# TEST SCRIPT #################################
###############################################################################
numSamples = 5

deviceName = 'cDAQ2Mod1'
channelAI1 = 'ai0'

print('OK 1 -------------------------------------')

#%% Task
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_rtd_chan(
            deviceName+"/"+channelAI1, name_to_assign_to_channel="", min_val=0.0,
            max_val=100.0, units=nidaqmx.constants.TemperatureUnits.DEG_C,
            rtd_type=nidaqmx.constants.RTDType.PT_3750,
            resistance_config=nidaqmx.constants.ResistanceConfiguration.FOUR_WIRE,
            current_excit_source=nidaqmx.constants.ExcitationSource.INTERNAL,
            current_excit_val=0.001, r_0=100.0)
    print('OK 2 -------------------------------------')
    
    #        """
#        Creates channel(s) that use an RTD to measure temperature.
#
#        Args:
#            physical_channel (str): Specifies the names of the physical
#                channels to use to create virtual channels. The DAQmx
#                physical channel constant lists all physical channels on
#                devices and modules installed in the system.
#            name_to_assign_to_channel (Optional[str]): Specifies a name
#                to assign to the virtual channel this function creates.
#                If you do not specify a value for this input, NI-DAQmx
#                uses the physical channel name as the virtual channel
#                name.
#            min_val (Optional[float]): Specifies in **units** the
#                minimum value you expect to measure.
#            max_val (Optional[float]): Specifies in **units** the
#                maximum value you expect to measure.
#            units (Optional[nidaqmx.constants.TemperatureUnits]): 
#                Specifies the units to use to return temperature
#                measurements.
#            rtd_type (Optional[nidaqmx.constants.RTDType]): Specifies
#                the type of RTD connected to the channel.
#            resistance_config (Optional[nidaqmx.constants.ResistanceConfiguration]): 
#                Specifies the number of wires to use for resistive
#                measurements.
#            current_excit_source (Optional[nidaqmx.constants.ExcitationSource]): 
#                Specifies the source of excitation.
#            current_excit_val (Optional[float]): Specifies in amperes
#                the amount of excitation to supply to the sensor. Refer
#                to the sensor documentation to determine this value.
#            r_0 (Optional[float]): Is the sensor resistance in ohms at 0
#                degrees Celsius. The Callendar-Van Dusen equation
#                requires this value. Refer to the sensor documentation
#                to determine this value.
#        Returns:
#            nidaqmx._task_modules.channels.ai_channel.AIChannel:
#            
#            Indicates the newly created channel object.
#        """  
    
#    task.ai_channels.add_ai_voltage_chan(deviceName+"/"+channelAI1)
#    max_val=channelAI1maxV, min_val=-channelAI1maxV
#    task.timing.cfg_samp_clk_timing(rate=100, 
#                                    active_edge=nidaqmx.constants.Edge.RISING,
#                                    sample_mode=nidaqmx.constants.AcquisitionType.FINITE, 
#                                    samps_per_chan=numSamples)
    

    print('Readings: ')
    data = task.read(number_of_samples_per_channel=numSamples)
    print(data)
    
data = np.array(data)

plt.close('all')
fig1, ax1 = plt.subplots()
ax1.plot((data), 'r')

