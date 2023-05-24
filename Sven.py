from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import Shader, loadPrcFileData

loadPrcFileData("", """
    cursor-hidden true
    show-frame-rate-meter true
    """)

class Floor:
    def __init__(self):
        self.model = loader.loadModel("models/floor.gltf")
        self.model.reparentTo(render)

class Player:
    def __init__(self):
        self.actor = Actor("models/low_poly_cat.gltf")
        self.actor.setScale(0.5)
        self.actor.reparentTo(render)
        self.actor.loop("WalkTrack")

        self.cameraTarget = self.actor.attachNewNode("cameraTarget")
        self.cameraTarget.setPos(0, 0, 1.5)

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()

        shader = Shader.load(Shader.SL_GLSL, vertex="shaders/jitter.vert", fragment="shaders/unlit.frag")
        self.render.setShader(shader)
        self.render.setShaderInput("snapScale", 30)

        self.floor = Floor()

        self.player = Player()

        # Set up the camera
        self.camera.reparentTo(self.player.cameraTarget)
        self.camera.setPos(0, -10, 2)
        self.camera.lookAt(self.player.cameraTarget)



if __name__ == "__main__":
    app = MyApp()
    app.run()
