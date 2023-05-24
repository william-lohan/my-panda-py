from panda3d.core import CollisionNode, CollisionTraverser, CollisionHandlerQueue, CollisionSegment, NodePath, PandaNode

class Camera():

    def __init__(
        self,
        tilt: float,
        intendedDistance: float,
        height: float,
        adjustmentSpeed: float,
        ownerNodePath: NodePath,
        camera: NodePath,
        colliderRadius: float = 1.0
    ):
        self.tilt = tilt
        self.intendedDistance = intendedDistance
        self.height = height
        self.adjustmentSpeed = adjustmentSpeed
        self.ownerNodePath = ownerNodePath
        self.camera = camera
        self.colliderRadius = colliderRadius

        # The node-structure of the camera-controller:
        # A base, which is positioned either to the left, centre, or right of the owner,
        # and to which the "tilt" is applied; and a "holder", which handles the camera's
        # retreat from obstacles and recovery when there are none
        self.cameraBase = ownerNodePath.attachNewNode(PandaNode("third-person camera-base"))
        self.cameraHolder = self.cameraBase.attachNewNode(PandaNode("third-person camera-holder"))
        camera.reparentTo(self.cameraHolder)

        self.cameraBase.setZ(height)
        self.cameraBase.setP(tilt)
        self.cameraHolder.setY(-intendedDistance)

        # Setup the collision used by the controller--however the relevant sub-class
        # may have implemented that
        self.setupCollision()

    # Build the collision-related elements that inform the camera's behaviour
    #
    # This implementation uses Panda's built-in collision-system
    def setupCollision(self):
        # A traverser, which enacts the actual collision-detection
        self.traverser = CollisionTraverser()

        # We'll use a queue, since we only want the nearest collision in a given update
        self.collisionQueue = CollisionHandlerQueue()

        # Our collision-objects: four segments, extending backwards for the "intended distance".
        self.colliderNode = CollisionNode("camera collider")
        self.colliderNode.addSolid(CollisionSegment(-self.colliderRadius, -self.colliderRadius, 0, -self.colliderRadius, -self.intendedDistance, 0))
        self.colliderNode.addSolid(CollisionSegment(self.colliderRadius, -self.colliderRadius, 0, self.colliderRadius, -self.intendedDistance, 0))
        self.colliderNode.addSolid(CollisionSegment(0, -self.colliderRadius, -self.colliderRadius, 0, -self.intendedDistance, -self.colliderRadius))
        self.colliderNode.addSolid(CollisionSegment(0, -self.colliderRadius, self.colliderRadius, 0, -self.intendedDistance, self.colliderRadius))

        self.colliderNode.setIntoCollideMask(0)
        self.colliderNode.setFromCollideMask(1)

        self.collider = self.cameraBase.attachNewNode(self.colliderNode)

        # Add our collision -objects and -handler to our traverser
        self.traverser.addCollider(self.collider, self.collisionQueue)

    # Check for a collision relevant to the camera
    #
    # This implementation uses Panda's built-in collision-system
    def getNearestCollision(self, sceneRoot) -> float:
        # Ask the traverser to check for collisions
        self.traverser.traverse(sceneRoot)

        # If there have been any collisions...
        if self.collisionQueue.getNumEntries() > 0:

            # Sort the collision-entries, which orders them from
            # nearest to furthest, I believe.
            self.collisionQueue.sortEntries()

            # Then get the first--i.e. nearest--of them.
            entry = self.collisionQueue.getEntry(0)

            # Now, use the collision-position to determine how far away the
            # collision occurred from the camera's base-position, and return that.
            pos = entry.getSurfacePoint(sceneRoot)
            diff = self.cameraBase.getPos(sceneRoot) - pos

            return diff.length()

        # In there were no collisions, just return the "intended distance"
        return self.intendedDistance
    
    # Update the camera's state
    def update(self, dt: float, sceneRoot: NodePath):
        # Determine how far out the camera is placed at the moment
        currentDistance = abs(self.cameraHolder.getY())

        # Determine where it should be:

        # Default to the assumption that it should be at the "intended distance"
        targetY = self.intendedDistance

        # Check for camera-relevant collisions, and update the "targetY" if called for
        collisionDistance = self.getNearestCollision(sceneRoot)
        if targetY > collisionDistance:
            targetY = collisionDistance

        # Compare the current placement with the target
        yDiff = targetY - currentDistance

        # Update the camera's position based on that "yDiff"
        #
        # The "> 1" section prevents overly-large delta-times from
        # producing overly-large movements
        offsetVal = self.adjustmentSpeed*dt
        if offsetVal > 1:
            offsetVal = 1
        offset = yDiff*offsetVal
        self.cameraHolder.setY(-currentDistance -offset)

    # A method to call when destroying the camera-controller
    def cleanup(self):
        # This class doesn't take ownership of either the camera
        # or the "ownerNodePath", and so simply detaches the former
        # and disengages from the latter. The assumption is that other
        # code is responsible for them.
        # (And indeed, one may want to re-use the camera!)

        if self.camera is not None:
            self.camera.detachNode()
            self.camera = None

        if self.ownerNodePath is not None:
            self.ownerNodePath = None

        # Clean up the controller's objects
        self.cleanupCollision()
        if self.cameraBase is not None:
            self.cameraBase.removeNode()
            self.cameraBase = None

    # A method to clean up the controller's collision elements
    def cleanupCollision(self):
        if self.collider is not None:
            self.traverser.removeCollider(self.collider)
            self.collider.removeNode()
            self.collider = None
            self.colliderNode = None

        self.traverser = None
        self.collisionQueue = None
