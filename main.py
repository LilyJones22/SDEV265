import tkinter as tk

window = tk.Tk() # creating tkinter window

greeting = tk.Label(text ="Hello World", fg="white", bg="black") # creating label text
greeting.pack() # displaying label text

entry = tk.Entry() # creates text prompt
entry.pack() # displays text prompt

def print_text(): # button function
    text = entry.get() # text input
    print(text) # displays to console

button = tk.Button(window, text = "Print to Console", command=print_text) # button displays text, runs print_text when clicked
button.pack() # displays button

window.mainloop() # needs to be at end of sequence

