import tkinter as tk
from tkinter import messagebox
  
def add_clinic():
    id = clinic_id.get()
    name = clinic_name.get()
    phone = clinic_phone.get()
 
    # Add to database
 
    clinic_id.set('')
    clinic_name.set('')
    clinic_phone.set('')
    messagebox.showinfo("Confirmation", "Clinic Registered")
 
def validate_phone(key):
    return len(key) == 0 or len(clinic_phone.get()) <= 10 and key.isdigit()
 
def to_upper(var):
    var.set(var.get().upper())
 
def form_complete(event):
    if  len(clinic_id.get()) < 1 or len(clinic_name.get()) < 1 or len(clinic_phone.get()) < 10:
        add_button.configure(state=tk.DISABLED)
    else:
        add_button.configure(state=tk.NORMAL)
 
win = tk.Tk()
win.title("ADD Clinic")
win.geometry("600x300")
win.configure(background='light blue')
win.resizable(False, False)
win.bind("<KeyRelease>", form_complete)
 
tk.Label(win, text="Clinic Details", font=('Helvetica 20 italic'), bg="light blue") \
    .grid(row=0, column=2, padx=10, pady=10)
tk.Label(win, text='Clinic ID.', bg="light blue").grid(row=2, column=1, padx=10, pady=10)
tk.Label(win, text='Clinic Name', bg="light blue").grid(row=3, column=1, padx=10, pady=10)
tk.Label(win, text='Phone No.', bg="light blue").grid(row=4, column=1, padx=10, pady=10)
 
clinic_id = tk.StringVar(win, str(1))
entry = tk.Entry(win, textvariable=clinic_id, width=10)
entry.grid(row=2,column=2,sticky=tk.W,padx=10,pady=10)
 
clinic_name = tk.StringVar(win)
clinic_name.trace('w', lambda a, b, c: to_upper(clinic_name))
entry = tk.Entry(win, textvariable=clinic_name, width=10)
entry.grid(row=3, column=2, padx=10, pady=10, sticky=tk.W)
 
clinic_phone = tk.StringVar(win)
entry = tk.Entry(win, width=40, textvariable=clinic_phone, validate="key",\
    validatecommand=(win.register(validate_phone), "%S"))
entry.grid(row=4, column=2, padx=10, pady=10)
 
add_button = tk.Button(win, text="ADD", command = add_clinic, state=tk.DISABLED)
add_button.grid(row=5, column=2, padx=10, pady=10, sticky=tk.W)
 
exit_button = tk.Button(win, text="Exit", command=win.destroy)
exit_button.grid(row=5, column=2, padx=10, pady=10, sticky=tk.E)
  
win.mainloop()