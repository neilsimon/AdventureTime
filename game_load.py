#Text Adventure Game Engine for Declan

import json
import sys
import os
import argparse

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
currentLocation = locations["start location"]

def describeLocation(location):
    if location in locations:
        description = locations[location]["description"]
        print("\n" + description)
        return True
    else:
        print("Error: location does not exist: " + location)
        return False

def getAction(location):
    if location in locations:
        if "verbs" not in locations[location] or len(locations[location]["verbs"]) == 0:
            print("\nGame over\n")
            return False
            
        verbs = locations[location]["verbs"].keys()
        print("You can: "+ ','.join([str(elem) for elem in verbs]))
        action = input()
        while action not in verbs:
            print("Invalid action. What do you want to do?")
            print("You can: "+ ','.join([str(elem) for elem in verbs]))
            action = input()
        return locations[location]["verbs"][action]
    else:
        print("Error: location does not exist: " + location)
        return False

# Keep running until an ending location
while currentLocation and describeLocation(currentLocation):
    # Update the location based on the action
    currentLocation = getAction(currentLocation)
