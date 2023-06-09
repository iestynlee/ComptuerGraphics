from BaseModel import BaseModel,DrawModelFromMesh
from mesh import *
from matutils import *
from texture import *
from shaders import *
from cubeMap import CubeMap

class SkyBoxShader(BaseShaderProgram):
    def __init__(self, name='skybox'):
        BaseShaderProgram.__init__(self, name=name)
        self.add_uniform('sampler_cube')

    def bind(self, model, M):
        BaseShaderProgram.bind(self, model, M)
        P = model.scene.P  # Get projection matrix from the scene
        V = model.scene.camera.V  # Get view matrix from the camera
        Vr = np.identity(4)
        Vr[:3, :3] = V[:3, :3]

        self.uniforms['PVM'].bind(np.matmul(P, np.matmul(V, M)))

class SkyBox(DrawModelFromMesh):
    def __init__(self, scene):
        DrawModelFromMesh.__init__(self, scene=scene, M=poseMatrix(scale=10.0),
                                   mesh=CubeMesh(texture=CubeMap(name='skybox/jungle'), inside=True),
                                   shader=SkyBoxShader(), name='skybox') #Gets the name of the folder for the skybox

    def draw(self):
        glDepthMask(GL_FALSE)
        DrawModelFromMesh.draw(self)
        glDepthMask(GL_TRUE)

