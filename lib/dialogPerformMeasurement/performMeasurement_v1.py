# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 14:14:59 2020

@author: Martin Garaj

This is script representing the UI-window-1. The window promts the user for 
measurement related parameters (e.g. positive and negative voltage) and 
the period of sweep
"""

#%%############################################################################
################################### IMPORTS ###################################
###############################################################################
import tkinter

#%%############################################################################
############################## OBJECT DEFINITION ##############################
###############################################################################
#%% Class
class performMeasurement(object):

    # Init    
    def __init__(self, master, initPosVoltage, initPosSteps, initPosTime, initNegVoltage, initNegSteps, initNegTime, initRampBool, width, height):
        # master "window"
        self.master = master
        #%% keep initial values
        self.tempPosVoltage = initPosVoltage
        self.tempPosSteps   = initPosSteps
        self.tempPosTime    = initPosTime
        self.tempNegVoltage = initNegVoltage
        self.tempNegSteps   = initNegSteps
        self.tempNegTime    = initNegTime
        self.tempRampBool   = initRampBool
        
        # set size
        # set position
        w = width
        h = height
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        #%% initial values
        self.performMeasurement = False 
        self.newData = False 
        
        # initial folder
        if(initPosVoltage==''):
            self.posVoltage = str(0.0)
        else:
            self.posVoltage = str( initPosVoltage )
        # init file
        if(initPosSteps==''):
            self.posSteps = str(0)
        else:
            self.posSteps = str( initPosSteps )
        # init file
        if(initPosTime==''):
            self.posTime = str(0.0)
        else:
            self.posTime = str( initPosTime )
            
        # initial folder
        if(initNegVoltage==''):
            self.negVoltage = str(0.0)
        else:
            self.negVoltage = str( initNegVoltage )
        # init file
        if(initNegSteps==''):
            self.negSteps = str(0)
        else:
            self.negSteps = str( initNegSteps )
        # init file
        if(initNegTime==''):
            self.negTime = str(0.0)
        else:
            self.negTime = str( initNegTime )
        
        # init file
        self.rampBool = initRampBool
        
        #%% populate the master
        # set window title
        self.master.title("Perform measurement?")
        
        # positive voltage
        self.l_posVoltage = tkinter.Label( self.master, text="Positive voltage:" )
        self.l_posVoltage.grid(row=1, column=1, sticky='W')
        # Prompt = posVoltage
        self.l_posVoltage = tkinter.Label( self.master, text="max(V) = " )
        self.l_posVoltage.grid(row=2, column=2, sticky='W')
        # Entry = posVoltage
        self.e_posVoltage = tkinter.Entry(self.master, width = 6, text = self.posVoltage)
        self.e_posVoltage.insert(0, self.posVoltage)
        self.e_posVoltage.grid(row = 2, column = 3, sticky='W') 
        # Prompt = posSteps
        self.l_posSteps = tkinter.Label( self.master, text="[V]    steps = " )
        self.l_posSteps.grid(row=2, column=4, sticky='W')
        # Entry = posSteps
        self.e_posSteps = tkinter.Entry(self.master, width = 6, text = self.posSteps)
        self.e_posSteps.insert(0, self.posSteps)
        self.e_posSteps.grid(row = 2, column = 5, sticky='W') 
        # Prompt = posTime
        self.l_posTime = tkinter.Label( self.master, text="[#]    time = " )
        self.l_posTime.grid(row=2, column=6, sticky='W')
        # Entry = posTime
        self.e_posTime = tkinter.Entry(self.master, width = 6, text = self.posTime)
        self.e_posTime.insert(0, self.posTime)
        self.e_posTime.grid(row = 2, column = 7, sticky='W') 
        # Prompt = posTime
        self.l_posTimeEnd = tkinter.Label( self.master, text="[s]" )
        self.l_posTimeEnd.grid(row=2, column=8, sticky='W')
        
        
        # negative voltage
        self.l_negVoltage = tkinter.Label( self.master, text="Negative voltage:" )
        self.l_negVoltage.grid(row=3, column=1, sticky='W')
        # Prompt = negVoltage
        self.l_negVoltage = tkinter.Label( self.master, text="min(V) = " )
        self.l_negVoltage.grid(row=4, column=2, sticky='W')
        # Entry = posVoltage
        self.e_negVoltage = tkinter.Entry(self.master, width = 6, text = self.negVoltage)
        self.e_negVoltage.insert(0, self.negVoltage)
        self.e_negVoltage.grid(row = 4, column = 3, sticky='W') 
        # Prompt = negSteps
        self.l_negSteps = tkinter.Label( self.master, text="[V]    steps = " )
        self.l_negSteps.grid(row=4, column=4, sticky='W')
        # Entry = posSteps
        self.e_negSteps = tkinter.Entry(self.master, width = 6, text = self.negSteps)
        self.e_negSteps.insert(0, self.negSteps)
        self.e_negSteps.grid(row = 4, column = 5, sticky='W') 
        # Prompt = posTime
        self.l_negTime = tkinter.Label( self.master, text="[#]    time = " )
        self.l_negTime.grid(row=4, column=6, sticky='W')
        # Entry = posTime
        self.e_negTime = tkinter.Entry(self.master, width = 6, textvariable = self.negTime)
        self.e_negTime.insert(0, self.negTime)
        self.e_negTime.grid(row = 4, column = 7, sticky='W') 
        # Prompt = posTime
        self.l_negTimeEnd = tkinter.Label( self.master, text="[s]" )
        self.l_negTimeEnd.grid(row=4, column=8, sticky='W')
        
        
        # Prompt = Sweep setting
        self.l_negTime = tkinter.Label( self.master, text="Sweep Setting:" )
        self.l_negTime.grid(row=5, column=1, sticky='W')
        # Prompt = save data to
        self.rampCheckBox = tkinter.IntVar()
        self.c_ramp = tkinter.Checkbutton(self.master, text=" ramp", variable=self.rampCheckBox)
        self.rampCheckBox.set(self.rampBool)
        self.c_ramp.grid(row = 6, column = 2, sticky='W')        
        
        # Button = save data
        self.b_measure = tkinter.Button(self.master,text='Measure', width = 10, height = 3, command = self.clickMeasure, bg="green", fg='black')
        self.b_measure.grid(row=7, column=1)
        self.b_measure.width = 100
        
        # Button = dont save data
        self.b_measure = tkinter.Button(self.master,text='END PROGRAM', width = 15, height = 3, command = self.clickEnd, bg="red", fg='black')
        self.b_measure.grid(row=7, column=9)
        self.b_measure.width = 100

        # whne closed by X
        self.master.protocol("WM_DELETE_WINDOW", self.onClosing)
        
        ### grid settings
        self.master.columnconfigure(1, weight=0, minsize=1,  pad=1)
        self.master.columnconfigure(2, weight=0, minsize=1, pad=1)
        
        self.master.rowconfigure(1, weight=0, minsize=1,  pad=5)
        self.master.rowconfigure(2, weight=0, minsize=1, pad=5)
        
        ### focus
        self.master.lift()
        self.master.attributes('-topmost',True)
        self.master.after_idle(self.master.attributes,'-topmost',False)
        self.master.update_idletasks()
        self.master.focus_get()
        self.master.focus_force()   
    
    #%% Button to start the measurement
    def clickMeasure(self):
        # flag to save data
        self.performMeasurement = True
        # flag to update data
        self.newData = False   
        # compare init values with values in the fields
        if(self.e_posVoltage.get()!=str( self.tempPosVoltage )):
            self.posVoltage = float( self.e_posVoltage.get() )
            self.newData = True
        if(self.e_posSteps.get()!=str( self.tempPosSteps )):
            self.posSteps = int( self.e_posSteps.get() )
            self.newData = True
        if(self.e_posTime.get()!=str( self.tempPosTime )):
            self.posTime = float( self.e_posTime.get() )
            self.newData = True
        if(self.e_negVoltage.get()!=str( self.tempNegVoltage )):
            self.negVoltage = float( self.e_negVoltage.get() )
            self.newData = True
        if(self.e_negSteps.get()!=str( self.tempNegSteps )):
            self.negSteps = float( self.e_negSteps.get() )
            self.newData = True
        if(self.e_negTime.get()!=str( self.tempNegTime )):
            self.negTime = float( self.e_negTime.get() )
            self.newData = True
        if(bool( self.rampCheckBox.get() ) != bool( self.tempRampBool )):
            if(self.rampCheckBox.get()):
                self.rampBool = 1
            else:
                self.rampBool = 0
            self.newData = True       
        self._quit()
    
    #%% Button to end the program
    def clickEnd(self):
        # flag to save data
        self.performMeasurement = False
        # flag to update data
        self.newData = False   
        self.posVoltage = float( self.tempPosVoltage )
        self.posSteps = int( self.tempPosSteps )
        self.posTime = float( self.tempPosTime )
        self.negVoltage = float( self.tempNegSteps )
        self.negSteps = int( self.tempNegSteps )
        self.negTime = float( self.tempNegTime )
        self.rampBool = 0
        self._quit()

    #%% Button to close the window
    def onClosing(self):
        # flag to save data
        self.performMeasurement = False
        # flag to update data
        self.newData = False   
        self.posVoltage = float( self.tempPosVoltage )
        self.posSteps = int( self.tempPosSteps )
        self.posTime = float( self.tempPosTime )
        self.negVoltage = float( self.tempNegSteps )
        self.negSteps = int( self.tempNegSteps )
        self.negTime = float( self.tempNegTime )
        self.rampBool = 0
        self._quit()
        
    #%% quit function
    def _quit(self):
        self.master.quit()
        self.master.destroy()
        
    #%% color function
    def _from_rgb(self, rgb):
        """ from: https://stackoverflow.com/questions/51591456/can-i-use-rgb-in-tkinter/51592104 """
        """ translates an rgb tuple of int to a tkinter friendly color code """
        return "#%02x%02x%02x" % rgb  
        