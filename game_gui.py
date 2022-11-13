#Text Adventure Game Engine for Declan

import json
import sys
import os
import argparse

import tkinter as tk

# Load the settings
if os.path.exists("settings.json"):
    settings = json.load(open("settings.json"))
else:
    settings = {}
parser = argparse.ArgumentParser(
    prog = 'Game',
    description = 'Simple adventure game system')
parser.add_argument('-g', '--gamefile', default=argparse.SUPPRESS)
parser.add_argument('-a', '--assetsdirectory', default=argparse.SUPPRESS)
args = parser.parse_args()
settings.update(vars(args))

# Open the game file with the locations in json format
gameFile = open(settings['gamefile'])
# Parse the file into locations
locations = json.load(gameFile)
# Set the current location from the start location in the locations file
startLocation = locations["start location"]

# Layout for the main window
window = tk.Tk()
window.columnconfigure(0, minsize=200, weight=1)
window.columnconfigure(1, minsize=300, weight=1)
window.rowconfigure(0, minsize=200, weight=1)
window.rowconfigure(1, minsize=100, weight=1)

# Layout for image window
pictureFrame = tk.Frame(master=window)
pictureFrame.grid(column=1, row=0, rowspan=2, sticky="nsew")
picture = False;
pictureLabel = tk.Label(master=pictureFrame)
pictureLabel.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Layout for the description frame
descriptionFrame = tk.Frame(master=window)
descriptionFrame.grid(column=0, row=0, sticky="nsew")
descriptionLabel = tk.Text(master=descriptionFrame, height=20, width=40)
scroll = tk.Scrollbar(master=descriptionFrame, command=descriptionLabel.yview)
descriptionLabel.configure(yscrollcommand=scroll.set, state="disabled", wrap=tk.WORD)
descriptionLabel.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

# Layout for the actions frame
actionsFrame = tk.Frame(master=window)
actionsFrame.grid(column=0, row=1, sticky="nsew")
actionButtons = []

# Empty the actions frame
def resetActions():
    global actionButtons
    for actionButton in actionButtons:
        actionButton.pack_forget()
        actionButton.destroy
    actionButtons = []

# Go to the location (describe the action taken)
def goTo(action, location):
    addDescriptionText("\nYou " + action + "\n")
    describeLocation(location)

# Add actions to the actions frame
def addActions(verbs):
    for verb, location in verbs.items():
        actionButton = tk.Button(master=actionsFrame, text=verb, command=lambda act=verb, loc=location: goTo(act, loc))
        actionButton.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        actionButtons.append(actionButton)

# Add description text
def addDescriptionText(text):
    descriptionLabel.configure(state="normal")
    descriptionLabel.insert(tk.END, text)
    descriptionLabel.configure(state="disabled")
    descriptionLabel.see(tk.END)

# Set the image displayed
def setImage(imageFile):
    global pictureLabel, picture
    imagePath = os.path.join(settings["assetsdirectory"], "images", imageFile)
    picture = tk.PhotoImage(file=imagePath)
    pictureLabel.configure(image=picture)

# Remove the image being displayed
def removeImage():
    global picture
    picture = False

# Describe the location
def describeLocation(location):
    global locations
    if location in locations:
        description = locations[location]["description"]
        addDescriptionText("\n" + description + "\n")
        if "image" in locations[location]:
            setImage(locations[location]["image"])
        else:
            removeImage()
        setActions(location)
    else:
        addDescriptionText("Error: location does not exist: " + location)
        quit()

# Set the actions buttons
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

# Set things up
describeLocation(startLocation)

window.mainloop()
