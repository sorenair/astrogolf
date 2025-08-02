import pygame as pg
from SimLib.Vector import Vector
import random

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

    def __init__(self, screen_size, model=None):
        """
        Initializes the NBodyRender class.
        
        Sets up colors, sizes, rendering scale, and initializes the font for rendering text.
        """
        self.bg = pg.image.load("Assignments/final/sprites/bg_pixel_light.png")
        self.colors = [(255,255,0),(100,100,255),(255,0,0),(255,255,255)]
        self.sizes = [20,10,15,5]
        self.rocket_pos = (0,0)
        self.lvl = 0
        self.screen_size = screen_size

        super().__init__(scale=[40,40], offset=[750,450])
        
        pg.font.init()
        self.font_title = pg.font.SysFont('Grand9K Pixel', 100)
        self.font_subtitle = pg.font.SysFont('Grand9K Pixel', 50)

    def add_sprites(self, level, jp_en=False):
        self.pbar = Bar('power')
        self.fbar = Bar('fuel')
        self.menu_btn = MenuBtn()
        self.menu_btn2 = MenuBtn(version=2)

        self.menu_sprites = pg.sprite.Group()
        self.menu_sprites.add(self.menu_btn)
        self.menu_sprites.add(self.menu_btn2)
        self.players = pg.sprite.Group()
        self.flags = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.voids = pg.sprite.Group()
        self.portals = pg.sprite.Group()
        self.portals2 = pg.sprite.Group()
        
        if level == 0:
            # Instantiate player
            self.player = Player(0,0)
            self.arrow = Arrow(0,0)
            # Instantiate overlays
            self.rocket = pg.image.load("Assignments/final/sprites/pixel_pack/RocketWhite.png").convert_alpha()
            self.rocket = pg.transform.scale(self.rocket, (75,75))
            self.clock = pg.image.load("Assignments/final/sprites/clock.png").convert_alpha()
            self.clock = pg.transform.scale(self.clock, (50,50))
            self.key_up = pg.image.load('Assignments/final/sprites/keys/Classic/Light/Single PNGs/ARROWUP.png').convert_alpha()
            self.key_up = pg.transform.scale(self.key_up, (50,50))
            self.key_down = pg.image.load('Assignments/final/sprites/keys/Classic/Light/Single PNGs/ARROWDOWN.png').convert_alpha()
            self.key_down = pg.transform.scale(self.key_down, (50,50))
            self.key_left = pg.image.load('Assignments/final/sprites/keys/Classic/Light/Single PNGs/ARROWLEFT.png').convert_alpha()
            self.key_left = pg.transform.scale(self.key_left, (50,50))
            self.key_right = pg.image.load('Assignments/final/sprites/keys/Classic/Light/Single PNGs/ARROWRIGHT.png').convert_alpha()
            self.key_right = pg.transform.scale(self.key_right, (50,50))
            self.key_r = pg.image.load('Assignments/final/sprites/keys/Classic/Light/Single PNGs/R.png').convert_alpha()
            self.key_r = pg.transform.scale(self.key_r, (50,50))
            self.key_tab = pg.image.load('Assignments/final/sprites/keys/Classic/Light/Single PNGs/TAB.png').convert_alpha()
            self.key_tab = pg.transform.scale(self.key_tab, (94,50))
            # Instantiate flag
            self.flag = Flag(0, 0)
            self.flag.rect.center = (1200,300)
            # Instantiate groups
            self.players.add(self.player)
            self.flags.add(self.flag)
            
        elif level == 1:
            # Instantiate player
            self.player = Player(0,0)
            if jp_en:
                self.player.image = pg.image.load("Assignments/final/sprites/pixel_pack/Astronaut1_jetpack.png").convert_alpha()
                self.player.image = pg.transform.scale(self.player.image, (50,50))
            self.arrow = Arrow(0,0)
            # Instantiate overlays
            self.rocket = pg.image.load("Assignments/final/sprites/pixel_pack/RocketWhite.png").convert_alpha()
            self.rocket = pg.transform.scale(self.rocket, (75,75))
            self.clock = pg.image.load("Assignments/final/sprites/clock.png").convert_alpha()
            self.clock = pg.transform.scale(self.clock, (50,50))
            # Instantiate flag
            self.flag = Flag(0, 0)
            self.flag.rect.center = (1200,300)
            # Instantiate planets
            self.sun = Planet(0,0, 'co_mars')

            # Instantiate groups
            self.players.add(self.player)
            self.flags.add(self.flag)
            self.obstacles.add(self.sun)
        elif level == 2:
            # Instantiate player
            self.player = Player(0,0)
            if jp_en:
                self.player.image = pg.image.load("Assignments/final/sprites/pixel_pack/Astronaut1_jetpack.png").convert_alpha()
                self.player.image = pg.transform.scale(self.player.image, (50,50))
            self.arrow = Arrow(0,0)
            # Instantiate overlays
            self.rocket = pg.image.load("Assignments/final/sprites/pixel_pack/RocketWhite.png").convert_alpha()
            self.rocket = pg.transform.scale(self.rocket, (75,75))
            self.clock = pg.image.load("Assignments/final/sprites/clock.png").convert_alpha()
            self.clock = pg.transform.scale(self.clock, (50,50))
            # Instantiate flag
            self.flag = Flag(0, 0)
            self.flag.rect.center = (1200,275)
            # Instantiate planets
            self.sun = Planet(0,0, 'co_mars')
            self.earth = Planet(0,0, 'co_blue')

            # Instantiate groups
            self.players.add(self.player)
            self.flags.add(self.flag)
            self.obstacles.add(self.sun)
            self.obstacles.add(self.earth)
        elif level == 3:
            # Instantiate player
            self.player = Player(0,0)
            if jp_en:
                self.player.image = pg.image.load("Assignments/final/sprites/pixel_pack/Astronaut1_jetpack.png").convert_alpha()
                self.player.image = pg.transform.scale(self.player.image, (50,50))
            self.arrow = Arrow(0,0)
            # Instantiate overlays
            self.rocket = pg.image.load("Assignments/final/sprites/pixel_pack/RocketWhite.png").convert_alpha()
            self.rocket = pg.transform.scale(self.rocket, (75,75))
            self.clock = pg.image.load("Assignments/final/sprites/clock.png").convert_alpha()
            self.clock = pg.transform.scale(self.clock, (50,50))
            # Instantiate flag
            self.flag = Flag(0, 0)
            self.flag.rect.center = (1200,275)
            # Instantiate planets
            self.a1 = Planet(0,0, 'co_asteroid_1')
            self.a2 = Planet(0,0, 'co_asteroid_2')
            self.a3 = Planet(0,0, 'co_asteroid_3')

            # Instantiate groups
            self.players.add(self.player)
            self.flags.add(self.flag)
            self.obstacles.add([self.a1, self.a2, self.a3])
        elif level == 4:
            # Instantiate player
            self.player = Player(0,0)
            if jp_en:
                self.player.image = pg.image.load("Assignments/final/sprites/pixel_pack/Astronaut1_jetpack.png").convert_alpha()
                self.player.image = pg.transform.scale(self.player.image, (50,50))
            self.arrow = Arrow(0,0)
            # Instantiate overlays
            self.rocket = pg.image.load("Assignments/final/sprites/pixel_pack/RocketWhite.png").convert_alpha()
            self.rocket = pg.transform.scale(self.rocket, (75,75))
            self.clock = pg.image.load("Assignments/final/sprites/clock.png").convert_alpha()
            self.clock = pg.transform.scale(self.clock, (50,50))
            # Instantiate flag
            self.mobile_flag = MobileFlag(0,0)
            # Instantiate planets
            self.sun = Planet(0,0, 'co_blackhole')

            # Instantiate groups
            self.players.add(self.player)
            self.flags.add(self.mobile_flag)
            self.obstacles.add(self.sun)
        elif level == 5:
            # Instantiate player
            self.player = Player(0,0)
            if jp_en:
                self.player.image = pg.image.load("Assignments/final/sprites/pixel_pack/Astronaut1_jetpack.png").convert_alpha()
                self.player.image = pg.transform.scale(self.player.image, (50,50))
            self.arrow = Arrow(0,0)
            # Instantiate overlays
            self.rocket = pg.image.load("Assignments/final/sprites/pixel_pack/RocketWhite.png").convert_alpha()
            self.rocket = pg.transform.scale(self.rocket, (75,75))
            self.clock = pg.image.load("Assignments/final/sprites/clock.png").convert_alpha()
            self.clock = pg.transform.scale(self.clock, (50,50))
            # Instantiate flag
            self.flag = Flag(0, 0)
            self.flag.rect.center = (1200,675)
            # Instantiate planets
            self.whitehole = Planet(x=0,y=0, planet='co_whitehole')
            self.void = Void(200,200,900,600)
            # Instantiate groups
            self.players.add(self.player)
            self.flags.add(self.flag)
            self.obstacles.add(self.whitehole)
            self.voids.add(self.void)
        elif level == 6:
            # Instantiate player
            self.player = Player(0,0)
            if jp_en:
                self.player.image = pg.image.load("Assignments/final/sprites/pixel_pack/Astronaut1_jetpack.png").convert_alpha()
                self.player.image = pg.transform.scale(self.player.image, (50,50))
            self.arrow = Arrow(0,0)
            # Instantiate overlays
            self.rocket = pg.image.load("Assignments/final/sprites/pixel_pack/RocketWhite.png").convert_alpha()
            self.rocket = pg.transform.scale(self.rocket, (75,75))
            self.clock = pg.image.load("Assignments/final/sprites/clock.png").convert_alpha()
            self.clock = pg.transform.scale(self.clock, (50,50))
            # Instantiate flag
            self.mobile_flag = MobileFlag(0,0)
            # Instantiate planets
            self.whitehole = Planet(x=0,y=0, planet='co_whitehole')
            self.blackhole = Planet(0,0, 'co_blackhole')
            self.planet = Planet(0,0,'co_blue')
            self.planet2 = Planet(0,0,'co_mars')
            # Instantiate groups
            self.players.add(self.player)
            self.flags.add(self.mobile_flag)
            self.obstacles.add(self.whitehole)
            self.obstacles.add(self.blackhole)
            self.obstacles.add(self.planet)
            self.obstacles.add(self.planet2)
        elif level == 7:
            # Instantiate player
            self.player = Player(0,0)
            if jp_en:
                self.player.image = pg.image.load("Assignments/final/sprites/pixel_pack/Astronaut1_jetpack.png").convert_alpha()
                self.player.image = pg.transform.scale(self.player.image, (50,50))
            self.arrow = Arrow(0,0)
            # Instantiate overlays
            self.rocket = pg.image.load("Assignments/final/sprites/pixel_pack/RocketWhite.png").convert_alpha()
            self.rocket = pg.transform.scale(self.rocket, (75,75))
            self.clock = pg.image.load("Assignments/final/sprites/clock.png").convert_alpha()
            self.clock = pg.transform.scale(self.clock, (50,50))
            # Instantiate flag
            self.mobile_flag = MobileFlag(0,0)
            # Instantiate planets
            self.planet = Planet(0,0,'co_asteroid_2')
            # Instantiate portals
            self.portal_r = Portal('red')
            self.portal_r.rect.center = (120,480)
            self.portal_b = Portal('blue')
            self.portal_b.rect.center = (1400,285)
            # Instantiate groups
            self.players.add(self.player)
            self.flags.add(self.mobile_flag)
            self.portals.add(self.portal_r)
            self.portals.add(self.portal_b)
            self.obstacles.add(self.planet)
        elif level == 8:
            # Instantiate player
            self.player = Player(0,0)
            if jp_en:
                self.player.image = pg.image.load("Assignments/final/sprites/pixel_pack/Astronaut1_jetpack.png").convert_alpha()
                self.player.image = pg.transform.scale(self.player.image, (50,50))
            self.arrow = Arrow(0,0)
            # Instantiate overlays
            self.rocket = pg.image.load("Assignments/final/sprites/pixel_pack/RocketWhite.png").convert_alpha()
            self.rocket = pg.transform.scale(self.rocket, (75,75))
            self.clock = pg.image.load("Assignments/final/sprites/clock.png").convert_alpha()
            self.clock = pg.transform.scale(self.clock, (50,50))
            # Instantiate flag
            self.flag = Flag(0, 0)
            self.flag.rect.center = (1200,700)
            # Instantiate planets
            self.a1 = Planet(0,0,'co_asteroid_2')
            self.planet = Planet(0,0,'co_mars')
            self.void = Void(200,200,800,500)
            self.void2 = Void(200,200,150,420)
            self.void3 = Void(200,200,1000,740)
            # Instantiate portals
            self.portal_r = Portal('red',200,210)
            self.portal_b = Portal('blue',1220,420)
            self.portal_y = Portal('yellow',350,650)
            self.portal_p = Portal('purple',1300,650)
            # Instantiate groups
            self.players.add(self.player)
            self.flags.add(self.flag)
            self.portals.add(self.portal_r)
            self.portals.add(self.portal_b)
            self.portals2.add(self.portal_y)
            self.portals2.add(self.portal_p)
            self.obstacles.add([self.planet,self.a1])
            self.voids.add([self.void,self.void2,self.void3])
        elif level == 9:
            # Instantiate player
            self.player = Player(0,0)
            if jp_en:
                self.player.image = pg.image.load("Assignments/final/sprites/pixel_pack/Astronaut1_jetpack.png").convert_alpha()
                self.player.image = pg.transform.scale(self.player.image, (50,50))
            self.arrow = Arrow(0,0)
            # Instantiate overlays
            self.rocket = pg.image.load("Assignments/final/sprites/pixel_pack/RocketWhite.png").convert_alpha()
            self.rocket = pg.transform.scale(self.rocket, (75,75))
            self.clock = pg.image.load("Assignments/final/sprites/clock.png").convert_alpha()
            self.clock = pg.transform.scale(self.clock, (50,50))
            # Instantiate flag
            self.mobile_flag = MobileFlag(0,0)
            # Instantiate planets
            self.planet = Planet(0,0,'co_blackhole')
            # Instantiate portals
            self.portal_r = Portal('red')
            self.portal_r.rect.center = (120,480)
            self.portal_b = Portal('blue')
            self.portal_b.rect.center = (1400,285)
            # Instantiate groups
            self.players.add(self.player)
            self.flags.add(self.mobile_flag)
            self.portals.add(self.portal_r)
            self.portals.add(self.portal_b)
            self.obstacles.add(self.planet)
        elif level == 10:
            # Instantiate player
            self.player1 = Player(0,0,num=1)
            self.player1.image = pg.image.load("Assignments/final/sprites/pixel_pack/Astronaut1_jetpack.png").convert_alpha()
            self.player1.image = pg.transform.scale(self.player1.image, (50,50))
            self.player2 = Player(0,0,num=2)
            self.player2.image = pg.image.load("Assignments/final/sprites/pixel_pack/Astronaut1_alt_jetpack.png").convert_alpha()
            self.player2.image = pg.transform.scale(self.player2.image, (50,50))
            self.arrow = Arrow(0,0)
            # Instantiate overlays
            self.clock = pg.image.load("Assignments/final/sprites/clock.png").convert_alpha()
            self.clock = pg.transform.scale(self.clock, (50,50))
            # Instantiate planets
            self.blackhole = Planet(0,0, 'co_blackhole')
            self.a1 = Planet(0,0, 'co_asteroid_2')
            self.a2 = Planet(0,0, 'co_asteroid_2')
            self.a3 = Planet(0,0, 'co_asteroid_3')
            # Instantiate groups
            self.players.add(self.player1)
            self.players.add(self.player2)
            self.voids.add(self.blackhole)
            self.obstacles.add([self.a1, self.a2, self.a3])
        else:
            pass

    def render(self, model, screen):
        """
        Parameters
        ----------
        model : object
            The NBody model containing bodies and time data.
        screen : pygame.Surface
            The Pygame screen surface to render onto.
        """
        screen.blit(self.bg, (0, 0))
        screen.blit(self.clock, (1300,50))
        if self.lvl != 10:
            screen.blit(self.rocket, self.rocket_pos)

        for i,body in enumerate(model.gphobjects.state):
            coords = [body[0], body[2]] # [x,z]
            transformed_coords = super()._coord_transform(coords)

            if (self.lvl == 0):
                if i == 0:
                    self.player.rect.center = transformed_coords
                    screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
            elif (self.lvl == 1) or (self.lvl == 2):
                if i == 0:
                    self.player.rect.center = transformed_coords
                    screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
                elif i == 1:
                    self.sun.rect.center = transformed_coords
                    screen.blit(self.sun.image, (self.sun.rect.x, self.sun.rect.y))
                elif i == 2:
                    self.earth.rect.center = transformed_coords
                    screen.blit(self.earth.image, (self.earth.rect.x, self.earth.rect.y))
            elif self.lvl == 3:
                if i == 0:
                    self.player.rect.center = transformed_coords
                    screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
                elif i == 1:
                    if ((transformed_coords[0] > self.screen_size[0] + 1000) or (transformed_coords[0] < 0 - 1000)) or ((transformed_coords[1] > self.screen_size[1] + 300) or (transformed_coords[1] < 0 - 300)):
                        model.gphobjects.state[i,:3] = [5,0,-18]
                        model.gphobjects.state[i,3:] = [-2,0,12]
                        coords = [body[0], body[2]] # [x,z]
                        transformed_coords = super()._coord_transform(coords)
                    self.a1.rect.center = transformed_coords
                    screen.blit(self.a1.image, (self.a1.rect.x, self.a1.rect.y))
                elif i == 2:
                    if ((transformed_coords[0] > self.screen_size[0] + 1000) or (transformed_coords[0] < 0 - 1000)) or ((transformed_coords[1] > self.screen_size[1] + 300) or (transformed_coords[1] < 0 - 300)):
                        model.gphobjects.state[i,:3] = [8,0,-12]
                        model.gphobjects.state[i,3:] = [-1,0,18]
                        coords = [body[0], body[2]] # [x,z]
                        transformed_coords = super()._coord_transform(coords)
                    self.a2.rect.center = transformed_coords
                    screen.blit(self.a2.image, (self.a2.rect.x, self.a2.rect.y))
                elif i == 3:
                    if ((transformed_coords[0] > self.screen_size[0] + 1000) or (transformed_coords[0] < 0 - 1000)) or ((transformed_coords[1] > self.screen_size[1] + 300) or (transformed_coords[1] < 0 - 300)):
                        model.gphobjects.state[i,:3] = [11,0,-16]
                        model.gphobjects.state[i,3:] = [-3,0,15]
                        coords = [body[0], body[2]] # [x,z]
                        transformed_coords = super()._coord_transform(coords)
                    self.a3.rect.center = transformed_coords
                    screen.blit(self.a3.image, (self.a3.rect.x, self.a3.rect.y))
            elif self.lvl == 4:
                if i == 0:
                    self.player.rect.center = transformed_coords
                    screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
                elif i == 1:
                    self.sun.rect.center = transformed_coords
                    screen.blit(self.sun.image, (self.sun.rect.x, self.sun.rect.y))
                elif i == 2:
                    self.mobile_flag.rect.center = transformed_coords
                    screen.blit(self.mobile_flag.image, (self.mobile_flag.rect.x, self.mobile_flag.rect.y))
                else:
                    pg.draw.circle(screen,color=self.colors[i],center=transformed_coords,radius=self.sizes[i],width=1)
            elif self.lvl == 5:
                if i == 0:
                    self.player.rect.center = transformed_coords
                    screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
                elif i == 1:
                    self.whitehole.rect.center = transformed_coords
                    screen.blit(self.whitehole.image, (self.whitehole.rect.x, self.whitehole.rect.y))
            elif self.lvl == 6:
                if i == 0:
                    self.player.rect.center = transformed_coords
                    screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
                elif i == 1:
                    self.whitehole.rect.center = transformed_coords
                    screen.blit(self.whitehole.image, (self.whitehole.rect.x, self.whitehole.rect.y))
                elif i == 2:
                    self.blackhole.rect.center = transformed_coords
                    screen.blit(self.blackhole.image, (self.blackhole.rect.x, self.blackhole.rect.y))
                elif i == 3:
                    self.mobile_flag.rect.center = transformed_coords
                    screen.blit(self.mobile_flag.image, (self.mobile_flag.rect.x, self.mobile_flag.rect.y))
                elif i == 4:
                    self.planet.rect.center = transformed_coords
                    screen.blit(self.planet.image, (self.planet.rect.x, self.planet.rect.y))
                elif i == 5:
                    self.planet2.rect.center = transformed_coords
                    screen.blit(self.planet2.image, (self.planet2.rect.x, self.planet2.rect.y))
            elif self.lvl == 7:
                if i == 0:
                    self.player.rect.center = transformed_coords
                    screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
                elif i == 1:
                    self.mobile_flag.rect.center = transformed_coords
                    screen.blit(self.mobile_flag.image, (self.mobile_flag.rect.x, self.mobile_flag.rect.y))
                elif i == 2:
                    self.planet.rect.center = transformed_coords
                    screen.blit(self.planet.image, (self.planet.rect.x, self.planet.rect.y))
            elif self.lvl == 8:
                if i == 0:
                    self.player.rect.center = transformed_coords
                    screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
                elif i == 1:
                    self.a1.rect.center = transformed_coords
                    screen.blit(self.a1.image, (self.a1.rect.x, self.a1.rect.y))
                elif i == 2:
                    self.planet.rect.center = transformed_coords
                    screen.blit(self.planet.image, (self.planet.rect.x, self.planet.rect.y))
            elif self.lvl == 9:
                if i == 0:
                    self.player.rect.center = transformed_coords
                    screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
                elif i == 1:
                    self.planet.rect.center = transformed_coords
                    screen.blit(self.planet.image, (self.planet.rect.x, self.planet.rect.y))
            elif self.lvl == 10:
                if i == 0:
                    self.player1.rect.center = transformed_coords
                    screen.blit(self.player1.image, (self.player1.rect.x, self.player1.rect.y))
                elif i == 1:
                    self.player2.rect.center = transformed_coords
                    screen.blit(self.player2.image, (self.player2.rect.x, self.player2.rect.y))
                elif i == 2:
                    self.blackhole.rect.center = transformed_coords
                    screen.blit(self.blackhole.image, (self.blackhole.rect.x, self.blackhole.rect.y))
                elif i == 3:
                    # TEST FOR ASTEROID COLLISIONS
                    if ((transformed_coords[0] > self.screen_size[0] + 3000) or (transformed_coords[0] < 0 - 3000)) or ((transformed_coords[1] > self.screen_size[1] + 1000) or (transformed_coords[1] < 0 - 1000)):
                        a_spawn = random.randint(0,3)
                        if a_spawn == 0:
                                model.gphobjects.state[i,:3] = [random.randint(-22,22),0,15]       # Set new position
                        elif a_spawn == 1:
                                model.gphobjects.state[i,:3] = [random.randint(-22,22),0,-15]       # Set new position
                        elif a_spawn == 2:
                                model.gphobjects.state[i,:3] = [22,0,random.randint(-15,15)]       # Set new position
                        else:
                                model.gphobjects.state[i,:3] = [-22,0,random.randint(-15,15)]       # Set new position
                        # SET NEW VELOCITY
                        pos_vec_normalized = random.randint(6,11) * -(Vector(model.gphobjects.state[i,:3]) / Vector(model.gphobjects.state[i,:3]).mag)
                        model.gphobjects.state[i,3] = pos_vec_normalized.x
                        model.gphobjects.state[i,5] = pos_vec_normalized.z
                        coords = [body[0], body[2]] # [x,z]
                        transformed_coords = super()._coord_transform(coords)
                    else:
                        hits = pg.sprite.spritecollide(self.a1, self.voids, False)
                        for hit in hits:
                            a_spawn = random.randint(0,3)
                            if a_spawn == 0:
                                 model.gphobjects.state[i,:3] = [random.randint(-22,22),0,15]       # Set new position
                            elif a_spawn == 1:
                                 model.gphobjects.state[i,:3] = [random.randint(-22,22),0,-15]       # Set new position
                            elif a_spawn == 2:
                                 model.gphobjects.state[i,:3] = [22,0,random.randint(-15,15)]       # Set new position
                            else:
                                 model.gphobjects.state[i,:3] = [-22,0,random.randint(-15,15)]       # Set new position
                            # SET NEW VELOCITY
                            pos_vec_normalized = random.randint(6,11) * -(Vector(model.gphobjects.state[i,:3]) / Vector(model.gphobjects.state[i,:3]).mag)
                            model.gphobjects.state[i,3] = pos_vec_normalized.x
                            model.gphobjects.state[i,5] = pos_vec_normalized.z
                            coords = [body[0], body[2]] # [x,z]
                            transformed_coords = super()._coord_transform(coords)
                    self.a1.rect.center = transformed_coords
                    screen.blit(self.a2.image, (self.a1.rect.x, self.a1.rect.y))
                elif i == 4:
                    # TEST FOR ASTEROID COLLISIONS
                    if ((transformed_coords[0] > self.screen_size[0] + 3000) or (transformed_coords[0] < 0 - 3000)) or ((transformed_coords[1] > self.screen_size[1] + 1000) or (transformed_coords[1] < 0 - 1000)):
                        a_spawn = random.randint(0,3)
                        if a_spawn == 0:
                                model.gphobjects.state[i,:3] = [random.randint(-22,22),0,15]       # Set new position
                        elif a_spawn == 1:
                                model.gphobjects.state[i,:3] = [random.randint(-22,22),0,-15]       # Set new position
                        elif a_spawn == 2:
                                model.gphobjects.state[i,:3] = [22,0,random.randint(-15,15)]       # Set new position
                        else:
                                model.gphobjects.state[i,:3] = [-22,0,random.randint(-15,15)]       # Set new position
                        # SET NEW VELOCITY
                        pos_vec_normalized = random.randint(6,11) * -(Vector(model.gphobjects.state[i,:3]) / Vector(model.gphobjects.state[i,:3]).mag)
                        model.gphobjects.state[i,3] = pos_vec_normalized.x
                        model.gphobjects.state[i,5] = pos_vec_normalized.z
                        coords = [body[0], body[2]] # [x,z]
                        transformed_coords = super()._coord_transform(coords)
                    else:
                        hits = pg.sprite.spritecollide(self.a2, self.voids, False)
                        for hit in hits:
                            a_spawn = random.randint(0,3)
                            if a_spawn == 0:
                                 model.gphobjects.state[i,:3] = [random.randint(-22,22),0,15]       # Set new position
                            elif a_spawn == 1:
                                 model.gphobjects.state[i,:3] = [random.randint(-22,22),0,-15]       # Set new position
                            elif a_spawn == 2:
                                 model.gphobjects.state[i,:3] = [22,0,random.randint(-15,15)]       # Set new position
                            else:
                                 model.gphobjects.state[i,:3] = [-22,0,random.randint(-15,15)]       # Set new position
                            # SET NEW VELOCITY
                            pos_vec_normalized = random.randint(6,11) * -(Vector(model.gphobjects.state[i,:3]) / Vector(model.gphobjects.state[i,:3]).mag)
                            model.gphobjects.state[i,3] = pos_vec_normalized.x
                            model.gphobjects.state[i,5] = pos_vec_normalized.z
                            coords = [body[0], body[2]] # [x,z]
                            transformed_coords = super()._coord_transform(coords)
                    self.a2.rect.center = transformed_coords
                    screen.blit(self.a2.image, (self.a2.rect.x, self.a2.rect.y))
                elif i == 5:
                    # TEST FOR ASTEROID COLLISIONS
                    if ((transformed_coords[0] > self.screen_size[0] + 3000) or (transformed_coords[0] < 0 - 3000)) or ((transformed_coords[1] > self.screen_size[1] + 1000) or (transformed_coords[1] < 0 - 1000)):
                        a_spawn = random.randint(0,3)
                        if a_spawn == 0:
                                model.gphobjects.state[i,:3] = [random.randint(-22,22),0,15]       # Set new position
                        elif a_spawn == 1:
                                model.gphobjects.state[i,:3] = [random.randint(-22,22),0,-15]       # Set new position
                        elif a_spawn == 2:
                                model.gphobjects.state[i,:3] = [22,0,random.randint(-15,15)]       # Set new position
                        else:
                                model.gphobjects.state[i,:3] = [-22,0,random.randint(-15,15)]       # Set new position
                        # SET NEW VELOCITY
                        pos_vec_normalized = random.randint(6,11) * -(Vector(model.gphobjects.state[i,:3]) / Vector(model.gphobjects.state[i,:3]).mag)
                        model.gphobjects.state[i,3] = pos_vec_normalized.x
                        model.gphobjects.state[i,5] = pos_vec_normalized.z
                        coords = [body[0], body[2]] # [x,z]
                        transformed_coords = super()._coord_transform(coords)
                    else:
                        hits = pg.sprite.spritecollide(self.a3, self.voids, False)
                        for hit in hits:
                            a_spawn = random.randint(0,3)
                            if a_spawn == 0:
                                 model.gphobjects.state[i,:3] = [random.randint(-22,22),0,15]       # Set new position
                            elif a_spawn == 1:
                                 model.gphobjects.state[i,:3] = [random.randint(-22,22),0,-15]       # Set new position
                            elif a_spawn == 2:
                                 model.gphobjects.state[i,:3] = [22,0,random.randint(-15,15)]       # Set new position
                            else:
                                 model.gphobjects.state[i,:3] = [-22,0,random.randint(-15,15)]       # Set new position
                            # SET NEW VELOCITY
                            pos_vec_normalized = random.randint(6,11) * -(Vector(model.gphobjects.state[i,:3]) / Vector(model.gphobjects.state[i,:3]).mag)
                            model.gphobjects.state[i,3] = pos_vec_normalized.x
                            model.gphobjects.state[i,5] = pos_vec_normalized.z
                            coords = [body[0], body[2]] # [x,z]
                            transformed_coords = super()._coord_transform(coords)
                    self.a3.rect.center = transformed_coords
                    screen.blit(self.a2.image, (self.a3.rect.x, self.a3.rect.y))
                
        
        # Set static flags and overlays
        if (self.lvl == 1) or (self.lvl == 2) or (self.lvl == 3) or (self.lvl == 5) or (self.lvl == 8):
            screen.blit(self.flag.image, (self.flag.rect.x, self.flag.rect.y))
        if self.lvl == 0:
            screen.blit(self.key_up, (50,700))
            screen.blit(self.key_down, (120,700))
            screen.blit(self.key_left, (50,800))
            screen.blit(self.key_right, (120,800))
            screen.blit(self.key_r, (50,600))
            screen.blit(self.key_tab, (50, 500))

            screen.blit(self.flag.image, (self.flag.rect.x, self.flag.rect.y))
        
        # Set static voids
        if self.lvl == 5:
            screen.blit(self.void.image, (self.void.rect.x, self.void.rect.y))
        elif self.lvl == 8:
            screen.blit(self.void.image, (self.void.rect.x, self.void.rect.y))
            screen.blit(self.void2.image, (self.void2.rect.x, self.void2.rect.y))
            screen.blit(self.void3.image, (self.void3.rect.x, self.void3.rect.y))

        # Set static portals
        if (self.lvl == 7):
            screen.blit(self.portal_r.image, (self.portal_r.rect.x, self.portal_r.rect.y))
            screen.blit(self.portal_b.image, (self.portal_b.rect.x, self.portal_b.rect.y))
        elif (self.lvl == 8):
            screen.blit(self.portal_r.image, (self.portal_r.rect.x, self.portal_r.rect.y))
            screen.blit(self.portal_b.image, (self.portal_b.rect.x, self.portal_b.rect.y))
            screen.blit(self.portal_y.image, (self.portal_y.rect.x, self.portal_y.rect.y))
            screen.blit(self.portal_p.image, (self.portal_p.rect.x, self.portal_p.rect.y))

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, num=1):
        # --- Essential: Call the parent class (Sprite) constructor ---
        super().__init__() # or pygame.sprite.Sprite.__init__(self)
        image_path = "Assignments/final/sprites/pixel_pack/Astronaut1.png"

        self.num = num

        # --- Essential: Load the image and set the 'image' attribute ---
        # Load the image from a file
        try:
            # Use convert_alpha() for images with transparency
            self.image = pg.image.load(image_path).convert_alpha()
            self.image = pg.transform.scale(self.image, (50,50))
            # Use convert() for images without transparency (slightly faster)
            # self.image = pygame.image.load(image_path).convert()
        except pg.error as e:
            print(f"Unable to load image: {image_path} - {e}")
            # Create a fallback surface if image loading fails
            self.image = pg.Surface([50, 50])
            self.image.fill((255,255,255))

        # Set player hitbox, second tuple is (width x height)
        #self.rect = self.image.get_rect()
        self.rect = pg.rect.Rect((0,0),(20,20))

        # --- Set the initial position using the 'rect' ---
        self.rect.x = x
        self.rect.y = y
        # Or set the center: self.rect.center = (x, y)

