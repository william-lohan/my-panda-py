from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties

from panda3d.core import Shader

from math import pi, sin, cos

from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from direct.gui.OnscreenText import OnscreenText

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # self.disableMouse()

        # properties = WindowProperties()
        # properties.setSize(1000, 750)
        # self.win.requestProperties(properties)



        # Load the environment model.
        self.stage = self.loader.loadModel("models/stage.glb")
        # Reparent the model to render.
        self.stage.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        # self.stage.setScale(0.25, 0.25, 0.25)
        # self.stage.setPos(-8, 42, 0)

        shader = Shader.load(Shader.SL_GLSL, vertex="shaders/jitter.vert", fragment="shaders/unlit.frag")
        self.stage.setShader(shader)
        self.stage.setShaderInput("snapScale", 10)

        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

if __name__ == "__main__":
    game = Game()
    game.run()
