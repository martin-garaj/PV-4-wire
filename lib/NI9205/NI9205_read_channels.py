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
#%% User Input
numSamples = 25000

deviceName = 'cDAQ1Mod1'
channelAI1 = 'ai3'
channelAI1maxV = 5 # [V]
channelAI1scale = 6
channelAI2 = 'ai7'
channelAI2maxV = 2 # [V]
channelAI2scale = 10
channelAI3 = 'ai19'
channelAI3maxV = 10 # [V]
channelAI3scale = 6

#%% Task
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan(deviceName+"/"+channelAI1, max_val=channelAI1maxV, min_val=-channelAI1maxV)
    task.ai_channels.add_ai_voltage_chan(deviceName+"/"+channelAI2, max_val=channelAI2maxV, min_val=-channelAI2maxV)
    task.ai_channels.add_ai_voltage_chan(deviceName+"/"+channelAI3, max_val=channelAI3maxV, min_val=-channelAI3maxV)
    
    task.timing.cfg_samp_clk_timing(rate=50000, 
                                    active_edge=nidaqmx.constants.Edge.RISING,
                                    sample_mode=nidaqmx.constants.AcquisitionType.FINITE, 
                                    samps_per_chan=numSamples)
    
    print('Readings: ')
    data = task.read(number_of_samples_per_channel=numSamples)
    print(data[0][0:10])
    
data = np.array(data)
tempScale = np.array([channelAI1scale, channelAI2scale, channelAI3scale])
tempScale = np.transpose([tempScale])
data = np.multiply(data, tempScale)
    
plt.close('all')
fig1, ax1 = plt.subplots()
ax1.plot((data[0][0:numSamples]), 'r')
ax2 = ax1.twinx()
ax2.plot((data[1][0:numSamples]), 'b')  
#plt.plot(data[2][0:numSamples], 'y')

plt.figure()
plt.plot(data[0][0:numSamples], data[1][0:numSamples], 'r.', markersize=0.1)

errorV = "{:.2f}".format( (max(data[0][0:numSamples])-min(data[0][0:numSamples]))*1000 )
errorI = "{:.2f}".format( (max(data[1][0:numSamples])-min(data[1][0:numSamples]))*1000 )
print('voltge error =  ' + errorV + '[mV]')
print('current error = ' + errorI + '[mA]')
