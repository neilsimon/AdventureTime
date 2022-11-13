#Text Adventure Game Engine for Declan

import json
import sys
import tkinter as tk

# Open the first argument as a file with the locations in json format
gameFile = open(sys.argv[1])
# Parse the file into locations
locations = json.load(gameFile)
# Set the current location from the start location in the locations file
startLocation = locations["start location"]

window = tk.Tk()
window.columnconfigure(0, minsize=200, weight=1)
window.rowconfigure(0, minsize=200, weight=1)
window.rowconfigure(1, minsize=200, weight=1)

descriptionFrame = tk.Frame(master=window)
descriptionFrame.grid(column=0, row=0, sticky="nsew")
descriptionLabel = tk.Text(master=descriptionFrame, height=20, width=50)
scroll = tk.Scrollbar(master=descriptionFrame, command=descriptionLabel.yview)
descriptionLabel.configure(yscrollcommand=scroll.set, state="disabled", wrap=tk.WORD)
descriptionLabel.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

actionsFrame = tk.Frame(master=window)
actionsFrame.grid(column=0, row=1, sticky="nsew")
actionButtons = []

def resetActions():
    global actionButtons
    for actionButton in actionButtons:
        actionButton.pack_forget()
        actionButton.destroy
    actionButtons = []

def goTo(action, location):
    addDescriptionText("\nYou " + action + "\n")
    describeLocation(location)
    
def addActions(verbs):
    for verb, location in verbs.items():
        actionButton = tk.Button(master=actionsFrame, text=verb, command=lambda act=verb, loc=location: goTo(act, loc))
        actionButton.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        actionButtons.append(actionButton)
    
def addDescriptionText(text):
    descriptionLabel.configure(state="normal")
    descriptionLabel.insert(tk.END, text)
    descriptionLabel.configure(state="disabled")
    
def describeLocation(location):
    global locations
    if location in locations:
        description = locations[location]["description"]
        addDescriptionText("\n" + description + "\n")
        setActions(location)
    else:
        addDescriptionText("Error: location does not exist: " + location)
        quit()

def setActions(location):
    resetActions()
    if location in locations:
        if "verbs" not in locations[location] or len(locations[location]["verbs"]) == 0:
            addDescriptionText("\nGame over\n")
            return False
            
        addActions(locations[location]["verbs"])
    else:
        addDescriptionText("Error: location does not exist: " + location)
        quit()


describeLocation(startLocation)

window.mainloop()
