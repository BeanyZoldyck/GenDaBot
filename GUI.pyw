from GenDaBot import GenDaBot, appraise, LinearNetwork
import tkinter as tk

def processInput(EVENT):
    inputText = inputEntry.get()
    conf = GenDaBotexp(inputText)
    cert, ans, flt = appraise(conf)
    outputText = f'This was tweeted by a {["female","male"][ans]} ({cert:.2f}% confidence)'
    outputLabel.config(text=outputText)
    sliderValue.set(int(200*flt -100))
    slider.configure(troughcolor=f"{'pink' if ans == 0 else 'cyan'}")
    #print(val)

#def updateLabel(EVENT):
    #val = slider.get()
#    print(slider.get())
    #slider.configure(troughcolor=f"{'pink' if val == 0 else 'blue'}")
# Create the main window
window = tk.Tk()
window.title("Gen Da Bot")
window.geometry("300x150")  # Set the window size

# Create input label and entry
inputLabel = tk.Label(window, text="Enter text:")
inputLabel.pack(padx=10, pady=10)
inputEntry = tk.Entry(window, width=50)
inputEntry.pack(padx=10, pady=10)
inputEntry.bind("<KeyRelease>", processInput)
# Create output label
outputLabel = tk.Label(window, width=100, text="")
outputLabel.pack()
checkbox_var = tk.IntVar()
checkbox = tk.Checkbutton(window, text="Experimental Mode", variable=checkbox_var)
# Create process button
sliderValue = tk.DoubleVar()
slider = tk.Scale(window,troughcolor="white", from_=-100, to=100, variable=sliderValue, orient="horizontal", length=200, showvalue=0)
slider.configure(state="disabled")
slider.pack()

# Start the main loop
window.mainloop()
