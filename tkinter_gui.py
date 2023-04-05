from tkinter import * 
from tkinter import messagebox

root = Tk()  # create a root widget
root.title("Asteroid deflection with Gravity Tractor")
root.configure(background="grey")
root.geometry("700x500") 


#TODO
root.minsize(200, 200)  # width, height
root.maxsize(700, 700)

#gravitational constant
G=6.67*(10**(-11))

############################################################################################################################
#dropdown menu options
options = [
"Years",
"Days",
"Minutes",
"Seconds"
]

dropdown = StringVar()
dropdown.set(options[0])

dropdown2 = StringVar()
dropdown2.set(options[0])
#############################################################################################################################
def validate_number(key):
    return key.isdigit()

def calculate_event():
    #gravitational force between the asteroid and the GT
    fGravitation=G*((int(asteroidMass.get())*int(gravityTractorMass.get()))/(int(distance.get())**2))

    #acceleration of the asteroid
    massTogether=int(asteroidMass.get())+int(gravityTractorMass.get())
    aNEO=fGravitation/massTogether

    #deflection: delta X
    chosenTimeLeft = dropdown.get()
    chosenTimeLeft2 = dropdown2.get()
    convertedTimeLeft = convert_time(int(timeLeft.get()),chosenTimeLeft)
    convertedHoveringTimeLeft = convert_time(int(timeForLevitatingLeft.get()),chosenTimeLeft2)
    print(convertedTimeLeft)
    print(convertedHoveringTimeLeft)
    deflection=1.5*aNEO*convertedHoveringTimeLeft*((2*(convertedTimeLeft))-convertedHoveringTimeLeft)
    roundedDeflection=round(deflection,3)
    answer="The deflection after " + str(timeLeft.get()) + " " + dropdown.get().lower()+ " is: " + str(roundedDeflection) + " meters"
    deflectionAnswerLabel.config(text=answer)
    deflectionAnswerLabel["state"] = "normal"
    

def allow_calculation(event):
    if  len(asteroidMass.get()) < 1 or len(gravityTractorMass.get()) < 1 or len(distance.get()) < 1 or len(timeLeft.get()) < 1 or len(timeForLevitatingLeft.get()) < 1:
        calculate_button.configure(state=DISABLED)
    else:
        calculate_button.configure(state=NORMAL)

def convert_time(writtenTime, chosenTimeLeft):
    match chosenTimeLeft:
        case "Years":
            return writtenTime*365*24*60*60
        case "Days":
            return writtenTime*24*60*60
        case "Minutes":
            return writtenTime*60
        case "Seconds":
            return writtenTime




#TODO
#############################################################
root.bind("<KeyRelease>", allow_calculation)


Label(root, text="Asteroid deflection with Gravity Tractor", font=('Helvetica 20 italic'), bg="light blue") \
    .grid(row=0, column=1, columnspan=2 ,padx=10, pady=10)
Label(root, text='Enter the mass of the asteroid in kg:', bg="light blue").grid(row=1, column=1, padx=10, pady=10)
Label(root, text='Enter the mass of the gravity tractor in kg:', bg="light blue").grid(row=2, column=1, padx=10, pady=10)
Label(root, text='Enter the distance between the asteroid and the GT in meters:', bg="light blue").grid(row=3, column=1, padx=10, pady=10)
Label(root, text='Enter the time left:', bg="light blue").grid(row=4, column=1, padx=10, pady=10)
Label(root, text='Enter the time left for hovering:', bg="light blue").grid(row=5, column=1, padx=10, pady=10)
deflectionAnswerLabel=Label(root, text='Here comes the aswer', bg="light blue")
deflectionAnswerLabel.grid(row=7, column=1, padx=10, pady=10, columnspan=2)
dateChanger1 = OptionMenu(root, dropdown, *options)
dateChanger1.grid(row=4, column=3, padx=10, pady=10)
dateChanger1.config(width=6)
dateChanger2 = OptionMenu(root, dropdown2, *options)
dateChanger2.grid(row=5, column=3, padx=10, pady=10)
dateChanger2.config(width=6)

asteroidMass = StringVar(root)
entry = Entry(root, textvariable=asteroidMass, width=25, validate="key",\
            validatecommand=(root.register(validate_number), "%S"))
entry.grid(row=1, column=2, padx=10, pady=10, sticky=W)
 
gravityTractorMass = StringVar(root)
entry = Entry(root, textvariable=gravityTractorMass, width=25, validate="key",\
            validatecommand=(root.register(validate_number), "%S"))
entry.grid(row=2, column=2, padx=10, pady=10, sticky=W)
 
distance = StringVar(root)
entry = Entry(root, textvariable=distance, width=25, validate="key",\
            validatecommand=(root.register(validate_number), "%S"))
entry.grid(row=3, column=2, padx=10, pady=10, sticky=W)

timeLeft = StringVar(root)
entry = Entry(root, textvariable=timeLeft, width=25, validate="key",\
            validatecommand=(root.register(validate_number), "%S"))
entry.grid(row=4, column=2, padx=10, pady=10, sticky=W)
 
timeForLevitatingLeft = StringVar(root)
entry = Entry(root, textvariable=timeForLevitatingLeft, width=25, validate="key",\
            validatecommand=(root.register(validate_number), "%S"))
entry.grid(row=5, column=2, padx=10, pady=10, sticky=W)

calculate_button = Button(root, text="CALCULATE", command = calculate_event, state=DISABLED)
calculate_button.grid(row=6, column=2, padx=10, pady=10, sticky=W)


root.mainloop()