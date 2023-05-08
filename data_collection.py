from tkinter import *
from base import *
import time
import tkinter.messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#This class represents the frame that is used for the Basic mode
class FrameDataCollection:
    #The init function places all of the Labels, Entries, Buttons, OptionMenus to their given places
    def __init__(self, root, frame):
        self.root = root
        self.frame = frame

        options = [
            "Years",
            "Days",
            "Minutes",
            "Seconds"
        ]

        self.G = 6.67*(10**(-11))

        self.dropdown = StringVar()
        self.dropdown.set(options[0])

        self.dropdown2 = StringVar()
        self.dropdown2.set(options[0])

        Label(self.frame, text='Enter the mass of the asteroid in kg:',
              bg="light blue").grid(row=1, column=1, padx=10, pady=10, sticky='w')
        Label(self.frame, text='Enter the mass of the gravity tractor in kg:',
              bg="light blue").grid(row=2, column=1, padx=10, pady=10, sticky='w')
        Label(self.frame, text='Enter the distance between the asteroid and the GT in meters:',
              bg="light blue").grid(row=3, column=1, padx=10, pady=10, sticky='w')
        Label(self.frame, text='Enter the time left:', bg="light blue").grid(
            row=4, column=1, padx=10, pady=10, sticky='w')
        Label(self.frame, text='Enter the time left for hovering:', bg="light blue").grid(
            row=5, column=1, padx=10, pady=10, sticky='w')

        dateChanger1 = OptionMenu(self.frame, self.dropdown, *options)
        dateChanger1.grid(row=4, column=3, padx=10, pady=10)
        dateChanger1.config(width=6)
        dateChanger2 = OptionMenu(self.frame, self.dropdown2, *options)
        dateChanger2.grid(row=5, column=3, padx=10, pady=10)
        dateChanger2.config(width=6)

        self.asteroidMass = StringVar(self.root)
        entry = Entry(self.frame, textvariable=self.asteroidMass, width=25, validate="key",
                      validatecommand=(self.root.register(self.validate_number), "%S"))
        entry.grid(row=1, column=2, padx=10, pady=10, sticky=W)

        self.gravityTractorMass = StringVar(self.root)
        entry = Entry(self.frame, textvariable=self.gravityTractorMass, width=25, validate="key",
                      validatecommand=(self.root.register(self.validate_number), "%S"))
        entry.grid(row=2, column=2, padx=10, pady=10, sticky=W)

        self.distance = StringVar(self.root)
        entry = Entry(self.frame, textvariable=self.distance, width=25, validate="key",
                      validatecommand=(self.root.register(self.validate_number), "%S"))
        entry.grid(row=3, column=2, padx=10, pady=10, sticky=W)

        self.timeLeft = StringVar(self.root)
        entry = Entry(self.frame, textvariable=self.timeLeft, width=25, validate="key",
                      validatecommand=(self.root.register(self.validate_number), "%S"))
        entry.grid(row=4, column=2, padx=10, pady=10, sticky=W)

        self.timeForLevitatingLeft = StringVar(self.root)
        entry = Entry(self.frame, textvariable=self.timeForLevitatingLeft, width=25, validate="key",
                      validatecommand=(self.root.register(self.validate_number), "%S"))
        entry.grid(row=5, column=2, padx=10, pady=10, sticky=W)

        self.calculate_button = Button(self.frame, text="CALCULATE", width=70, command=self.calculate_event,
                                       state=NORMAL, disabledforeground="light gray", fg='black', bg='slate grey')
        self.calculate_button.grid(
            row=6, column=1, padx=10, pady=10, columnspan=2, sticky='w')

        self.deflectionAnswerLabel = Label(
            self.frame, text='Here comes the answer', bg="light blue")
        self.deflectionAnswerLabel.grid(
            row=7, column=1, padx=10, pady=10, columnspan=2, sticky='w')

        self.fileCreatedLabel = Label(
            self.frame, text='', fg="green yellow", bg="grey")
        self.fileCreatedLabel.grid(
            row=8, column=1, padx=10, pady=10, columnspan=2, sticky='w')

    #This function is used, when the user enters a text into one of the entries
    #The users are supposed to only type numbers into the entries
    #The validate_number function returns a boolean:
    #true, if the input only contains numbers, and false if it also contains other characters
    def validate_number(self, key):
        return key.isdigit()

    #This function returns a boolean, true if all of the data is provided and false if not
    def allow_calculation(self):
        if len(self.asteroidMass.get()) < 1 or len(self.gravityTractorMass.get()) < 1 or len(self.distance.get()) < 1 or len(self.timeLeft.get()) < 1 or len(self.timeForLevitatingLeft.get()) < 1:
            return False
        else:
            return True


    #This function creates a file with a new name, and writes the input data into the file
    #Then it calculates the deflection daily, which is also written into the file
    #With the calculated values, it plots a graph where the time  and the deflection is represented
    def create_file(self):
        t = time.localtime()
        current_time = time.strftime("%d%m%Y%H%M%S", t)
        filename = "GToutput" + current_time + "basic.txt"
        f = open(filename, "w")
        f.write("input:\n")
        f.write("Asteroid mass: " + self.asteroidMass.get() + "\n")
        f.write("GT mass: " + self.gravityTractorMass.get() + "\n")
        f.write("Distance: " + str(int(self.distance.get())) + "\n")
        f.write("Time left: " + str(self.convert_time(int(self.timeLeft.get()),
                self.dropdown.get())) + "\n")
        f.write("Time left for levitating: " + str(self.convert_time(
            int(self.timeForLevitatingLeft.get()), self.dropdown2.get())) + "\n")
        convertedRemainingTime = self.convert_to_days(
            int(self.timeLeft.get()), self.dropdown.get())
        convertedLevitatingTime = self.convert_to_days(
            int(self.timeForLevitatingLeft.get()), self.dropdown2.get())
        # 1 day = 86 400 sec

        figure = plt.Figure(figsize=(7, 6), dpi=100)
        ax = figure.add_subplot(111)
        line = FigureCanvasTkAgg(figure, self.root)
        line.get_tk_widget().grid(row=1, column=4, padx=10, pady=10)
        ax.set_xlabel("Days")
        ax.set_ylabel("Meters")
        ax.set_title('Time Vs. Deflection')

        plotTime = []
        plotDistance = []
        for i in range(0, convertedRemainingTime+1):
            plotTime.append(i)
            if i > convertedLevitatingTime:
                calculatedValue = self.calculate_deflection(
                    i*86400, convertedLevitatingTime*86400, int(self.distance.get()))
                f.write(str(i) + "  " + str(calculatedValue) + "\n")
                plotDistance.append(calculatedValue)
            else:
                calculatedValue = self.calculate_deflection(
                    i*86400, i*86400, int(self.distance.get()))
                f.write(str(i) + "  " + str(calculatedValue) + "\n")
                plotDistance.append(calculatedValue)
        data = {'Days': plotTime, 'distance': plotDistance}
        df = pd.DataFrame(data)
        df = df[['Days', 'distance']].groupby('Days').sum()
        df.plot(kind='line', legend=True, ax=ax, color='r', fontsize=10)
        ax.legend().remove()

        f.close()
        return filename

    #The calculate_deflection returns the deflection calculated from the given parameters
    def calculate_deflection(self, timeLeft, timeLeftLev, distance):
        # gravitational force between the asteroid and the GT
        fGravitation = self.G * \
            ((int(self.asteroidMass.get()) *
             int(self.gravityTractorMass.get()))/(distance**2))

        # acceleration of the asteroid
        massTogether = int(self.asteroidMass.get()) + \
            int(self.gravityTractorMass.get())

        aNEO = fGravitation/massTogether

        # deflection: delta X
        deflection = 1.5*aNEO*timeLeftLev*((2*(timeLeft))-timeLeftLev)
        roundedDeflection = round(deflection, 6)
        return roundedDeflection

    #The calculate_event function is called, when the calculate button is pressed
    #First, it checks if all of the data is provided or not
    #Then it calculates the deflection according to the given parameters, and updates the Label with the results
    #It also calls the create_file function, to write the data to a file and to draw a graph
    def calculate_event(self):
        if self.allow_calculation() == False:
            tkinter.messagebox.showerror(
                title="Error", message="You have not provided all of the data!")
        else:
            if self.convert_to_days(int(self.timeForLevitatingLeft.get()), self.dropdown2.get()) > self.convert_to_days(int(self.timeLeft.get()), self.dropdown.get()):
                tkinter.messagebox.showerror(
                    title="Error", message="Time left for hovering should be less, than the full time left!")
            else:
                # gravitational force between the asteroid and the GT
                fGravitation = self.G*((int(self.asteroidMass.get())*int(
                    self.gravityTractorMass.get()))/(int(self.distance.get())**2))

                # acceleration of the asteroid
                massTogether = int(self.asteroidMass.get()) + \
                    int(self.gravityTractorMass.get())
                aNEO = fGravitation/massTogether

                # deflection: delta X
                chosenTimeLeft = self.dropdown.get()
                chosenTimeLeft2 = self.dropdown2.get()
                convertedTimeLeft = self.convert_time(
                    int(self.timeLeft.get()), chosenTimeLeft)
                convertedHoveringTimeLeft = self.convert_time(
                    int(self.timeForLevitatingLeft.get()), chosenTimeLeft2)
                deflection = 1.5*aNEO*convertedHoveringTimeLeft * \
                    ((2*(convertedTimeLeft))-convertedHoveringTimeLeft)
                roundedDeflection = round(deflection, 3)
                answer = "The deflection after " + str(self.timeLeft.get()) + " " + self.dropdown.get(
                ).lower() + " is: " + str(roundedDeflection) + " meters"
                self.deflectionAnswerLabel.config(text=answer)
                self.deflectionAnswerLabel["state"] = "normal"
                filename = self.create_file()
                answer = "Output file successfully generated: " + filename
                self.fileCreatedLabel.config(text=answer)
                self.fileCreatedLabel["state"] = "normal"

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
