# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 14:14:59 2020

@author: Martin Garaj

This is top script controlling the IV characterization. 
Running this script manages the connected devices, 
provides user interface dialogues and saves the data given the used data.
"""
#%%############################################################################
############################### VERSION CONTROL ###############################
###############################################################################
scriptName = 'TopScript.py'

#%%############################################################################
################################### IMPORTS ###################################
###############################################################################
# pyVISA
import pyvisa as visa
# python libraries
import numpy as np # arrays and operations on arrays
import matplotlib.pyplot as plt # plotting
import time
import json
import tkinter

# custom libraries for connected hardware
import lib.KikusuiPLZ164WA.device as libKikusuiPLZ164WA
import lib.BKPrecision9202.device as libBK9202
import lib.NI9205.device as libNI9205
import lib.NI9217.device as libNI9217
# custom libraries for user input
import lib.dialogPerformMeasurement.performMeasurement_v1 as libUserInputPerfMeasure
import lib.dialogSaveData.saveDataDialog_v1 as libUserInputSaveDialog

#%%############################################################################
############################### DEFAULT VALUES ################################
###############################################################################
# below are default values that appear in user-interface window. 
# There is no need to change these values in code, sine the user is prompted 
# to chenge them, before the actual measurement is performed.
### Initial values for libUserInputPerfMeasure.performMeasurement
tempPerformMeasurement = False
tempNewDataMeasurement = False
tempPosVoltage  = 0.0  # [V]
tempPosSteps    = 10   # [#]
tempPosTime     = 0.7  # [s]
tempNegVoltage  = -1.0 # [V]
tempNegSteps    = 5    # [#]
tempNegTime     = 0.2  # [s]
tempRampBool    = 1    # [bool] 0=steps, 1=sweep
windowUserMeasureWidth  = 700 # [px]
windowUserMeasureHeigth = 250 # [px]

### Initial values for libUserInputSaveDialog.saveDataDialog
tempSaveData        = False
tempSaveFolder      = ''
tempfileName        = 'data_ID_time_user'
tempPVid            = 'DUT-ID'
tempIrrad           = '1000'
tempLightSource     = 'artificial Sun system 1'
tempLightPower      = '75[%]'
tempDetail1         = 'user defined text 1'
tempDetail2         = 'user defined text 2'
tempDetail3         = 'user defined text 3'
windowUserSaveWidth = 1200 # [px]
windowUserSaveHeigth= 375 # [px]

### ignore devices (testing)
# True = USB communication is active
# False = script runs with fake communication to test user interaction
activeDevices = True

#%%############################################################################
############################## DEVICE PARAMETERS ##############################
###############################################################################
# Electronic load: KikusuiPLZ
KikusuiPLZaddress = 'USB0::0x0B3E::0x1005::LA001385::INSTR'

# Power source: BK9202
BK9202address = 'USB0::0xFFFF::0x9200::802204020746810020::INSTR'
currentLimit  = 15 # max current [V]
voltageMargin = 3.0 # voltage margin, which will be the minimum value at the el. load, when the PV device is in reverse bias

# Measurement card: NI9205
deviceNameMeasure = 'cDAQ2Mod1'
channelsMeasure   = ['ai3', 'ai7'] # inputs on Ni9205 for voltage and current
samplingRate      = 20000 # [Hz] = sampling frequency
sample            = 60000 # [#] =total  number of acquired samples
maxVals           = [5,      2] # limit of the range (e.g. 2 = +/-2[V], maximum value is 10, which is +/-10[V]) of the NI9205 inputs
scale             = [5.155, 10] # scale of the acquired signal (e.g. voltage divider 1:5.155 reqiures multiplication by 5.155)

# Measurement card: NI9217
deviceNameTemp    = 'cDAQ1Mod1'
channelTemp       = 'ai0' # ['ai0'] # temperature using PT100, 4-wire thermocouple

#%%############################################################################
############################### pyVISA MANAGER ################################
###############################################################################
if(activeDevices):
    # resource manager
    print('VISA Driver: checkpoint 1')
    RM = visa.ResourceManager()
    print('VISA Driver: checkpoint 2')
    RM.list_resources()
    print('VISA Driver: checkpoint 3')
    # Electronic load
    KikusuiPLZ = libKikusuiPLZ164WA.KikusuiPLZ164WA(RM, KikusuiPLZaddress, debugMode=False)
    # power source
    BK9202 = libBK9202.BKPrecision9202(RM, BK9202address, debugMode=True)
    # NI
    NI9205 = libNI9205.NI9205(deviceNameMeasure)
    NI9217 = libNI9217.NI9217(deviceNameTemp)
    print('VISA Driver: check COMPLETE')
else:
    print('VISA Driver: SKIPPED, devices not active, only user-interface is tested')

try:
    # initialization bool
    initializedBOOL = False # the initialization was not performed
    
    # run indefinitely 
    while(True):
        
        if(not(initializedBOOL)): # initialization was not perfromed
            if(activeDevices):
                ### Set devices to known state
                #%% KikusuiPLZ
                KikusuiPLZ.reset()
                KikusuiPLZ.configDeviceRemote(voltageRange='HIGH', currentRange='HIGH', outputFunc='CV', debugMode=False)
                KikusuiPLZ.wait()
                errors = KikusuiPLZ.getErrorQueue()
                print('Kikusui errors: ')
                print(errors)
                
                #%% BK9202
                BK9202.reset()
                BK9202.configDeviceRemote(debugMode=False)
                BK9202.setCurrentLimit(currentLimit, debugMode=False)
                BK9202.setVoltage(5.0, debugMode=False)
                BK9202.enableOutput(True, debugMode=False)
                BK9202.wait()
                print('INIT: Devices initialized')
                
                #%% Perform intial measurement (to determine voltage/current offset)
                print('INIT: Initial measuremnt')
                ### let the voltage and current settle down (e.g. due to capacitors)
                time.sleep(3.0)
                ### NI9217 - measure temperature
                measTemperature = np.median( np.array( NI9217.measure(channel=channelTemp, samples=1, debugMode=False) ) )
                ### NI9205 - measure V_oc of the PV device
                data = NI9205.measure(channels=channelsMeasure, maxVals=maxVals, samplingRate=1000, samples=1000, debugMode=False)
                VpvDevice = np.mean(data[0][:])*scale[0]
                ### BK9202 - measure voltage at power source
                VpowerSource = BK9202.measureVolatge()
                ### KikusuiPLZ - measure voltage at el. load
                VelecLoad = KikusuiPLZ.measureVolatge()
                print('   Temperature of PV device =  ' + str(measTemperature)  + ' [degC]')
                print('   Voltage of PV device     =  ' + str(VpvDevice)        + ' [V]')
                print('   Voltage of Power Source  =  ' + str(VpowerSource)     + ' [V]')
                print('   Voltage El. load         =  ' + str(VelecLoad)        + ' [V]')
                # disable voltage output
                BK9202.enableOutput(False, debugMode=False)
            else:
                print('   Temperature of PV device =  ' + str(0.0)  + ' [degC]')
                print('   Voltage of PV device     =  ' + str(0.0)  + ' [V]')
                print('   Voltage of Power Source  =  ' + str(0.0)  + ' [V]')
                print('   Voltage El. load         =  ' + str(0.0)  + ' [V]')
        
        #%% Get user input to perform measurement
        print('-----------------------------------------------------------------')
        windowUserMeasure = tkinter.Tk()
        dialogUserMeasure = libUserInputPerfMeasure.performMeasurement(
                                windowUserMeasure, # master window
                                tempPosVoltage, # positive voltage
                                tempPosSteps, # number of steps
                                tempPosTime, # time [s]
                                tempNegVoltage, # negative voltage
                                tempNegSteps, # number of steps
                                tempNegTime, # time [s]
                                tempRampBool, # ramp=0 / sweep=1
                                windowUserMeasureWidth, # [px]
                                windowUserMeasureHeigth) # [px]
        # User Input for measurement parameters
        windowUserMeasure.mainloop()
        # preserve the input
        tempPerformMeasurement  = dialogUserMeasure.performMeasurement
        tempNewDataMeasurement  = dialogUserMeasure.newData
        tempPosVoltage          = float( dialogUserMeasure.posVoltage )
        tempPosSteps            = int( dialogUserMeasure.posSteps )
        tempPosTime             = float( dialogUserMeasure.posTime )
        tempNegVoltage          = float( dialogUserMeasure.negVoltage )
        tempNegSteps            = int( dialogUserMeasure.negSteps )
        tempNegTime             = float( dialogUserMeasure.negTime )
        tempRampBool            = int( dialogUserMeasure.rampBool )
        # delete dialog
        del windowUserMeasure
        del dialogUserMeasure
        
        # check if the user provided initialization parameters
        if(initializedBOOL==False and tempNewDataMeasurement==False):
            print('Initial dialog for measurement MUST BE FILLED IN! \
                  This is a safety feature to prevent the user from running \
                  the program without properly setting up the parameters. \
                  Exiting program!')
            break
        else:
            initializedBOOL = True # Never repeat initialization

        #%% Perform measurement
        if(tempPerformMeasurement==True):
            #%% Check for change in data
            if(tempNewDataMeasurement==True):
                #%% Recalculate perturbation vector
                # Reverse perturbation vector
                perturbVreverse = np.linspace(voltageMargin, # start at minimum voltage, which is the power source margin of 3
                                              abs(tempNegVoltage)+voltageMargin-0.3,
                                              tempNegSteps)
                # prevent dision by zero
                if(tempNegSteps != 0):
                    perturbTreverse= np.ones(tempNegSteps)*(tempNegTime/tempNegSteps)
                else:
                    perturbTreverse= np.ones(0)
                # Forwards perturbation vector
                perturbVforward = np.linspace(abs(tempNegVoltage)+voltageMargin,
                                              abs(tempNegVoltage)+voltageMargin+tempPosVoltage+0.3,
                                              tempPosSteps)
                if(tempPosSteps != 0):
                    perturbTforward = np.ones(tempPosSteps)*(tempPosTime/tempPosSteps)
                else:
                    perturbTforward= np.ones(0)
                    
                ### final voltage perturbation vector
                perturbV = np.concatenate((perturbVreverse, perturbVforward))
                ### final time perturbation vector
                perturbT = np.concatenate((perturbTreverse, perturbTforward))
                ### total perturbation time
                fPertTime = np.sum(perturbT)
                
                print('Perturbation steps:')
                np.set_printoptions(precision=1)
                print(perturbV) 
                
                if(activeDevices):
                    ### Update Kikusui (only if there is any change)
                    if(abs(tempNegVoltage)+voltageMargin < 14.5): # just below 15 [V], which is operating limit for "LOW" voltage mode
                        KikusuiPLZ.configSweep(idleValue=abs(tempNegVoltage)+voltageMargin+tempPosVoltage+0.3, 
                                        rampBool=tempRampBool, seqID=1, seqName='perturb V', seqOutputFunc='NCV', 
                                        seqVoltageRange='LOW', seqCurrentRange='HIGH', seqLoop=1, 
                                        seqValues=perturbV, seqTimeSteps=perturbT,
                                        debugMode=False)
                    else:
                        KikusuiPLZ.configSweep(idleValue=abs(tempNegVoltage)+voltageMargin+tempPosVoltage+0.3, 
                                        rampBool=tempRampBool, seqID=1, seqName='perturb V', seqOutputFunc='NCV', 
                                        seqVoltageRange='HIGH', seqCurrentRange='HIGH', seqLoop=1, 
                                        seqValues=perturbV, seqTimeSteps=perturbT,
                                        debugMode=False)
                    KikusuiPLZ.wait()
                    
                    ### Update Power Source
                    BK9202.setVoltage(abs(tempNegVoltage)+voltageMargin, debugMode=False)                    
                else:
                    print('Programming Kikusui and BK9202 SKIPPED, devices not active')

                
            #%% Perform measurement
            if(activeDevices):
                # Enable voltage output
                BK9202.enableOutput(True, debugMode=False)
                BK9202.wait()
                # measure temperature
                measTemperature = np.median( np.array( NI9217.measure(channel=channelTemp, samples=1, debugMode=False) ) )
                # Start the sweep
                KikusuiPLZ.executeSweep(debugMode=False)
                time.sleep(0.5)
                # Start the measurement
                rawData = NI9205.measure(channels=channelsMeasure, maxVals=maxVals, samplingRate=samplingRate, samples=sample, debugMode=False)
                # wait until the end
                KikusuiPLZ.wait()
                
                # turn off power source
                BK9202.enableOutput(False, debugMode=False)
            else:
                # use fake data to populate user-interface
                measTemperature = 0.0
                rawData = [[0.01,0.02,0.03,0.04,0.05], [1.0,0.9,0.6,0.3,0.1]]
            
            #%% Process raw data
            ### Arrange the data into array and scale them
            rawData = np.array(rawData)
            # detect first sample of perturbed current 
            sampleStart = np.argmax(rawData[1][:]>0.1)
            sampleEnd = int(1.04*samplingRate*fPertTime) + sampleStart
            
            data = rawData[:, sampleStart:sampleEnd]
        
            tempScale = np.array(scale)
            tempScale = np.transpose([tempScale])
            data = np.multiply(data, tempScale)
            data = data.transpose()
            
            #%% Plot          
            # plot the measured data for visual check
            plt.close('all')
    
            fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(8, 6), dpi=150)
            fig.suptitle('Measurement at '+"{:.2f}".format(measTemperature)+' [degC] (title is updated upon saving the data)')
            # IV char
            ax[0].plot(data[:, 0], data[:, 1], 'k', linewidth=0.1)
            ax[0].set_ylabel ('Current [A]',color='k')
            ax[0].set_xlabel ('Voltage [V]',color='k')  
            ax[0].set_xlim(tempNegVoltage, tempPosVoltage) # [V]
            ax[0].set_ylim(0, currentLimit) # [A]
            # sampled data
            ax[1].plot(np.linspace(0, fPertTime*1.04, len(data[:,0])).transpose(), data[:, 0], 'b', linewidth=0.1)
            ax[1].set_ylabel('Voltage [V]',color='k')
            ax11 = ax[1].twinx()
            ax11.plot(np.linspace(0, fPertTime*1.04, len(data[:,0])).transpose(), data[:, 1], 'r', linewidth=0.1)
            ax11.set_ylabel('Current [A]',color='k')
            ax[1].set_xlabel('Time [s]',color='k')
            # show the plot
            plt.show()

            #%% Get user input to save the data         
            windowUserSave = tkinter.Tk()
            dialogUserSave = libUserInputSaveDialog.saveDataDialog(
                                    windowUserSave, # master window
                                    tempSaveFolder,
                                    tempfileName,
                                    tempPVid, # DTU ID
                                    tempIrrad, # irradiance
                                    tempLightSource, # light source name
                                    tempLightPower, # light source power
                                    tempDetail1, # detail 1
                                    tempDetail2, # detail 2
                                    tempDetail3, # detail 3
                                    windowUserSaveWidth, # [px]
                                    windowUserSaveHeigth) # [px]
            # User Input for measurement parameters
            windowUserSave.mainloop()
            # preserve the input
            tempSaveFolder          = dialogUserSave.saveFolder
            tempfileName            = dialogUserSave.fileName
            tempSaveData            = dialogUserSave.saveData
            # tempNewData             = dialogUserSave.newData
            tempPVid                = dialogUserSave.pvID
            tempIrrad               = dialogUserSave.irrad
            tempLightSource         = dialogUserSave.lightSource
            tempLightPower          = dialogUserSave.lightPower
            tempDetail1             = dialogUserSave.detail1
            tempDetail2             = dialogUserSave.detail2
            tempDetail3             = dialogUserSave.detail3
            # delete dialog
            del windowUserSave
            del dialogUserSave
            
            #%% info STRUCTURE
            ### info                  : STRUCT info 
            #       PV                   : STRUCT PV device
            #           id                  : ID of the sample
            #           info                    : info STRUCTURE
            #               detail1             : detail/note 1
            #               detail2             : detail/note 2
            #               detail3             : detail/note 3
            #       irr                  : STRUCT irradiation
            #           value               : intended value of irradiance reaching the PV device
            #           source              : STRUCT source
            #               name                : name of the light source
            #               power               : power of the light source Atlas[%], Newport[W]
            #       temp                : STRUCT temperature
            #           value               : PV device temperature
            #       perturb             : STRUCT perturbation parameters
            #            scriptName         : Name of THIS script
            #            posVoltage         : parameter from measurement dialog
            #            posSteps
            #            posTime
            #            negVoltage
            #            negSteps
            #            negTime
            #            ramp

            ### info.PV
            info_PV_id   = tempPVid
            info_PV_info = {"detail1"           : tempDetail1,
                            "detail2"           : tempDetail2,
                            "detail3"           : tempDetail3}
            ### info.PV
            info_PV = {"id"      :   info_PV_id,
                       "info"    :   info_PV_info}
            ### info.irr
            info_irr_source = {"name"        : tempLightSource,
                               "power"       : tempLightPower}
            ### info.irr
            info_irr = {"value"     : tempIrrad,
                        "source"    : info_irr_source}
            ### info.temp
            # info. temp.value
            info_temp = {"value"    : measTemperature}
            ### info.perturb
            info_perturb = {"scriptName"        : scriptName,
                            "posVoltage"        : tempPosVoltage,
                            "posSteps"          : tempPosSteps,
                            "posTime"           : tempPosTime,
                            "negVoltage"        : tempNegVoltage,
                            "negSteps"          : tempNegSteps,
                            "negTime"           : tempNegTime,
                            "ramp"              : tempRampBool}
            ### info
            info = {"PV"        :   info_PV,
                    "irr"       :   info_irr,
                    "temp"      :   info_temp,
                    "perturb"   :   info_perturb}
            
            #%% Save data
            if(tempSaveData==True):
                # ADD the figure title
                fig.suptitle(tempPVid+' ('+tempDetail1+') at '+"{:.2f}".format(measTemperature)+' [degC] / '+str(tempIrrad)+' [W/m^2]')
                # save as JSON
                infoName = tempSaveFolder+'\\'+tempfileName+'_info.txt'
                with open(infoName, 'w') as outfile:
                    json.dump(info, outfile, indent=2)            
                # save CSV
                fileName = tempSaveFolder+'\\'+tempfileName+'_IV.csv'
                np.savetxt(fileName, data, '%10.5f', delimiter=",")
                # save PNG
                plt.savefig(tempSaveFolder+'\\'+tempfileName+'_IV.png')
                # console print
                print('Data saved as ' +tempfileName+' ... _IV.csv / ... _IV.png / ... _info.txt')
            else:
                # console print
                print('Data NOT saved!')

        else: 
            if(activeDevices):
                BK9202.enableOutput(False, debugMode=False)
                # close connections
                del KikusuiPLZ
                del BK9202
                RM.close()
            else:
                print('END OF PROGRAM')
            break # exit the main loop
            

#%% close ResourceManager if device communication failed
except visa.VisaIOError as e:
    if(activeDevices):
        BK9202.enableOutput(False, debugMode=False)
        #%% Visa - disconect
        del KikusuiPLZ
        del BK9202
        RM.close()
        # print exception handling
        print(e.args)
        print(RM.last_status)
        print(RM.visalib.last_status)
    else:
        print('END OF PROGRAM')
