# pygame is just used to create a window with the operating system on which to draw.
import pygame

# imports all openGL functions
from OpenGL.GL import *

# import the shader class
from shaders import *

# import the camera class
from camera import Camera

# and we import a bunch of helper functions
from matutils import *

from lightSource import LightSource

class Scene:
    '''
    This is the main class for adrawing an OpenGL scene using the PyGame library
    '''
    def __init__(self, width=800, height=600, shaders=None):
        '''
        Initialises the scene
        '''

        # This is the size of the window but default is the width and the height
        self.window_size = (width, height)

        # Default Wireframe is off
        self.wireframe = False

        # Initialises the pygame window
        pygame.init()
        screen = pygame.display.set_mode(self.window_size, pygame.OPENGL | pygame.DOUBLEBUF, 24)

        # Here we start initialising the window from the OpenGL side
        glViewport(0, 0, self.window_size[0], self.window_size[1])

        # This selects the background color
        glClearColor(0.7, 0.7, 1.0, 1.0)

        # Enable back face culling
        glEnable(GL_CULL_FACE)

        # Enable the vertex array capability
        glEnableClientState(GL_VERTEX_ARRAY)

        # Enable depth test for clean output
        glEnable(GL_DEPTH_TEST)

        # Set the default shader program (can be set on a per-mesh basis)
        self.shaders = 'flat'

        # Initialise the projective transform
        near = 1.0
        far = 20.0
        left = -1.0
        right = 1.0
        top = -1.0
        bottom = 1.0

        # Cycle through models
        self.show_model = -1

        # Sets up as frustumMatrix
        self.P = frustumMatrix(left, right, top, bottom, near, far)

        # initialises the camera object
        self.camera = Camera()

        # Initialise the light source and position
        self.light = LightSource(self, position=[5., 5., 5.])

        # Rendering mode for the shaders
        self.mode = 1  # initialise to full interpolated shading

        # This class will maintain a list of models to draw in the scene,
        self.models = []

    def add_model(self, model):
        '''
        This method just adds a model to the scene.
        :param model: The model object to add to the scene
        :return: None
        '''

        # bind the default shader to the mesh
        #model.bind_shader(self.shaders)

        #Add models to model
        self.models.append(model)

    def add_models_list(self, models_list):
        '''
        This method just adds a model to the scene.
        :param model: The model object to add to the scene
        :return: None
        '''
        for model in models_list:
            self.add_model(model)

    def draw(self, framebuffer=False):
        '''
        Draw all models in the scene
        :return: None
        '''

        # First we need to clear the scene, we also clear the depth buffer to handle occlusions
        if not framebuffer:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Ensure that the camera view matrix is up to date
            self.camera.update()

        # Then we loop over all models in the list and draw them
        for model in self.models:
            model.draw()

        # Once we are done drawing, we display the scene
        # Note that here we use double buffering to avoid artefacts:
        # We draw on a different buffer than the one we display,
        # And flip the two buffers once we are done drawing.
        if not framebuffer:
            pygame.display.flip()

    def keyboard(self, event):
        '''
        Method to process keyboard events. Check Pygame documentation for a list of key events
        :param event: the event object that was raised
        '''
        if event.key == pygame.K_q:
            self.running = False

        # flag to switch wireframe rendering
        elif event.key == pygame.K_0:
            if self.wireframe:
                print('--> Rendering using colour fill')
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                self.wireframe = False
            else:
                print('--> Rendering using colour wireframe')
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                self.wireframe = True

    def pygameEvents(self):
        '''
        Method to handle PyGame events for user interaction.
        '''
        # check whether the window has been closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            #Keyboard events
            elif event.type == pygame.KEYDOWN:
                self.keyboard(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mods = pygame.key.get_mods()
                if event.button == 4:
                    #pass
                    if mods & pygame.KMOD_CTRL:
                        self.light.position *= 1.1
                        self.light.update()
                    else:
                        self.camera.distance = max(1, self.camera.distance - 1)

                elif event.button == 5:
                    #pass
                    if mods & pygame.KMOD_CTRL:
                        self.light.position *= 0.9
                        self.light.update()
                    else:
                        self.camera.distance += 1

            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    if self.mouse_mvt is not None:
                        self.mouse_mvt = pygame.mouse.get_rel()

                        self.camera.center[0] -= (float(self.mouse_mvt[0]) / self.window_size[0])
                        self.camera.center[1] -= (float(self.mouse_mvt[1]) / self.window_size[1])
                    else:
                        self.mouse_mvt = pygame.mouse.get_rel()

                elif pygame.mouse.get_pressed()[2]:
                    if self.mouse_mvt is not None:
                        self.mouse_mvt = pygame.mouse.get_rel()

                        self.camera.phi -= (float(self.mouse_mvt[0]) / self.window_size[0])
                        self.camera.psi -= (float(self.mouse_mvt[1]) / self.window_size[1])
                    else:
                        self.mouse_mvt = pygame.mouse.get_rel()
                else:
                    self.mouse_mvt = None

    def run(self):
        '''
        Draws the scene in a loop until exit.
        '''

        #Looping, the running can be turned false if q is pressed
        self.running = True
        while self.running:

            self.pygameEvents()

            #Continues drawing the scene until the window is quitted out of
            self.draw()