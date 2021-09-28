# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 14:14:59 2020

@author: Martin Garaj

This is script representing the UI-window-2. The window promts the user for 
measured data descriptors, such as file path, file name, meausrement 
information and user defined text fields. These parameters are saved in unique
file and are programatically readible. 
"""

#%%############################################################################
################################### IMPORTS ###################################
###############################################################################
import tkinter 
from tkinter import filedialog
import os

#%%############################################################################
############################## OBJECT DEFINITION ##############################
###############################################################################
#%% Class
class saveDataDialog(object):
    # Init    
    def __init__(self, master, initSelectDir, initFileName, initPVid, initIrrad, initLightSource, initLightPower, initDetail1, initDetail2, initDetail3, width, height):
        # master "window"
        self.master = master
        #%% keep initial values
        self.tempSaveFolder = initSelectDir
        self.tempFileName = initFileName
        self.tempPVid = initPVid
        self.tempIrrad = initIrrad
        self.tempLightSource = initLightSource
        self.tempLightPower = initLightPower
        self.tempDetail1 = initDetail1
        self.tempDetail2 = initDetail2
        self.tempDetail3 = initDetail3

        # set position
        w = width
        h = height
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = ws - w #(ws/2) - (w/2)
        y = 0 #(hs/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        #%% initial values
        self.saveData = False 
        self.newData = False 
        # initial folder
        if(initSelectDir==''):
            self.saveFolder = os.getcwd()
        else:
            self.saveFolder = initSelectDir
        # init file
        if(initFileName==''):
            self.fileName = 'data'
        else:
            self.fileName = initFileName           
        
        # init PV id
        if(initPVid==''):
            self.pvID = 'FTNK-APV-0000100'
        else:
            self.pvID = initPVid   
        # init irradiance
        if(initIrrad==''):
            self.irrad = '1000'
        else:
            self.irrad = initIrrad      
        # init light source
        if(initLightSource==''):
            self.lightSource = 'ecosun'
        else:
            self.lightSource = initLightSource  
        # init light power
        if(initLightPower==''):
            self.lightPower = '75'
        else:
            self.lightPower = initLightPower  
        # init detail 1
        if(initDetail1==''):
            self.detail1 = ''
        else:
            self.detail1 = initDetail1  
        # init detail 2
        if(initDetail2==''):
            self.detail2 = ''
        else:
            self.detail2 = initDetail2
        # init detail 3
        if(initDetail3==''):
            self.detail3 = ''
        else:
            self.detail3 = initDetail3  
        
        #%% populate the master
        # set window title
        self.master.title("Save data?")
        
        # Prompt = save data to
        self.l_saveTo = tkinter.Label( self.master, text="Save to folder " )
        self.l_saveTo.grid(row=1, column=1, sticky='W')
        # Button = Choose folder
        self.b_saveTo = tkinter.Button(self.master, text = "Choose folder", width = 15, height = 1, command = self.chooseDir)
        self.b_saveTo.grid(row=1,column=2, sticky='W')
        self.b_saveTo.width = 100
        # Text = save data to folder
        self.l_saveToFolder = tkinter.Label( self.master, text=self.saveFolder, anchor="e", width = 100)
        self.l_saveToFolder['text'] = self.saveFolder
        self.l_saveToFolder.grid(row=1, column=3, columnspan=2, sticky='W')
        
        # Prompt = save file name
        self.l_saveTo = tkinter.Label( self.master, text="File name: " )
        self.l_saveTo.grid(row=2, column=2, sticky='W')
        # Entry = Save File name
        self.e_saveFile = tkinter.Entry(self.master, width = 50, text = self.fileName)
        self.e_saveFile.insert(0, self.fileName)
        self.e_saveFile.grid(row = 2, column = 3, columnspan=2, sticky='W') 
        # Prompt = file suffix
        self.l_saveTo = tkinter.Label( self.master, text="... _IV.csv / ... _IV.png / ... _info.txt" )
        self.l_saveTo.grid(row=2, column=4, sticky='W')        
        
        # Prompt = measurement details
        self.l_measureDetails = tkinter.Label( self.master, text="Measurement details: ")
        self.l_measureDetails.grid(row=3, column=2, sticky='W')    
    
        # Prompt = pvID
        self.l_pvID = tkinter.Label( self.master, text="PV device [DTU ID]: ")
        self.l_pvID.grid(row=4, column=3, sticky='W')
        # Entry = pvID
        self.e_pvID = tkinter.Entry(self.master, width = 50)
        self.e_pvID.insert(0, self.pvID)
        self.e_pvID.grid(row = 4, column = 4, sticky='W')    
    
        # Prompt = irrad
        self.l_irrad = tkinter.Label( self.master, text="Irradiance [W/m^2] : ")
        self.l_irrad.grid(row=5, column=3, sticky='W')
        # Entry = irrad
        self.e_irrad = tkinter.Entry(self.master, width = 50 )
        self.e_irrad.insert(0, self.irrad)
        self.e_irrad.grid(row = 5, column = 4, sticky='W')
        
        # Prompt = lightSource
        self.l_lightSource = tkinter.Label( self.master, text="Light source [name] : ")
        self.l_lightSource.grid(row=6, column=3, sticky='W')
        # Entry = lightSource
        self.e_lightSource = tkinter.Entry(self.master, width = 50)
        self.e_lightSource.insert(0, self.lightSource)
        self.e_lightSource.grid(row = 6, column = 4, sticky='W')
        
        # Prompt = lightPower
        self.l_lightPower = tkinter.Label( self.master, text="Light power [W,%,#] : ")
        self.l_lightPower.grid(row=7, column=3, sticky='W')
        # Entry = lightPower
        self.e_lightPower = tkinter.Entry(self.master, width = 50)
        self.e_lightPower.insert(0, self.lightPower)
        self.e_lightPower.grid(row = 7, column = 4, sticky='W')        
        
        # Prompt = detail1
        self.l_detail1 = tkinter.Label( self.master, text="Detail 1 [text] : ")
        self.l_detail1.grid(row=8, column=3, sticky='W')
        # Entry = lightPower
        self.e_detail1 = tkinter.Entry(self.master, width = 50)
        self.e_detail1.insert(0, self.detail1)
        self.e_detail1.grid(row = 8, column = 4, sticky='W')     
        
        # Prompt = detail2
        self.l_detail2 = tkinter.Label( self.master, text="Detail 2 [text] : ")
        self.l_detail2.grid(row=9, column=3, sticky='W')
        # Entry = lightPower
        self.e_detail2 = tkinter.Entry(self.master, width = 50)
        self.e_detail2.insert(0, self.detail2)
        self.e_detail2.grid(row = 9, column = 4, sticky='W')           
        
        # Prompt = detail3
        self.l_detail3 = tkinter.Label( self.master, text="Detail 3 [text] : ")
        self.l_detail3.grid(row=10, column=3, sticky='W')
        # Entry = lightPower
        self.e_detail3 = tkinter.Entry(self.master, width = 50)
        self.e_detail3.insert(0, self.detail3)
        self.e_detail3.grid(row = 10, column = 4, sticky='W')       


        ### save data
        # Button = save data
        self.b_measure = tkinter.Button(self.master,text='Save data', width = 20, height = 3, command = self.clickSave, bg="green", fg='black')
        self.b_measure.grid(row=11, column=2)
        self.b_measure.width = 100
        
        # Button = dont save data
        self.b_measure = tkinter.Button(self.master,text='DONT SAVE', width = 20, height = 3, command = self.clickDontSave, bg="red", fg='black')
        self.b_measure.grid(row=11, column=4)
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
        self.e_saveFile.focus()
        self.e_saveFile.icursor(100)    
    
    
    def chooseDir(self):
        self.saveFolder =  filedialog.askdirectory(parent=self.master, initialdir=self.saveFolder, title='Select directory to save the measured data')
        self.l_saveToFolder["text"] = self.saveFolder
        
    def clickSave(self):
        # flag to save data
        self.saveData = True
        # flag to update data
        self.newData = False     
        # these data are assumed to be updated every time
        self.saveFolder = self.l_saveToFolder.cget("text")
        self.fileName = self.e_saveFile.get()
        # compare init values with values in the fields
        if(self.e_pvID.get()!=self.tempPVid):
            self.pvID = self.e_pvID.get()
            self.newData = True
        if(self.e_irrad.get()!=self.tempIrrad):
            self.irrad = self.e_irrad.get()
            self.newData = True
        if(self.e_lightSource.get()!=self.tempLightSource):
            self.lightSource = self.e_lightSource.get()
            self.newData = True
        if(self.e_lightPower.get()!=self.tempLightPower):
            self.lightPower = self.e_lightPower.get()
            self.newData = True
        if(self.e_detail1.get()!=self.tempDetail1):
            self.detail1 = self.e_detail1.get()
            self.newData = True
        if(self.e_detail2.get()!=self.tempDetail2):
            self.detail2 = self.e_detail2.get()
            self.newData = True
        if(self.e_detail3.get()!=self.tempDetail3):
            self.detail3 = self.e_detail3.get()
            self.newData = True
        self._quit()
        
    def clickDontSave(self):
        # flag to save data
        self.saveData = False
        # flag to update data
        self.newData = False 
        self.saveFolder = self.tempSaveFolder
        self.fileName = self.tempFileName
        self.pvID = self.tempPVid
        self.irrad = self.tempIrrad
        self.lightSource = self.tempLightSource
        self.lightPower = self.tempLightPower
        self.detail1 = self.tempDetail1
        self.detail2 = self.tempDetail2
        self.detail3 = self.tempDetail3
        self._quit()

    def onClosing(self):
        # flag to save data
        self.saveData = False
        # flag to update data
        self.newData = False 
        self.saveFolder = self.tempSaveFolder
        self.fileName = self.tempFileName
        self.pvID = self.tempPVid
        self.irrad = self.tempIrrad
        self.lightSource = self.tempLightSource
        self.lightPower = self.tempLightPower
        self.detail1 = self.tempDetail1
        self.detail2 = self.tempDetail2
        self.detail3 = self.tempDetail3
        self._quit()
        
    def _quit(self):
        self.master.quit()
        self.master.destroy()
        
    def _from_rgb(self, rgb):
        """ from: https://stackoverflow.com/questions/51591456/can-i-use-rgb-in-tkinter/51592104 """
        """ translates an rgb tuple of int to a tkinter friendly color code """
        return "#%02x%02x%02x" % rgb  
