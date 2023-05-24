from direct.showbase.ShowBase import ShowBase
from panda3d.core import Shader, loadPrcFileData
from Floor import Floor
from Input import Input
from Player import Player

loadPrcFileData("", """
    cursor-hidden true
    show-frame-rate-meter true
    """)

class Game(Input, ShowBase):
    def __init__(self):
        Input.__init__(self)
        ShowBase.__init__(self)

        self.disableMouse()

        shader = Shader.load(Shader.SL_GLSL, vertex="shaders/jitter.vert", fragment="shaders/unlit.frag")
        self.render.setShader(shader)
        self.render.setShaderInput("snapScale", 30)

        self.floor = Floor()

        self.player = Player()

        # # Set up the camera
        # self.camera.reparentTo(self.player.cameraTarget)
        # self.camera.setPos(0, -10, 2)
        # self.camera.lookAt(self.player.cameraTarget)



if __name__ == "__main__":
    Game().run()