class Planet(pg.sprite.Sprite):
    def __init__(self, x, y, planet=''):
        super().__init__()
        self.planet = planet.lower()
        if self.planet[0:3] == 'co_':
            self.planet = self.planet[3:]
            image_path = f'Assignments/final/sprites/celestial_objects/{self.planet}.png'
        else:
            image_path = f'Assignments/final/sprites/pixel_pack/{planet}.png'

        # Load the image from a file
        try:
            self.image = pg.image.load(image_path).convert_alpha()
            if self.planet == 'sun':
                self.image = pg.transform.scale(self.image, (100,100))
            if self.planet == 'mars':
                self.image = pg.transform.scale(self.image, (100,100))
            elif (self.planet == 'earth') or (self.planet == 'blue'):
                self.image = pg.transform.scale(self.image, (75,75))
            elif (self.planet == 'blackhole') or (self.planet == 'whitehole'):
                self.image = pg.transform.scale(self.image, (136,100))
            elif (self.planet == 'forcefield'):
                self.image = pg.transform.scale(self.image, (75,75))
            elif (self.planet == 'asteroid_1'):
                self.image = pg.transform.scale(self.image, (180,90))
            elif (self.planet == 'asteroid_2'):
                self.image = pg.transform.scale(self.image, (93,90))
            elif (self.planet == 'asteroid_3'):
                self.image = pg.transform.scale(self.image, (75,52))
            else:
                self.image = pg.transform.scale(self.image, (100,100))
        except pg.error as e:
            print(f"Unable to load image: {image_path} - {e}")
            self.image = pg.Surface([50, 50])
            self.image.fill((255,255,255))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Flag(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        image_path = 'Assignments/final/sprites/flag_on_asteroid.png'

        # Load the image from a file
        try:
            self.image = pg.image.load(image_path).convert_alpha()
            self.image = pg.transform.scale(self.image, (75,112))
        except pg.error as e:
            print(f"Unable to load image: {image_path} - {e}")
            self.image = pg.Surface([50, 50])
            self.image.fill((255,255,255))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class MobileFlag(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        image_path = 'Assignments/final/sprites/flag_on_satellite.png'

        # Load the image from a file
        try:
            self.image = pg.image.load(image_path).convert_alpha()
            self.image = pg.transform.scale(self.image, (100,85))
        except pg.error as e:
            print(f"Unable to load image: {image_path} - {e}")
            self.image = pg.Surface([50, 50])
            self.image.fill((255,255,255))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
class Arrow(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        image_path = 'Assignments/final/sprites/arrow.png'

        # Load the image from a file
        try:
            self.original_image = pg.image.load(image_path).convert_alpha()
            self.original_image = pg.transform.scale(self.original_image, (50,50))
            self.image = self.original_image
        except pg.error as e:
            print(f"Unable to load image: {image_path} - {e}")
            self.image = pg.Surface([50, 50])
            self.image.fill((255,255,255))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Void(pg.sprite.Sprite):
    def __init__(self, w, h, x, y):
        super().__init__()
        '''
        image_path = 'Assignments/final/flag_on_satellite.png'

        # Load the image from a file
        try:
            self.image = pg.image.load(image_path).convert_alpha()
            self.image = pg.transform.scale(self.image, (100,85))
        except pg.error as e:
            print(f"Unable to load image: {image_path} - {e}")
            self.image = pg.Surface([50, 50])
            self.image.fill((255,255,255))
        '''

        self.image = pg.image.load('Assignments/final/sprites/celestial_objects/void.png').convert_alpha()
        self.image = pg.transform.scale(self.image, (w,h))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Bar(pg.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        '''
        image_path = 'Assignments/final/flag_on_satellite.png'

        # Load the image from a file
        try:
            self.image = pg.image.load(image_path).convert_alpha()
            self.image = pg.transform.scale(self.image, (100,85))
        except pg.error as e:
            print(f"Unable to load image: {image_path} - {e}")
            self.image = pg.Surface([50, 50])
            self.image.fill((255,255,255))
        '''
        try:
            if type == 'power':
                self.image = pg.image.load('Assignments/final/sprites/pbar2/0.png').convert_alpha()
                self.image = pg.transform.scale(self.image, (328,60))
            elif type == 'fuel':
                self.image = pg.image.load('Assignments/final/sprites/fuelbar/8.png').convert_alpha()
                self.image = pg.transform.scale(self.image, (150,55))
        except pg.error as e:
            print(f"Unable to load image")
            self.image = pg.Surface([50, 50])
            self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (50, 50)

class MenuBtn(pg.sprite.Sprite):
    def __init__(self, version=1):
        super().__init__()
        '''
        image_path = 'Assignments/final/flag_on_satellite.png'

        # Load the image from a file
        try:
            self.image = pg.image.load(image_path).convert_alpha()
            self.image = pg.transform.scale(self.image, (100,85))
        except pg.error as e:
            print(f"Unable to load image: {image_path} - {e}")
            self.image = pg.Surface([50, 50])
            self.image.fill((255,255,255))
        '''
        self.image = pg.image.load('Assignments/final/sprites/menubtn.png').convert_alpha()
        if version == 1:
            self.image = pg.transform.scale(self.image, (165,102))
            self.rect = self.image.get_rect()
            self.rect.x = 670
            self.rect.y = 550
        else:
            self.image = pg.transform.scale(self.image, (165,102))
            self.rect = self.image.get_rect()
            self.rect.x = 1320
            self.rect.y = 780

class Portal(pg.sprite.Sprite):
    def __init__(self, color, x=0, y=0):
        super().__init__()
        self.color = color.lower()
        if self.color == 'red':
            self.image = pg.image.load('Assignments/final/sprites/celestial_objects/portal_red.png').convert_alpha()
            self.image = pg.transform.scale(self.image, (60,58))
        elif self.color == 'blue':
            self.image = pg.image.load('Assignments/final/sprites/celestial_objects/portal_blue.png').convert_alpha()
            self.image = pg.transform.scale(self.image, (60,58))
        elif self.color == 'yellow':
            self.image = pg.image.load('Assignments/final/sprites/celestial_objects/portal_yellow.png').convert_alpha()
            self.image = pg.transform.scale(self.image, (62,58))
        else:
            self.image = pg.image.load('Assignments/final/sprites/celestial_objects/portal_purple.png').convert_alpha()
            self.image = pg.transform.scale(self.image, (62,58))
        
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)