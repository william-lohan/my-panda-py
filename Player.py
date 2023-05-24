from panda3d.core import PandaNode, Vec3, CollisionNode, CollisionSphere, NodePath
from direct.actor.Actor import Actor
from Camera import Camera

class Player():

    def __init__(self):
        # self.actor = Actor("models/low_poly_cat.gltf")
        # self.actor.setScale(0.5)
        # self.actor.reparentTo(render)
        # self.actor.loop("WalkTrack")

        # self.cameraTarget = self.actor.attachNewNode("cameraTarget")
        # self.cameraTarget.setPos(0, 0, 1.5)

        # The basics: a root-node and a (static) model
        self.manipulator = render.attachNewNode(PandaNode("player"))

        self.model = Actor("models/low_poly_cat.gltf")
        self.model.reparentTo(self.manipulator)

        # Collision, so that the player doesn't pass through walls
        self.colliderNode = CollisionNode("player collider")
        self.colliderNode.addSolid(CollisionSphere(0, 0, 0, 1))
        self.colliderNode.setIntoCollideMask(0)
        self.colliderNode.setFromCollideMask(2)
        self.collider = self.manipulator.attachNewNode(self.colliderNode)
        self.collider.setZ(1)

        # The camera-controller!
        self.cameraController = Camera(-5, 5, 2.0, 7.0, self.manipulator, camera, colliderRadius = 0.5)

        # Some variables used by the player's movement.
        self.velocity = Vec3(0, 0, 0)
        self.acceleration = 300.0
        self.maxSpeed = 15.0
        self.friction = 50.0
        self.turnSpeed = 200.0

    # The update-method of the player, intended to be called by the game-class
    def update(self, dt: float, keyMap: dict[str, bool], sceneRoot: NodePath):
        # Again, it's perhaps better to have a reference to the game-object
        # in a "common" Python-file from which we could access the scene-root,
        # "render". But for the sake of convenience and cleanness, and given that
        # this is so simple a demo, I'm just passing it in as a parameter.

        # Movement

        # Update velocity according to key-presses and player-direction
        orientationQuat = self.manipulator.getQuat(sceneRoot)
        forward = orientationQuat.getForward()
        right = orientationQuat.getRight()

        walking = False

        if keyMap["up"]:
            self.velocity += forward*self.acceleration*dt
            walking = True
        if keyMap["down"]:
            self.velocity -= forward*self.acceleration*dt
            walking = True
        if keyMap["right"]:
            self.velocity += right*self.acceleration*dt
            walking = True
        if keyMap["left"]:
            self.velocity -= right*self.acceleration*dt
            walking = True

        # Turn the player according to key-presses
        if keyMap["turnRight"]:
            self.manipulator.setH(self.manipulator, -self.turnSpeed*dt)
        if keyMap["turnLeft"]:
            self.manipulator.setH(self.manipulator, self.turnSpeed*dt)

        # Prevent the player from moving too fast
        speed = self.velocity.length()

        if speed > self.maxSpeed:
            speed = self.maxSpeed
            self.velocity.normalize()
            self.velocity *= speed

        # Update the player's position
        self.manipulator.setPos(self.manipulator.getPos() + self.velocity*dt)

        # Apply friction when the player stops moving
        if not walking:
            frictionVal = self.friction*dt
            if frictionVal > speed:
                self.velocity.set(0, 0, 0)
            else:
                frictionVec = -self.velocity
                frictionVec.normalize()
                frictionVec *= frictionVal
                self.velocity += frictionVec

        # And update the camera-controller
        self.cameraController.update(dt, sceneRoot)

    # A method to clean up when destroying this object
    def cleanup(self):
        if self.cameraController is not None:
            self.cameraController.cleanup()
            self.cameraController = None
