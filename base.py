from tkinter import * 
from tkinter import messagebox
from dinamic_distance import *
from data_collection import *


class Base:
    #This init function creates the frames and the button that switches between the 2 frames
    #It also sets the title and the size of the window
    def __init__(self):
        self.currentFrame = "FrameDinamicDistance"
        self.root = Tk()  # create a root widget
        self.root.title("Asteroid deflection with Gravity Tractor")
        self.root.configure(background="grey")
        self.root.geometry("1500x750")


        self.root.minsize(200, 200)
    
        self.FrameData = Frame(self.root, bg="grey", padx=15, pady=15, highlightbackground="black", highlightthickness=2)

        self.FrameDynamic = Frame(self.root, bg="grey", padx=15, pady=15, highlightbackground="black", highlightthickness=2)
        self.FrameDynamic.grid(row=1, column=0, columnspan=2, sticky="nw")

        Label(self.root, text="Asteroid deflection with Gravity Tractor", font=('Helvetica 20 italic'), bg="light blue").grid(row=0, column=0, columnspan=1 ,padx=10, pady=10, sticky='w')
        
        self.SwitchFramesButton=Button(self.root, text="Switch to basic mode", command=lambda:self.switch_frames(), bg="light blue")
        self.SwitchFramesButton.grid(row=0, column=1, padx=10, pady=10)
        
        self.FrameDataCollection = FrameDataCollection(self.root, self.FrameData)
        self.FrameDinamicDistance = FrameDinamicDistance(self.root, self.FrameDynamic)

        self.nameDate = Label(self.root, text='\u00A9 Ilauszky Anna Luca 2023', fg="black", bg="grey")
        self.nameDate.grid(row=2, column=1, padx=10, pady=10, columnspan=2, sticky="ne")

        
	#This function switches between the two frames, depending on which frame is displayed at the moment
    def switch_frames(self):
        if self.currentFrame == "FrameDinamicDistance":
            self.FrameDynamic.grid_remove()
            self.FrameData.grid(row=1, column=0, columnspan=2, sticky="nw")
            self.currentFrame = "FrameDataCollection"
            self.SwitchFramesButton['text'] = 'Switch to slider mode'
        elif self.currentFrame == "FrameDataCollection":
            self.FrameData.grid_remove()
            self.FrameDynamic.grid(row=1, column=0, columnspan=2, sticky="nw")
            self.currentFrame = "FrameDinamicDistance"
            self.SwitchFramesButton['text'] = 'Switch to basic mode'

    def start(self):
        self.root.mainloop()