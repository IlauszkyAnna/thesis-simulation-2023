from tkinter import * 
from base import *
from modified_trajectory import *
from data_collection import *
import time
import tkinter.messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FrameDinamicDistance:
    def __init__(self, root, frame):
        self.root = root
        self.frame = frame


        options = [
            "Years",
            "Days",
            "Minutes",
            "Seconds"
            ]
                
        self.G=6.67*(10**(-11))

        self.dropdown = StringVar()
        self.dropdown.set(options[0])

        self.dropdown2 = StringVar()
        self.dropdown2.set(options[0])
        
        Label(self.frame, text='Enter the mass of the asteroid in kg:', bg="light blue").grid(row=1, column=1, padx=10, pady=10, sticky='w')
        Label(self.frame, text='Enter the mass of the gravity tractor in kg:', bg="light blue").grid(row=2, column=1, padx=10, pady=10, sticky='w')
        Label(self.frame, text='Enter the maximum distance between the asteroid and the GT:', bg="light blue").grid(row=3, column=1, padx=10, pady=10, sticky='w')
        Label(self.frame, text='Enter the time left:', bg="light blue").grid(row=4, column=1, padx=10, pady=10,sticky='w')
        Label(self.frame, text='Enter the time left for hovering:', bg="light blue").grid(row=5, column=1, padx=10, pady=10, sticky='w')

        dateChanger1 = OptionMenu(self.frame, self.dropdown, *options)
        dateChanger1.grid(row=4, column=3, padx=10, pady=10)
        dateChanger1.config(width=6)
        dateChanger2 = OptionMenu(self.frame, self.dropdown2, *options)
        dateChanger2.grid(row=5, column=3, padx=10, pady=10)
        dateChanger2.config(width=6)

        self.asteroidMass = StringVar(self.root)
        entry = Entry(self.frame, textvariable=self.asteroidMass, width=25, validate="key",\
                    validatecommand=(self.root.register(self.validate_number), "%S"))
        entry.grid(row=1, column=2, padx=10, pady=10, sticky=W)
                
        self.gravityTractorMass = StringVar(self.root)
        entry = Entry(self.frame, textvariable=self.gravityTractorMass, width=25, validate="key",\
                    validatecommand=(self.root.register(self.validate_number), "%S"))
        entry.grid(row=2, column=2, padx=10, pady=10, sticky=W)
                
        self.slider = Scale(self.frame, from_=0, to=1000, length=250,orient=HORIZONTAL, resolution=10)
        self.slider.set(500)
        self.slider.grid(row=3, column=2, padx=10, pady=10, sticky=W, columnspan=2)

        self.timeLeft = StringVar(self.root)
        entry = Entry(self.frame, textvariable=self.timeLeft, width=25, validate="key",\
                    validatecommand=(self.root.register(self.validate_number), "%S"))
        entry.grid(row=4, column=2, padx=10, pady=10, sticky=W)
                
        self.timeForLevitatingLeft = StringVar(self.root)
        entry = Entry(self.frame, textvariable=self.timeForLevitatingLeft, width=25, validate="key",\
                    validatecommand=(self.root.register(self.validate_number), "%S"))
        entry.grid(row=5, column=2, padx=10, pady=10, sticky=W)

        self.calculate_button = Button(self.frame, text="GENERATE OUTPUT FILE", width=97, command = self.calculate_event, state=DISABLED, disabledforeground="light gray", fg='black', bg='slate grey')
        self.calculate_button.grid(row=6, column=1, padx=10, pady=10, columnspan=3, sticky='w')

        self.deflectionAnswerLabel=Label(self.frame, text='', fg="green yellow", bg="grey")
        self.deflectionAnswerLabel.grid(row=7, column=1, padx=10, pady=10, columnspan=2, sticky='w')

        self.root.bind("<KeyRelease>", self.allow_calculation)
        
    

    def validate_number(self,key):
        return key.isdigit()
        
    def allow_calculation(self, event):
        if  len(self.asteroidMass.get()) < 1 or len(self.gravityTractorMass.get()) < 1 or len(self.timeLeft.get()) < 1 or len(self.timeForLevitatingLeft.get()) < 1:
            self.calculate_button.configure(state=DISABLED)
        else:
            self.calculate_button.configure(state=NORMAL)    

    def create_file(self):
        t = time.localtime()
        current_time = time.strftime("%d%m%Y%H%M%S", t)
        filename="GToutput" + current_time + ".txt"
        f = open(filename, "w")
        f.write("input:\n")
        f.write("Asteroid mass: " + self.asteroidMass.get() + "\n")
        f.write("GT mass: " + self.gravityTractorMass.get() + "\n")
        f.write("Max distance: " + str(self.slider.get()) + "\n")
        f.write("Time left: " + str(self.convert_time(int(self.timeLeft.get()),self.dropdown.get())) + "\n")
        f.write("Time left for levitating: " + str(self.convert_time(int(self.timeForLevitatingLeft.get()),self.dropdown2.get())) + "\n")
        convertedRemainingTime = self.convert_to_days(int(self.timeLeft.get()),self.dropdown.get())
        convertedLevitatingTime = self.convert_to_days(int(self.timeForLevitatingLeft.get()),self.dropdown2.get())
        # 1 day = 86 400 sec

        

        figure = plt.Figure(figsize=(5, 4), dpi=100)
        ax = figure.add_subplot(111)
        line = FigureCanvasTkAgg(figure, self.root)
        line.get_tk_widget().grid(row=1, column=4, padx=10, pady=10)
        ax.set_xlabel("Days")
        ax.set_ylabel("Meters")  
        ax.set_title('Time Vs. Deflection')

        for distance in range(10, int(self.slider.get())+1, 10):
            plotTime = []
            plotDistance = []
            for i in range(0,convertedRemainingTime+1):
                plotTime.append(i)
                if i > convertedLevitatingTime:
                    calculatedValue = self.calculate_deflection(i*86400, convertedLevitatingTime*86400, distance)
                    f.write(str(i) + "  " + str(calculatedValue) + "\n")
                    plotDistance.append(calculatedValue)
                else:
                    calculatedValue = self.calculate_deflection(i*86400, i*86400, distance)
                    f.write(str(i) + "  " + str(calculatedValue) + "\n")
                    plotDistance.append(calculatedValue)
            data = {'time': plotTime, 'distance': plotDistance}  
            df = pd.DataFrame(data)
            df = df[['time', 'distance']].groupby('time').sum()
            ax.set_color_cycle(['red', 'black', 'yellow'])
            df.plot(kind='line', legend=True, ax=ax, color='r', fontsize=10)
            ax.legend().remove()


        f.close()
        return filename
    
    def convert_to_days(self, time, unit):
        if unit == 'Years':
            return time * 365
        elif unit == 'Days':
            return time
        elif unit == 'Minutes':
            return time / (24 * 60)
        elif unit == 'Seconds':
            return time / (24 * 3600)
        else:
            print("Not valid")
            return None

    def calculate_deflection(self, timeLeft, timeLeftLev, distance):
        #gravitational force between the asteroid and the GT
        fGravitation=self.G*((int(self.asteroidMass.get())*int(self.gravityTractorMass.get()))/(distance**2))

        #acceleration of the asteroid
        massTogether=int(self.asteroidMass.get())+int(self.gravityTractorMass.get())

        aNEO=fGravitation/massTogether

        #deflection: delta X
        deflection=1.5*aNEO*timeLeftLev*((2*(timeLeft))-timeLeftLev)
        roundedDeflection=round(deflection,6)
        return roundedDeflection


        

    def calculate_event(self):
        if int(self.timeForLevitatingLeft.get()) > int(self.timeLeft.get()):
            tkinter.messagebox.showerror(title="Error", message="Time for hovering left should be less, than the overall time left!")
        else:    
            filename = self.create_file()
            answer="Output file successfully generated: "+ filename
            self.deflectionAnswerLabel.config(text=answer)
            self.deflectionAnswerLabel["state"] = "normal"
            self.create_file()
        


    def convert_time(self, writtenTime, chosenTimeLeft):
        match chosenTimeLeft:
            case "Years":
                return writtenTime*365*24*60*60
            case "Days":
                return writtenTime*24*60*60
            case "Minutes":
                return writtenTime*60
            case "Seconds":
                return writtenTime