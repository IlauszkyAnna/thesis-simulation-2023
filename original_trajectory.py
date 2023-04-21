from tkinter import * 
from base import *

class FrameOriginalTrajectory:
    def __init__(self, root, frame):
        self.root = root
        self.frame = frame

        Label(self.frame, text='TEESSST', bg="light blue").grid(row=0, column=0, padx=10, pady=10, sticky='w')