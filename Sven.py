from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import Shader, loadPrcFileData

loadPrcFileData("", """
    cursor-hidden true
    show-frame-rate-meter true
    """)



    

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()

        shader = Shader.load(Shader.SL_GLSL, vertex="shaders/jitter.vert", fragment="shaders/unlit.frag")
        self.render.setShader(shader)
        self.render.setShaderInput("snapScale", 30)

        self.floor = self.loader.loadModel("models/floor.glb")
        self.floor.reparentTo(self.render)

        self.sven = Actor("models/low_poly_cat.glb")
        self.sven.setScale(0.5)
        self.sven.reparentTo(self.render)
        self.sven.loop("WalkTrack")

        # Set up the camera
        self.cameraTarget = self.sven.attachNewNode("cameraTarget")
        self.cameraTarget.setPos(0, 0, 1.5)
        self.camera.reparentTo(self.cameraTarget)
        self.camera.setPos(0, -10, 2)
        self.camera.lookAt(self.cameraTarget)



if __name__ == "__main__":
    app = MyApp()
    app.run()
