from tkinter import * 
from tkinter import messagebox
from dinamic_distance import *
from data_collection import *
from modified_trajectory import *


class Base:
    def __init__(self):
        self.root = Tk()  # create a root widget
        self.root.title("Asteroid deflection with Gravity Tractor")
        self.root.configure(background="grey")
        self.root.geometry("800x500") 


        self.root.minsize(200, 200)
        self.root.maxsize(800, 1000)

    
        #self.FrameDataCollection = Frame(self.root, bg="grey", padx=15, pady=15, highlightbackground="black", highlightthickness=2)
        #self.FrameDataCollection.grid(row=1, column=0, columnspan=2)

        



        self.FrameDinamicDistance = Frame(self.root, bg="grey", padx=15, pady=15, highlightbackground="black", highlightthickness=2)
        self.FrameDinamicDistance.grid(row=1, column=0)

        #self.FrameModifiedTrajectory = Frame(self.root, bg="grey", padx=15, pady=15, highlightbackground="black", highlightthickness=2)
        #self.FrameModifiedTrajectory.grid(row=2, column=1)

        Label(self.root, text="Asteroid deflection with Gravity Tractor", font=('Helvetica 20 italic'), bg="light blue").grid(row=0, column=0, columnspan=1 ,padx=10, pady=10, sticky='w')
        
        #SwitchFramesButton=Button(self.root, text="Switch to the other mode", command=FrameDinamicDistance.switchFrames(self,"dinamicPage"), bg="light blue")
        #SwitchFramesButton.grid(row=0, column=1, padx=10, pady=10)
        
        
        #self.FrameDataCollection = FrameDataCollection(self.root, self.FrameDataCollection)
        self.FrameDinamicDistance = FrameDinamicDistance(self.root, self.FrameDinamicDistance)
        #self.FrameModifiedTrajectory = FrameModifiedTrajectory(self.root, self.FrameModifiedTrajectory)
        
	

    def start(self):
        self.root.mainloop()