import pygame

# Import the scene class
from scene import Scene

from lightSource import LightSource

from blender import load_obj_file

from OpenGL.GL import *
from OpenGL.GLU import *

from BaseModel import DrawModelFromMesh

from shaders import *

from ShadowMapping import *

from sphereModel import Sphere

from skyBox import *

from environmentMapping import *


class JungleScene(Scene):
    def __init__(self):
        Scene.__init__(self)

        # This is the environment of the skybox
        self.environment = EnvironmentMappingTexture(width=400, height=400)

        # Setting the light source values but changes the position
        self.light = LightSource(self, position=[-3., 4., 3.])

        # Draw the model of the light and uses the spheremodel
        self.show_light = DrawModelFromMesh(scene=self, M=poseMatrix(position=self.light.position, scale=0.000001),
                                            mesh=Sphere(material=Material(Ka=[10, 10, 10])), shader=FlatShader())

        # Setting the shaders set as phong
        self.shaders = 'phong'

        self.shadows = ShadowMap(light=self.light)
        self.show_shadow_map = ShowTexture(self, self.shadows)

        # Loads the entire scene
        jungle = load_obj_file('models/scene.obj')
        self.jungle = [DrawModelFromMesh(scene=self, M=translationMatrix([0, -5, 0]), mesh=mesh,
                                         shader=ShadowMappingShader(shadow_map=self.shadows), name='jungle') for mesh in
                       jungle]

        # Reflective Water
        water = load_obj_file('models/water.obj')
        self.water = [DrawModelFromMesh(scene=self, M=translationMatrix([0, -5.1, 0]), mesh=mesh,
                                        shader=EnvironmentShader(map=self.environment)) for mesh in water]

        # Rocks
        rocks1 = load_obj_file('models/Mossy_Rocks.obj')
        self.rocks1 = DrawModelFromMesh(scene=self, M=poseMatrix(position=[3, -4.95, 0], scale=0.1), mesh=rocks1[0],
                                        shader=FlatShader())

        rocks2 = load_obj_file('models/Mossy_Rocks.obj')
        self.rocks2 = [DrawModelFromMesh(scene=self, M=poseMatrix(position=[-4, -4.95, 3], scale=0.1), mesh=rocks2[0],
                                         shader=FlatShader()) for mesh in rocks2]

        # Setting the skybox
        self.skybox = SkyBox(scene=self)

    def draw_reflections(self):
        # Setting up reflections for reflected specifically the skybox
        self.skybox.draw()

        for model in self.models:
            model.draw()

        # All for Water
        for model in self.water:
            model.draw()

    def draw_shadow_map(self):
        # First we need to clear the scene, we also clear the depth buffer to handle occlusions
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # For Jungle
        for model in self.jungle:
            model.draw()

        # For Rocks
        for model in self.rocks2:
            model.draw()

    def draw(self, framebuffer=False):
        '''
        Draw all models in the scene
        :return: None
        '''
        # First we need to clear the scene, we also clear the depth buffer to handle occlusions
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # When using a framebuffer, we do not update the camera to allow for arbitrary viewpoint.
        if not framebuffer:
            self.camera.update()

        # First, we draw the skybox
        self.skybox.draw()

        # Render the shadows
        self.shadows.render(self)

        # When rendering the framebuffer we ignore the reflective object
        if not framebuffer:
            self.environment.update(self)

            # Draws the rocks1, this is done differently to allow calling each part of the rocks attributes
            self.rocks1.draw()

            # Shows the shadow_map
            self.show_shadow_map.draw()

        # Loop over all models in the list and draw them
        for model in self.models:
            model.draw()

        # Draws the scene
        for model in self.jungle:
            model.draw()

        # Draws the water into the scene
        for model in self.water:
            model.draw()

        # This is done differently to rocks1
        for model in self.rocks2:
            model.draw()

        # Draws the light onto the scene
        self.show_light.draw()

        # Once we are done drawing, we display the scene
        # Note that here we use double buffering to avoid artefacts:
        # We draw on a different buffer than the one we display,
        # And flip the two buffers once we are done drawing.
        if not framebuffer:
            pygame.display.flip()

    def keyboard(self, event):
        '''
        Process additional keyboard events
        '''

        Scene.keyboard(self, event)

        # Movement of Rock1
        if event.key == pygame.K_u:
            # Calls Rocks Matrix
            rocks = self.rocks1.M

            # Gets last column which is the position of the rock
            last_column = rocks[:, -1]

            # Moves the rock up the y axis by 0.5
            last_column[1] += 0.5

        if event.key == pygame.K_o:
            # Calls Rocks Matrix
            rocks = self.rocks1.M

            # Gets last column which is the position of the rock
            last_column = rocks[:, -1]

            # Moves the rock down the y axis by 0.5
            last_column[1] -= 0.5

        if event.key == pygame.K_i:
            # Calls Rocks Matrix
            rocks = self.rocks1.M

            # Gets last column which is the position of the rock
            last_column = rocks[:, -1]

            # Moves the rock up the x axis by 0.5
            last_column[0] += 0.5

        if event.key == pygame.K_k:
            # Calls Rocks Matrix
            rocks = self.rocks1.M

            # Gets last column which is the position of the rock
            last_column = rocks[:, -1]

            # Moves the rock down the x axis by 0.5
            last_column[0] -= 0.5

        if event.key == pygame.K_j:
            # Calls Rocks Matrix
            rocks = self.rocks1.M

            # Gets last column which is the position of the rock
            last_column = rocks[:, -1]

            # Moves the rock up the z axis by 0.5
            last_column[2] += 0.5

        if event.key == pygame.K_l:
            # Calls Rocks Matrix
            rocks = self.rocks1.M

            # Gets last column which is the position of the rock
            last_column = rocks[:, -1]

            # Moves the rock down the z axis by 0.5
            last_column[2] -= 0.5

        # Rotation
        elif event.key == pygame.K_r:
            # Call Rocks Matrix
            rocks = self.rocks1.M

            # Hardcoded the removal of scaling
            r1 = rocks[:, 0]
            r1[0] /= 0.1  # The scale factor
            r2 = rocks[:, 1]
            r2[1] /= 0.1
            r3 = rocks[:, 2]
            r3[2] /= 0.1

            # Numpy cos and sin for rotation fixed
            c = np.cos(10)
            s = np.sin(10)

            # Get the rotation for Z
            t1 = r1[0]
            t2 = r1[1]
            t3 = r2[0]
            t4 = r2[1]

            # Calculations for the matrix
            t1 = c
            t2 = s
            t3 = -s
            t4 = c

            # Applying scale again
            t1 *= 0.1
            t4 *= 0.1

            # Inserting back into the matrix
            r1[0] = t1
            r1[1] = t2
            r2[0] = t3
            r2[1] = t4

            # Applying the changes to the rocks
            rocks[:, 0] = r1
            rocks[:, 1] = r2
            rocks[:, 2] = r3

        elif event.key == pygame.K_e:
            # Call Rocks Matrix
            rocks = self.rocks1.M

            # Get columns
            r1 = rocks[:, 0]
            r2 = rocks[:, 1]
            r3 = rocks[:, 2]

            # Reverting rotation
            r1[0] = 0.1
            r1[1] = 0
            r1[2] = 0

            r2[0] = 0
            r2[1] = 0.1
            r2[2] = 0

            r3[0] = 0
            r3[1] = 0
            r3[2] = 0.1

            rocks[:, 0] = r1
            rocks[:, 1] = r2
            rocks[:, 2] = r3


if __name__ == '__main__':
    # Initialises the scene object
    # Scene = Scene(shaders='shader')
    scene = JungleScene()

    # Starts drawing the scene - Runs a loop
    scene.run()
