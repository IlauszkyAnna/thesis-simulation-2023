from tkinter import * 
from base import *
from data_collection import *
import time
import tkinter.messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


#This class represents the frame that is used for the Slider mode
class FrameDinamicDistance:
    def __init__(self, root, frame):
        #The init function places all of the Labels, Entries, Buttons, OptionMenus to their given places
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
                
        self.slider = Scale(self.frame, from_=300, to=1000, length=250,orient=HORIZONTAL, resolution=10)
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

        self.calculate_button = Button(self.frame, text="GENERATE OUTPUT FILE", width=97, command = lambda:self.calculate_event(), state=DISABLED, disabledforeground="light gray", fg='black', bg='slate grey')
        self.calculate_button.grid(row=6, column=1, padx=10, pady=10, columnspan=3, sticky='w')

        self.deflectionAnswerLabel=Label(self.frame, text='', fg="green yellow", bg="grey")
        self.deflectionAnswerLabel.grid(row=7, column=1, padx=10, pady=10, columnspan=2, sticky='w')

        self.root.bind("<KeyRelease>", self.allow_calculation)
        
    
    #This function is used, when the user enters a text into one of the entries
    #The users are supposed to only type numbers into the entries
    #The validate_number function returns a boolean:
    #true, if the input only contains numbers, and false if it also contains other characters
    def validate_number(self,key):
        return key.isdigit()

    #This function swithes the state of the calculate_button to normal, if all of the parameters are provided by the user
    # if not, the state of the button remains disabled  
    def allow_calculation(self, event):
        if  len(self.asteroidMass.get()) < 1 or len(self.gravityTractorMass.get()) < 1 or len(self.timeLeft.get()) < 1 or len(self.timeForLevitatingLeft.get()) < 1:
            self.calculate_button.configure(state=DISABLED)
        else:
            self.calculate_button.configure(state=NORMAL)    


    #This function creates a file with a new name, and writes the input data into the file
    #Then it calculates the deflection daily, which is also written into the file
    #With the calculated values, it plots a graph where the time  and the deflection is represented
    #The deflection is calculated for a couple of different distances between the asteroid and the Gravity Tractor
    #The distances start from 300 and the deflection is calculated every 10 meters until the chosen distance
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

        

        figure = plt.Figure(figsize=(7, 6), dpi=100)
        ax = figure.add_subplot(111)
        line = FigureCanvasTkAgg(figure, self.root)
        line.get_tk_widget().grid(row=1, column=4, padx=10, pady=10)
        ax.set_xlabel("Days")
        ax.set_ylabel("Meters")  
        ax.set_title('Time Vs. Deflection')

        colors = ['green', 'blue', 'purple', 'orange', 'brown', 'pink', 'gray', 'olive', 'cyan']

        for distance in range(300, int(self.slider.get())+1, 10):
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
            data = {'Days': plotTime, 'distance': plotDistance}  
            df = pd.DataFrame(data)
            df = df[['Days', 'distance']].groupby('Days').sum()
            df.plot(kind='line', ax=ax, label="hello", fontsize=10, color=colors[distance%len(colors)])
            ax.legend().remove()

        f.close()
        return filename
    
    #This function converts the given time from the given unit to days
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


    #The calculate_deflection returns the deflection calculated from the given parameters
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


        
    #The calculate_event function is called, when the calculate_button is pressed
    #It also calls the create_file function, to write the data to a file and to draw a graph
    #Then it puts the name of the generated file to the screen
    def calculate_event(self):
        if self.convert_to_days(int(self.timeForLevitatingLeft.get()),self.dropdown2.get()) > self.convert_to_days(int(self.timeLeft.get()),self.dropdown.get()):
            tkinter.messagebox.showerror(title="Error", message="Time left for hovering should be less, than the full time left!")
        else:    
            filename = self.create_file()
            answer="Output file successfully generated: "+ filename
            self.deflectionAnswerLabel.config(text=answer)
            self.deflectionAnswerLabel["state"] = "normal"
        

    #This function converts the give writtenTime to the given unit of chosenTimeLeft
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