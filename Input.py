from direct.showbase.ShowBase import DirectObject

class Input(DirectObject.DirectObject):

    # Input: a basic key-map, followed by some key-events
    keyMap = {
        "up" : False,
        "down" : False,
        "left" : False,
        "right" : False,
        "turnLeft" : False,
        "turnRight" : False,
    }

    def __init__(self):

        # Note: Sorry about the weird controls. In the interests of
        #       keeping this demo simple and brief, I'm eschewing
        #       mouse-control. ^^;
        self.accept("w", self.updateKeyMap, ["up", True])
        self.accept("w-up", self.updateKeyMap, ["up", False])
        self.accept("s", self.updateKeyMap, ["down", True])
        self.accept("s-up", self.updateKeyMap, ["down", False])
        self.accept("a", self.updateKeyMap, ["left", True])
        self.accept("a-up", self.updateKeyMap, ["left", False])
        self.accept("d", self.updateKeyMap, ["right", True])
        self.accept("d-up", self.updateKeyMap, ["right", False])
        self.accept("q", self.updateKeyMap, ["turnLeft", True])
        self.accept("q-up", self.updateKeyMap, ["turnLeft", False])
        self.accept("e", self.updateKeyMap, ["turnRight", True])
        self.accept("e-up", self.updateKeyMap, ["turnRight", False])

        # Allow the player to quit!
        self.accept("escape", self.userExit)

    # Update the key-map when a key is pressed or released
    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState
