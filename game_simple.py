#Text Adventure Game Engine for Declan

# Locations. All locations have to have the description. If a location is not an end state it must also have verbs.
locations = {
    "start location": "cave",
    "cave": {
        "description": "You are inside a cave. Outside the sun is shining brilliantly and it hurts your eyes. The darkness of the cave further along stares back at you.",
        "verbs": {
            "go deeper": "deeper cave",
            "go outside": "outside cave"
            }
        },
    "deeper cave": {
        "description": "It is black in here and you cannot see anything. You cannot find your way out. You will surely die of thirst or worse, being slowly digested by the stomach acid of a well fed grue.",
        "verbs": {
            "die of thirst": "die of thirst",
            "feed a grue": "feed a grue"
            }
        },
    "outside cave": {
        "description": "The sun is shining brightly and you are starting to get dizzy from the heat. You can see a deep and dark cave to you back and a lush green forest in front of you.",
        "verbs": {
            "enter cave": "cave",
            "go to the forest": "the forest"
            }
        },
    "the forest": {
        "description": "The sun's harsh rays are blocked by the canopy of lush green trees. You feel at home, among the mosses, lichen and bark.",
        },
    "die of thirst": {
        "description": "Over days you find yourself slowly dying of thirst, your body's aches getting worse with every passing moment until you no longer have the will to even try. You lie there, and die, in the comfort that you will make a nice meal for a grue.",
        },
    "feed a grue": {
        "description": "You call out into the darkness, making your best grue mating call. It only takes a few moments for a dozen grue to find you, and they quickly start making short work of you. Their teeth rend your flesh from your body, one excruciating bite at a time, but at least it will be all over soon.",
        },
    "place": {
        "description": "The description of the place goes here.",
        "verbs": {
            "the action": "where it brings you"
            }
        },
    "null": ""
    }

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
