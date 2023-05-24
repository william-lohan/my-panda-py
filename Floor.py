
class Floor():

    def __init__(self):
        self.model = loader.loadModel("models/floor.gltf")
        self.model.reparentTo(render)
