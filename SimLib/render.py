import pygame as pg
import random
from SimLib.Vector import Vector

class Render():
    """
    Generic class for rendering physics models with Pygame.
    
    Attributes
    ----------
    scale : 1x2 float array
        Coordinate transform scaling values. scale[0] is the x scalar, and scale[1] is the y scalar.
    offset : 1x2 float array
        Coordinate transform offset values. scale[0] is the x offset, and scale[1] is the y offset.
    """

    def __init__(self, scale, offset):
        """
        Initializes the Render class.
        
        Sets up scale and offset attributes.
        """
        self.scale = scale
        self.offset = offset

    def _coord_transform(self, coords):
        """
        Transforms physical coordinates from a model to digital display coordinates, bounded by the size of the screen.
        
        Returns
        -------
        x_new : int
            Transformed x-coordinate for displaying on the screen.
        y_new : int
            Transformed y-coordinate for displaying on the screen.
        """
        x_new = int((coords[0] * self.scale[0]) + self.offset[0])
        y_new = int((coords[1] * self.scale[1]) + self.offset[1])

        return [x_new,y_new]

class SolarRender(Render):
    """
    A class for rendering a solar system model using Pygame.
    
    Inherits from the `Render` class and is responsible for displaying orbitals
    with different colors and sizes.
    
    Attributes
    ----------
    colors : list of tuple
        RGB color values for different orbitals.
    sizes : list of int
        Sizes of the orbitals to be rendered.
    """

    def __init__(self):
        """
        Initializes the SolarRender class.
        
        Sets up colors, sizes, rendering scale, and initializes the font for rendering text.
        """
        self.colors = [(200, 245, 66),(245, 206, 66),(68, 154, 252),(255,0,0),(156, 156, 156)]
        self.sizes = [5,8,12,10,5]
        super().__init__(scale=[3.3990094470708966e-10,3.3990094470708966e-10], offset=[300,300])
        
        pg.font.init() # you have to call this at the start, 
                   # if you want to use this module.
        self.my_font = pg.font.SysFont('Arial', 30)

    def render(self, model, screen):
        """
        Parameters
        ----------
        model : object
            The solar system model containing orbitals and time data.
        screen : pygame.Surface
            The Pygame screen surface to render onto.
        """

        pg.draw.circle(screen,color=(255,255,255),center=[300,300],radius=5,width=1)
        text_surface = self.my_font.render(f'{str(int(model.time / 86400))} days', False, (255, 255, 255))
        screen.blit(text_surface, (0,0))

        for i,orbital in enumerate(model.orbitals):
            coords = [orbital.pos.x, orbital.pos.z]
            transformed_coords = super()._coord_transform(coords)
            pg.draw.circle(screen,color=self.colors[i],center=transformed_coords,radius=self.sizes[i],width=1)

class NBodyRender(Render):
    """
    A class for rendering an NBody physics model using Pygame.
    
    Inherits from the `Render` class and is responsible for displaying bodies
    with different colors and sizes.
    
    Attributes
    ----------
    colors : list of tuple
        RGB color values for different orbitals.
    sizes : list of int
        Sizes of the orbitals to be rendered.
    """

    def __init__(self, model):
        """
        Initializes the NBodyRender class.
        
        Sets up colors, sizes, rendering scale, and initializes the font for rendering text.
        """
        self.colors = [(255,255,0),(100,100,255),(255,0,0),(255,255,255)]
        self.sizes = [20,10,15,5]
        #for mass in model.gphobjects.m:
            #self.colors.append((255,255,255))
            #self.colors.append((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            #self.sizes.append(mass*10)

        super().__init__(scale=[40,40], offset=[750,450])
        
        pg.font.init()
        self.my_font = pg.font.SysFont('Arial', 30)

    def render(self, model, screen):
        """
        Parameters
        ----------
        model : object
            The NBody model containing bodies and time data.
        screen : pygame.Surface
            The Pygame screen surface to render onto.
        """
        text_surface = self.my_font.render(f'{str(round(model.time,2))} s', False, (255, 255, 255))
        screen.blit(text_surface, (0,0))

        if len(model.gphobjects.state) == 4:
            #'''
            # Distance between satellite and jupiter
            positions = model.gphobjects.state[:,:3]
            #print(f'{positions}\n')
            v1 = Vector(x=positions[2,0],y=positions[2,1],z=positions[2,2])
            v2 = Vector(x=positions[3,0],y=positions[3,1],z=positions[3,2])
            distance = round((v1 - v2).mag,2)

            text_surface = self.my_font.render(f'Distance = {distance}', False, (255, 255, 255))
            screen.blit(text_surface, (0,200))
            #'''

            #'''
            # Distance from satellite to sun
            satellite = model.gphobjects[3]
            rs = round(satellite.pos.r,1)
            #'''

            text_surface = self.my_font.render(f'Rs = {rs}', False, (255, 255, 255))
            screen.blit(text_surface, (0,400))

        for i,body in enumerate(model.gphobjects.state):
            coords = [body[0], body[2]] # [x,z]
            transformed_coords = super()._coord_transform(coords)
            pg.draw.circle(screen,color=self.colors[i],center=transformed_coords,radius=self.sizes[i],width=1)