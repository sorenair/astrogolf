import pygame as pg
import numpy as np
import math
import random
import time
from SimLib.Vector import Vector
from SimLib import model_final
from SimLib import phobject
from SimLib import final_controls

class Animate():
    """
    A class to handle animation and user interactions for a simulation.
    
    This class manages the rendering loop, event handling, and timing for
    updating the simulation model and display.
    
    Attributes
    ----------
    model : object
        The simulation model to be updated over time.
    render : object
        The rendering class responsible for drawing the simulation.
    screen_size : list of int, optional
        The width and height of the Pygame display window (default is [600, 400]).
    done : bool
        A flag indicating whether the animation loop should stop.
    time : int
        Keeps track of the elapsed time in the animation.
    screen : pygame.Surface
        The Pygame display surface.
    previous_time : int
        Timestamp of the previous frame for time calculations.
    elapsed_time : int
        Time elapsed between frames.
    """
    
    def __init__(self, render, screen_size=[600,400], timescale=1):
        """
        Initializes the Animate class.
        
        Parameters
        ----------
        model : object
            The simulation model to be animated.
        render : object
            The rendering engine responsible for drawing frames.
        screen_size : list of int, optional
            The pixel size of the Pygame display window (default is [600, 400]).
        """
        # Functional Components
        self.initialized = False
        self.model = None
        self.render = render
        self.screen_size = screen_size
        self.screen = pg.display.set_mode(self.screen_size)

        # Game Variables
        self.done = False
        self.time = 0
        self.timescale = timescale
        self.menu = True
        self.menu_page = 0
        self.lvl = 1            # Game level tracker
        self.mute = False
        self.beat_game = False
        
        # Level Variables
        self.play = False       # Plays / advances level when 'True'
        self.started = False    # Tracks if level has been started
        self.time_start = 0     # Level start time
        self.playtime = 0
        self.time_limit = 999
        self.jetpack_en = False
        self.jetfuel_max = 100
        self.jetfuel = self.jetfuel_max
        self.tutorial_time = time.time()
        self.portal_cooldown = time.time()
        self.portal_last = time.time()

        # Player variables
        self.velocity = 0
        self.angle = 0

        # Levels - initial conditions (player, sun, earth)
        lvl_0 = Level(pos=np.array([[0,0,0]]),
            vel=np.array([[0,0,1]]),
            m=np.array([1]),
            time_limit=99)
        lvl_1 = Level(pos=np.array([[-10,0,3],[0,0,0]]),
            vel=np.array([[0,0,1],[0,0,0]]),
            m=np.array([1,5]),
            time_limit=5.0)
        lvl_2 = Level(pos=np.array([[-10,0,3],[-2,0,-2],[6,0,3]]),
            vel=np.array([[0,0,1],[2,0,5],[-2,0,-5]]),
            m=np.array([1,5,5]),
            time_limit=2.5)
        lvl_3 = Level(pos=np.array([[-10,0,3],[5,0,-18],[8,0,-10],[11,0,-14]]),
            vel=np.array([[0,0,1],[-2,0,12],[-1,0,18],[-3,0,15]]),
            m=np.array([1,1.5,1.25,1]),
            time_limit=5.0)
        lvl_4 = Level(pos=np.array([[-10,0,3],[0,0,0],[10,0,0]]),
            vel=np.array([[0,0,1],[0,0,0],[0,0,0]]),
            m=np.array([1,7,2]),
            time_limit=4.0)
        lvl_5 = Level(pos=np.array([[-10,0,0],[11,0,-3]]),
            vel=np.array([[0,0,0],[0,0,0]]),
            m=np.array([1,-3]),
            time_limit=6)
        lvl_6 = Level(pos=np.array([[-10,0,0],[2,0,6],[-3,0,0],[11,0,-6],[-13,0,-7],[13,0,9]]),
            vel=np.array([[0,0,0],[0,0,0],[0,0,0],[-5,0,3],[8,0,0],[-20,0,-20]]),
            m=np.array([1,-3,3,1,2,1.5]),
            time_limit=2.5)
        lvl_7 = Level(pos=np.array([[-12,0,-3],[-6,0,8],[10,0,3]]),
            vel=np.array([[0,0,0],[10,0,-7],[-2,0,-1]]),
            m=np.array([1,1,5]),
            time_limit=7)
        lvl_8 = Level(pos=np.array([[-16,0,7],[10,0,-3],[1,0,6]]),
            vel=np.array([[0,0,0],[-4,0,0],[2,0,1]]),
            m=np.array([1,5,2]),
            time_limit=20)
        lvl_9 = Level(pos=np.array([[-14,0,0],[0,0,0]]),
            vel=np.array([[0,0,0],[0,0,0]]),
            m=np.array([1,50]),
            time_limit=5)
        self.lvls = [lvl_0,lvl_1,lvl_2,lvl_3,lvl_4,lvl_5,lvl_6,lvl_7,lvl_8,lvl_9]

        pg.init()
        self.initialize_sprites()
        self.initialized = True

        # --- Play Music ---
        if not self.mute:
            MUSIC_FILE = 'Assignments/final/sfx/ost.mp3'
            INITIAL_VOLUME = 0.7 # Volume from 0.0 (silent) to 1.0 (full)
            pg.mixer.music.load(MUSIC_FILE)
            pg.mixer.music.set_volume(INITIAL_VOLUME)
            # play(loops=-1) means loop indefinitely
            # play(loops=0) means play once
            # play(loops=N) means play N+1 times
            pg.mixer.music.play(loops=-1)

    def run(self):
        """
        Runs the animation loop, handling events, updating the model,
        rendering frames, and controlling timing until the loop is stopped.
        """

        # Get an initial time
        self.previous_time = pg.time.get_ticks()

        while not self.done:
            # Handle timing
            self._timing_handler()

            # Handle Events
            self._mouse_handler()
            self._event_handler()

            # Update the model
            if self.play or (self.lvl == 3 and (not self.menu) and (not self.started)):
                self.model.advance(self.elapsed_time*self.timescale)
            self.set_statics()              # Set static object positions

            # Render scene
            self.screen.fill((0,0,0))       # Clear screen
            if not self.menu:
                self.render.render(self.model, self.screen)

            # Text displays and GUI
            self.gui_displays()

            # Detect collisions / out-of-frame position
            self._detect_collisions()

            #Update the display
            pg.display.flip()

            # Delay just pauses for the specified time, necessary for animation
            pg.time.delay(10)

        pg.quit()

    def _timing_handler(self):
        """
        Handles the timing for animation by calculating the time elapsed
        between the current and previous frames.
        """
        time_o = pg.time.get_ticks()
        self.elapsed_time = time_o-self.previous_time
        self.previous_time = time_o

        # Portal cooldown timing
        if ((self.lvl == 7) or (self.lvl == 8)) and self.play:
                self.portal_cooldown = time.time() - self.portal_last

    def _event_handler(self):
        """
        Handles user input events, including quitting the animation and
        detecting key presses such as the escape key to exit.
        """
        for event in pg.event.get():
            # Closing the pygame window causes a Quit event
            if event.type == pg.QUIT:
                self.done = True

            # handle MOUSEBUTTONUP
            if event.type == pg.MOUSEBUTTONUP:
                final_controls.click(self)

            # Look for user input
            if event.type == pg.KEYDOWN:
                # Exit game
                if event.key == pg.K_ESCAPE:
                    self.done = True

                # Return to menu
                if (event.key == pg.K_TAB):
                    self.menu = True
                    self.menu_page = 0
                    self.lvl = 0
                    self.started = False
                    self.play = False
                    self.velocity = 0
                    self.angle = 0
                    if not self.beat_game:
                        self.jetpack_en = False
                    self.levels_btn = self.levels_btn = pg.image.load("Assignments/final/sprites/levels_btn.png").convert_alpha()
                    self.levels_btn = pg.transform.scale(self.levels_btn, (271,124))
                    # Play sound effect
                    if not self.mute:
                        sfx = pg.mixer.Sound("Assignments/final/sfx/sfx_interface/menu_pause_01.wav")
                        sfx.set_volume(1)
                        sfx.play(loops=0)

                # Restart game
                elif (event.key == pg.K_r) and (not self.menu):
                    self.restart_game()

                # In-game Controls
                if self.play:
                    # Jetpack
                    if (self.jetpack_en and (self.jetfuel > 0)) or (self.lvl == 10):
                        final_controls.jetpack_controls(self, event)

                # Set initial velocity
                if (self.play == False) and (self.started == False) and (event.key == pg.K_UP) and (self.velocity < 10):
                    self.velocity += 1
                    self.render.pbar.image = pg.image.load(f'Assignments/final/sprites/pbar2/{self.velocity}.png').convert_alpha()
                    self.render.pbar.image = pg.transform.scale(self.render.pbar.image, (328,60))
                elif (self.play == False) and (self.started == False) and (event.key == pg.K_DOWN) and (self.velocity > 0):
                    self.velocity -= 1
                    self.render.pbar.image = pg.image.load(f'Assignments/final/sprites/pbar2/{self.velocity}.png').convert_alpha()
                    self.render.pbar.image = pg.transform.scale(self.render.pbar.image, (328,60))
                # Set initial angle
                if (self.play == False) and (self.started == False) and (event.key == pg.K_LEFT):
                    if self.angle == 350:
                        self.angle = 0
                    else:
                        self.angle += 10
                elif (self.play == False) and (self.started == False) and (event.key == pg.K_RIGHT):
                    if self.angle == 0:
                        self.angle = 350
                    else:
                        self.angle -= 10
                        
                # Start game
                elif (event.key == pg.K_SPACE) and (self.play == False) and (self.started == False) and (self.menu == False):
                    # Update player sprite
                    if self.lvl != 10:
                        if not self.jetpack_en:
                            self.render.player.image = pg.image.load("Assignments/final/sprites/pixel_pack/Astronaut.png").convert_alpha()
                            self.render.player.image = pg.transform.scale(self.render.player.image, (50,50))
                        else:
                            self.render.player.image = pg.image.load("Assignments/final/sprites/pixel_pack/Astronaut_jetpack.png").convert_alpha()
                            self.render.player.image = pg.transform.scale(self.render.player.image, (50,50))
                    else:
                        self.render.player1.image = pg.image.load("Assignments/final/sprites/pixel_pack/Astronaut_jetpack.png").convert_alpha()
                        self.render.player1.image = pg.transform.scale(self.render.player1.image, (50,50))
                        self.render.player2.image = pg.image.load("Assignments/final/sprites/pixel_pack/Astronaut_alt_jetpack.png").convert_alpha()
                        self.render.player2.image = pg.transform.scale(self.render.player2.image, (50,50))

                    # Set player / model parameters to match user input
                    new_velocity = Vector.asSpherical(self.velocity,0,(self.angle + 90) * (np.pi / 180))
                    self.model.gphobjects.state[0,3:] = [new_velocity.x, new_velocity.y, new_velocity.z]

                    # Play sound effect
                    if not self.mute:
                        sfx = pg.mixer.Sound("Assignments/final/sfx/beep.wav")
                        sfx.set_volume(1)
                        sfx.play(loops=0)

                    # Set game flags
                    self.time_start = time.time()
                    self.play = True
                    self.started = True

                # Menu
                if self.menu and (event.key == pg.K_RIGHT) and (self.menu_page == 1):
                    self.menu_page = 2
                    # Play sound effect
                    if not self.mute:
                        sfx = pg.mixer.Sound("Assignments/final/sfx/sfx_interface/menu_pause_01.wav")
                        sfx.set_volume(1)
                        sfx.play(loops=0)
                elif self.menu and (event.key == pg.K_LEFT) and (self.menu_page == 2):
                    self.menu_page = 1
                    # Play sound effect
                    if not self.mute:
                        sfx = pg.mixer.Sound("Assignments/final/sfx/sfx_interface/menu_pause_01.wav")
                        sfx.set_volume(1)
                        sfx.play(loops=0)

                elif self.menu and ((self.menu_page == 1) or (self.menu_page == 2)) and (event.key != None):
                    #################################
                    # DELETE THIS LINE / MOVE TO LEVELS!!!
                    #################################
                    self.jetfuel = 100

                    # Select level
                    if (event.key == pg.K_0):
                        self.lvl = 0
                        self.render.bg = pg.image.load("Assignments/final/sprites/bg_paper_dark.png")
                        self.level_select()

                        # Set tutorial time
                        self.tutorial_time = time.time()
                    elif (event.key == pg.K_1):
                        self.lvl = 1
                        self.render.bg = pg.image.load("Assignments/final/sprites/bg_pixel_light.png")
                        self.level_select()
                    elif (event.key == pg.K_2):
                        self.lvl = 2
                        self.render.bg = pg.image.load("Assignments/final/sprites/bgs/bg_binary.png")
                        self.level_select()
                    elif (event.key == pg.K_3):
                        self.lvl = 3
                        self.render.bg = pg.image.load("Assignments/final/sprites/bgs/bg_saturn.png")
                        self.level_select()
                    elif (event.key == pg.K_4):
                        self.lvl = 4
                        self.render.bg = pg.image.load("Assignments/final/sprites/bgs/bg_bh.png")
                        self.level_select()
                    elif (event.key == pg.K_5):
                        self.lvl = 5
                        self.render.bg = pg.image.load("Assignments/final/sprites/bgs/bg_anomaly.png")
                        self.level_select()
                    elif (event.key == pg.K_6):
                        self.lvl = 6
                        self.render.bg = pg.image.load("Assignments/final/sprites/bgs/bg_dual.png")
                        self.level_select()
                    elif (event.key == pg.K_7):
                        self.lvl = 7
                        self.render.bg = pg.image.load("Assignments/final/sprites/bgs/bg_portals.png")
                        self.level_select()
                        # Set portal cooldown
                        self.portal_cooldown = time.time()
                    elif (event.key == pg.K_8):
                        self.lvl = 8
                        self.render.bg = pg.image.load("Assignments/final/sprites/bgs/bg_portals2.png")
                        self.level_select()
                    elif (event.key == pg.K_9):
                        self.lvl = 9
                        self.jetpack_en = True
                        self.render.bg = pg.image.load("Assignments/final/sprites/bgs/bg_ff.png")
                        self.level_select()
                    else:
                        # Play sound effect
                        if not self.mute:
                            sfx = pg.mixer.Sound("Assignments/final/sfx/sfx_interface/menu_cancel_01.wav")
                            sfx.set_volume(1)
                            sfx.play(loops=0)
                
                elif self.menu and (self.menu_page == 3) and (event.key != None):
                    self.lvl = 10
                    self.render.bg = pg.image.load("Assignments/final/sprites/bgs/bg_bh.png")
                    self.level_select()

    def _detect_collisions(self):
        """
        Handles collsions between sprites during gameplay.
        """
        # Timer runout detection
        if self.lvl != 10:
            if self.playtime <= 0:
                if self.play:
                    self.play = False
                    # Play sound effect
                    if not self.mute:
                        sfx = pg.mixer.Sound("Assignments/final/sfx/explode.mp3")
                        sfx.set_volume(0.7)
                        sfx.play(loops=0)
                # Apply filter to screen
                filter = pg.Surface(self.screen_size, pg.SRCALPHA)
                filter.fill((0,0,0,150))
                self.screen.blit(filter, (0,0))
                # Display EOG message
                text_surface = self.render.font_title.render('Time\'s up!', False, (255, 0, 0))
                self.screen.blit(text_surface, (self.screen_size[0] / 2 - 250, self.screen_size[1] / 2 - 100))
                self.screen.blit(self.render.menu_btn.image, (self.render.menu_btn.rect.x,self.render.menu_btn.rect.y))
                text_surface = self.render.font_subtitle.render('or press \'R\' to restart', False, (255, 255, 255))
                self.screen.blit(text_surface, (self.screen_size[0] / 2 - 300, self.screen_size[1] - 200))

        # Victory detection
        if self.started:
            hits = pg.sprite.groupcollide(self.render.players, self.render.flags, False, False) # Check player collision with flag
            for hit in hits:
                if self.play:
                    self.play = False
                    # Play sound effect
                    if not self.mute:
                        sfx = pg.mixer.Sound("Assignments/final/sfx/win.wav")
                        sfx.set_volume(1)
                        sfx.play(loops=0)
                    # Select victory message
                    msg_num = random.randint(0,2)
                    if msg_num == 0:
                        self.vic_msg = 'Victory!'
                        self.vic_msg_x_offset = 200
                    elif msg_num == 1:
                        self.vic_msg = 'One small step!'
                        self.vic_msg_x_offset = 375
                    elif msg_num == 2:
                        self.vic_msg = 'To infinity and beyond!'
                        self.vic_msg_x_offset = 600          
                # Apply filter to screen
                filter = pg.Surface(self.screen_size, pg.SRCALPHA)
                filter.fill((0,0,0,150))
                self.screen.blit(filter, (0,0))
                # Display EOG message
                text_surface = self.render.font_title.render(self.vic_msg, False, (0, 255, 0))
                self.screen.blit(text_surface, (self.screen_size[0] / 2 - self.vic_msg_x_offset, self.screen_size[1] / 2 - 100))
                self.screen.blit(self.render.menu_btn.image, (self.render.menu_btn.rect.x,self.render.menu_btn.rect.y))
                text_surface = self.render.font_subtitle.render('or press \'R\' to restart', False, (255, 255, 255))
                self.screen.blit(text_surface, (self.screen_size[0] / 2 - 300, self.screen_size[1] - 200))

            # Check player collision with obstacles
            hits = pg.sprite.groupcollide(self.render.players, self.render.obstacles, False, False)
            for hit in hits:
                if self.play:
                    self.play = False
                    # Play sound effect
                    if not self.mute:
                        #sfx = pg.mixer.Sound("Assignments/final/scream.mp3")
                        sfx = pg.mixer.Sound("Assignments/final/sfx/explode.mp3")
                        sfx.set_volume(0.7)
                        sfx.play(loops=0)
                # Apply filter to screen
                filter = pg.Surface(self.screen_size, pg.SRCALPHA)
                filter.fill((0,0,0,150))
                self.screen.blit(filter, (0,0))
                # Display EOG message
                if self.lvl != 10:
                    text_surface = self.render.font_title.render('Catastrophic collision!', False, (255, 0, 0))
                    self.screen.blit(text_surface, (self.screen_size[0] / 2 - 575, self.screen_size[1] / 2 - 100))
                else:
                    if hit.num == 1:
                        text_surface = self.render.font_title.render('Blue Wins!', False, (255, 255, 255))
                        self.screen.blit(text_surface, (self.screen_size[0] / 2 - 235, self.screen_size[1] / 2 - 100))
                    elif hit.num == 2:
                        text_surface = self.render.font_title.render('White Wins!', False, (255, 255, 255))
                        self.screen.blit(text_surface, (self.screen_size[0] / 2 - 255, self.screen_size[1] / 2 - 100))
                self.screen.blit(self.render.menu_btn.image, (self.render.menu_btn.rect.x,self.render.menu_btn.rect.y))
                text_surface = self.render.font_subtitle.render('or press \'R\' to restart', False, (255, 255, 255))
                self.screen.blit(text_surface, (self.screen_size[0] / 2 - 300, self.screen_size[1] - 200))
            
            # Check player collision with voids
            hits = pg.sprite.groupcollide(self.render.players, self.render.voids, False, False)
            for hit in hits:
                if self.play:
                    self.play = False
                    # Play sound effect
                    if not self.mute:
                        #sfx = pg.mixer.Sound("Assignments/final/scream.mp3")
                        sfx = pg.mixer.Sound("Assignments/final/sfx/explode.mp3")
                        sfx.set_volume(0.7)
                        sfx.play(loops=0)
                # Apply filter to screen
                filter = pg.Surface(self.screen_size, pg.SRCALPHA)
                filter.fill((0,0,0,150))
                self.screen.blit(filter, (0,0))
                # Display EOG message
                if self.lvl != 10:
                    text_surface = self.render.font_title.render('Lost to the void!', False, (255, 0, 0))
                    self.screen.blit(text_surface, (self.screen_size[0] / 2 - 430, self.screen_size[1] / 2 - 100))
                else:
                    if hit.num == 1:
                        text_surface = self.render.font_title.render('Blue Wins!', False, (255, 255, 255))
                        self.screen.blit(text_surface, (self.screen_size[0] / 2 - 235, self.screen_size[1] / 2 - 100))
                    elif hit.num == 2:
                        text_surface = self.render.font_title.render('White Wins!', False, (255, 255, 255))
                        self.screen.blit(text_surface, (self.screen_size[0] / 2 - 255, self.screen_size[1] / 2 - 100))
                self.screen.blit(self.render.menu_btn.image, (self.render.menu_btn.rect.x,self.render.menu_btn.rect.y))
                text_surface = self.render.font_subtitle.render('or press \'R\' to restart', False, (255, 255, 255))
                self.screen.blit(text_surface, (self.screen_size[0] / 2 - 300, self.screen_size[1] - 200))
            
            '''
            # Check planetary collisions
            obstacles = self.render.obstacles.sprites()
            for i, obstacle1 in enumerate(obstacles):
                for obstacle2 in obstacles[i+1:]:
                    if pg.sprite.collide_mask(obstacle1, obstacle2):
                        if len(self.model.gphobjects.state) > 2:
                            self.model.gphobjects.state[2,:3] = [1000000,0,100000]
                        self.model.gphobjects.state = self.model.gphobjects.state[:2]
                        self.model.gphobjects.m = self.model.gphobjects.m [:2]
                        # Play sound effect
                        #sfx = pg.mixer.Sound("Assignments/final/scream.mp3")
                        sfx = pg.mixer.Sound("Assignments/final/explode.mp3")
                        sfx.set_volume(0.7)
                        sfx.play(loops=0)
            '''
            if (self.lvl == 4) or (self.lvl == 6):
                # Check mobile flag collision with obstacles
                hits = pg.sprite.spritecollide(self.render.mobile_flag, self.render.obstacles, False)
                for hit in hits:
                    if self.play:
                        self.play = False
                        # Play sound effect
                        if not self.mute:
                            #sfx = pg.mixer.Sound("Assignments/final/scream.mp3")
                            sfx = pg.mixer.Sound("Assignments/final/sfx/explode.mp3")
                            sfx.set_volume(0.7)
                            sfx.play(loops=0)
                    # Apply filter to screen
                    filter = pg.Surface(self.screen_size, pg.SRCALPHA)
                    filter.fill((0,0,0,150))
                    self.screen.blit(filter, (0,0))
                    # Display EOG message
                    text_surface = self.render.font_title.render('Nighty night, satellite!', False, (255, 0, 0))
                    self.screen.blit(text_surface, (self.screen_size[0] / 2 - 580, self.screen_size[1] / 2 - 100))
                    self.screen.blit(self.render.menu_btn.image, (self.render.menu_btn.rect.x,self.render.menu_btn.rect.y))
                    text_surface = self.render.font_subtitle.render('or press \'R\' to restart', False, (255, 255, 255))
                    self.screen.blit(text_surface, (self.screen_size[0] / 2 - 300, self.screen_size[1] - 200))
            elif (self.lvl == 6) or (self.lvl == 7):
                if ((self.render.mobile_flag.rect.x > self.screen_size[0]) or (self.render.mobile_flag.rect.x < 0)) or ((self.render.mobile_flag.rect.y > self.screen_size[1]) or (self.render.mobile_flag.rect.y < 0)):
                    if self.play:
                        self.play = False
                        # Play sound effect
                        if not self.mute:
                            sfx = pg.mixer.Sound("Assignments/final/sfx/explode.mp3")
                            sfx.set_volume(0.7)
                            sfx.play(loops=0)
                    # Apply filter to screen
                    filter = pg.Surface(self.screen_size, pg.SRCALPHA)
                    filter.fill((0,0,0,150))
                    self.screen.blit(filter, (0,0))
                    # Display EOG message
                    text_surface = self.render.font_title.render('Nighty night, satellite!', False, (255, 0, 0))
                    self.screen.blit(text_surface, (self.screen_size[0] / 2 - 580, self.screen_size[1] / 2 - 100))
                    self.screen.blit(self.render.menu_btn.image, (self.render.menu_btn.rect.x,self.render.menu_btn.rect.y))
                    text_surface = self.render.font_subtitle.render('or press \'R\' to restart', False, (255, 255, 255))
                    self.screen.blit(text_surface, (self.screen_size[0] / 2 - 300, self.screen_size[1] - 200))

            # Out-of-frame detection
            for player in self.render.players:
                if self.lvl != 9:
                    if ((player.rect.x > self.screen_size[0]) or (player.rect.x < 0)) or ((player.rect.y > self.screen_size[1]) or (player.rect.y < 0)):
                        if self.play:
                            self.play = False
                            # Play sound effect
                            if not self.mute:
                                sfx = pg.mixer.Sound("Assignments/final/sfx/explode.mp3")
                                sfx.set_volume(0.7)
                                sfx.play(loops=0)
                        # Apply filter to screen
                        filter = pg.Surface(self.screen_size, pg.SRCALPHA)
                        filter.fill((0,0,0,150))
                        self.screen.blit(filter, (0,0))
                        # Display EOG message
                        if self.lvl != 10:
                            text_surface = self.render.font_title.render('A miss to the abyss!', False, (255, 0, 0))
                            self.screen.blit(text_surface, (self.screen_size[0] / 2 - 500, self.screen_size[1] / 2 - 100))
                        else:
                            if player.num == 1:
                                text_surface = self.render.font_title.render('Blue Wins!', False, (255, 255, 255))
                                self.screen.blit(text_surface, (self.screen_size[0] / 2 - 235, self.screen_size[1] / 2 - 100))
                            elif player.num == 2:
                                text_surface = self.render.font_title.render('White Wins!', False, (255, 255, 255))
                                self.screen.blit(text_surface, (self.screen_size[0] / 2 - 255, self.screen_size[1] / 2 - 100))
                        self.screen.blit(self.render.menu_btn.image, (self.render.menu_btn.rect.x,self.render.menu_btn.rect.y))
                        text_surface = self.render.font_subtitle.render('or press \'R\' to restart', False, (255, 255, 255))
                        self.screen.blit(text_surface, (self.screen_size[0] / 2 - 300, self.screen_size[1] - 200))
                else:
                    if (player.rect.x < 0) or ((player.rect.y > self.screen_size[1]) or (player.rect.y < 0)):
                        if self.play:
                            self.play = False
                            # Play sound effect
                            if not self.mute:
                                sfx = pg.mixer.Sound("Assignments/final/sfx/explode.mp3")
                                sfx.set_volume(0.7)
                                sfx.play(loops=0)
                        # Apply filter to screen
                        filter = pg.Surface(self.screen_size, pg.SRCALPHA)
                        filter.fill((0,0,0,150))
                        self.screen.blit(filter, (0,0))
                        # Display EOG message
                        if self.lvl != 10:
                            text_surface = self.render.font_title.render('A miss to the abyss!', False, (255, 0, 0))
                            self.screen.blit(text_surface, (self.screen_size[0] / 2 - 500, self.screen_size[1] / 2 - 100))
                        else:
                            if player.num == 1:
                                text_surface = self.render.font_title.render('Blue Wins!', False, (255, 255, 255))
                                self.screen.blit(text_surface, (self.screen_size[0] / 2 - 235, self.screen_size[1] / 2 - 100))
                            elif player.num == 2:
                                text_surface = self.render.font_title.render('White Wins!', False, (255, 255, 255))
                                self.screen.blit(text_surface, (self.screen_size[0] / 2 - 255, self.screen_size[1] / 2 - 100))
                        self.screen.blit(self.render.menu_btn.image, (self.render.menu_btn.rect.x,self.render.menu_btn.rect.y))
                        text_surface = self.render.font_subtitle.render('or press \'R\' to restart', False, (255, 255, 255))
                        self.screen.blit(text_surface, (self.screen_size[0] / 2 - 300, self.screen_size[1] - 200))
                    elif (player.rect.x > self.screen_size[0]):
                        if self.play:
                            self.play = False
                            # Play sound effect
                            if not self.mute:
                                sfx = pg.mixer.Sound("Assignments/final/sfx/win.wav")
                                sfx.set_volume(1)
                                sfx.play(loops=0)     
                        # Apply filter to screen
                        filter = pg.Surface(self.screen_size, pg.SRCALPHA)
                        filter.fill((0,0,0,150))
                        self.screen.blit(filter, (0,0))
                        # Display EOG message
                        text_surface = self.render.font_subtitle.render('ENDLESS MODE UNLOCKED', False, (255, 255, 255))
                        self.screen.blit(text_surface, (self.screen_size[0] / 2 - 345, self.screen_size[1] / 2 - 220))
                        text_surface = self.render.font_title.render('Mission Complete!', False, (0, 255, 0))
                        self.screen.blit(text_surface, (self.screen_size[0] / 2 - 440, self.screen_size[1] / 2 - 100))
                        self.screen.blit(self.render.menu_btn.image, (self.render.menu_btn.rect.x,self.render.menu_btn.rect.y))
                        text_surface = self.render.font_subtitle.render('or press \'R\' to restart', False, (255, 255, 255))
                        self.screen.blit(text_surface, (self.screen_size[0] / 2 - 300, self.screen_size[1] - 200))

                        self.beat_game = True

            # Check player collision with portals
            if (self.lvl == 7) or (self.lvl == 8):
                if (self.portal_cooldown > 1):
                    hits = pg.sprite.spritecollide(self.render.player, self.render.portals, False)
                    for hit in hits:
                        for s in self.render.portals:
                            if not (hit.color == s.color):
                                portal_pos = s.rect.center
                                x_new = (portal_pos[0] - self.render.offset[0]) / self.render.scale[0]
                                y_new = (portal_pos[1] - self.render.offset[1]) / self.render.scale[1]
                                self.model.gphobjects.state[0,:3] = [x_new,0,y_new]
                                self.portal_last = time.time()
                                # Play sound effect
                                if not self.mute:
                                    sfx = pg.mixer.Sound("Assignments/final/sfx/portal.wav")
                                    sfx.set_volume(0.7)
                                    sfx.play(loops=0)
                    hits = pg.sprite.spritecollide(self.render.player, self.render.portals2, False)
                    for hit in hits:
                        for s in self.render.portals2:
                            if not (hit.color == s.color):
                                portal_pos = s.rect.center
                                x_new = (portal_pos[0] - self.render.offset[0]) / self.render.scale[0]
                                y_new = (portal_pos[1] - self.render.offset[1]) / self.render.scale[1]
                                self.model.gphobjects.state[0,:3] = [x_new,0,y_new]
                                self.portal_last = time.time()
                                # Play sound effect
                                if not self.mute:
                                    sfx = pg.mixer.Sound("Assignments/final/sfx/portal.wav")
                                    sfx.set_volume(0.7)
                                    sfx.play(loops=0)

    def _startup(self):
        """
        Start menu GUI.
        """
        if (not self.menu):
            # Instructions
            text_surface = self.render.font_subtitle.render('Press \'SPACE\' to launch', False, (255, 255, 255))
            self.screen.blit(text_surface, (self.screen_size[0] / 2 - 300, self.screen_size[1] - 100))
            if not (self.lvl == 10):
                # Initial velocity
                text_surface = self.render.font_subtitle.render(f'POWER', False, (255, 255, 255))
                self.screen.blit(text_surface, (120, 100))
                '''
                # Initial angle
                text_surface = self.render.font_subtitle.render(f'Angle (LEFT / RIGHT) - {self.angle}°', False, (255, 255, 255))
                self.screen.blit(text_surface, (50, 100))
                '''
            else:
                text_surface = self.render.font_title.render('GALACTIC DEATHMATCH!', False, (255, 255, 255))
                self.screen.blit(text_surface, (self.screen_size[0] / 2 - 650, 150))

        # Start menu
        if self.menu and (self.menu_page == 0):
            menu_bg = pg.image.load("Assignments/final/sprites/menu_bg.png")
            self.screen.blit(menu_bg, (0,0))
            text_surface = self.render.font_title.render('ASTROGOLF', False, (255, 255, 255))
            self.screen.blit(text_surface, (self.screen_size[0] / 2 - 325, self.screen_size[1] / 2 - 100))
            text_surface = self.render.font_subtitle.render('©2025 SØREN', False, (255, 255, 255))
            self.screen.blit(text_surface, (self.screen_size[0] / 2 - 200, self.screen_size[1] - 380))
            # Level Button
            self.screen.blit(self.levels_btn, (self.screen_size[0] / 2 - 330, self.screen_size[1] - 200))
            # Extra Button
            self.screen.blit(self.extra_btn, (self.screen_size[0] / 2 + 40, self.screen_size[1] - 200))
        # Level select
        if self.menu and (self.menu_page == 1):
            menu_bg = pg.image.load("Assignments/final/sprites/menu_bg.png")
            self.screen.blit(menu_bg, (0,0))
            text_surface = self.render.font_title.render('LEVEL SELECT', False, (255, 255, 255))
            self.screen.blit(text_surface, (self.screen_size[0] / 2 - 400, 30))
            text_surface = self.render.font_subtitle.render('CHAPTER I', False, (255, 255, 255))
            self.screen.blit(text_surface, (self.screen_size[0] / 2 - 140, 160))
            text_surface = self.render.font_subtitle.render('0 - Tutorial', False, (255, 255, 255))
            self.screen.blit(text_surface, (self.screen_size[0] / 2 - 160, 250))
            text_surface = self.render.font_subtitle.render('1 - Liftoff', False, (255, 255, 255))
            self.screen.blit(text_surface, (self.screen_size[0] / 2 - 140, 350))
            text_surface = self.render.font_subtitle.render('2 - Binary', False, (255, 255, 255))
            self.screen.blit(text_surface, (self.screen_size[0] / 2 - 140, 450))
            text_surface = self.render.font_subtitle.render('3 - Bodies!', False, (255, 255, 255))
            self.screen.blit(text_surface, (self.screen_size[0] / 2 - 140, 550))
            text_surface = self.render.font_subtitle.render('4 - Interstellar', False, (255, 255, 255))
            self.screen.blit(text_surface, (self.screen_size[0] / 2 - 205, 650))
            # Right Button
            self.screen.blit(self.pg_right_btn, (self.screen_size[0] / 2 + 80, self.screen_size[1] - 150))
            # Left Button
            self.screen.blit(self.pg_left_btn, (self.screen_size[0] / 2 - 130, self.screen_size[1] - 150))
        if self.menu and (self.menu_page == 2):
            menu_bg = pg.image.load("Assignments/final/sprites/menu_bg.png")
            self.screen.blit(menu_bg, (0,0))
            text_surface = self.render.font_title.render('LEVEL SELECT', False, (255, 255, 255))
            self.screen.blit(text_surface, (self.screen_size[0] / 2 - 400, 30))
            text_surface = self.render.font_subtitle.render('CHAPTER II', False, (255, 255, 255))
            self.screen.blit(text_surface, (self.screen_size[0] / 2 - 150, 160))
            text_surface = self.render.font_subtitle.render('5 - Anomaly', False, (255, 255, 255))
            self.screen.blit(text_surface, (self.screen_size[0] / 2 - 160, 250))
            text_surface = self.render.font_subtitle.render('6 - Too Much Motion', False, (255, 255, 255))
            self.screen.blit(text_surface, (self.screen_size[0] / 2 - 270, 350))
            text_surface = self.render.font_subtitle.render('7 - Portal 3', False, (255, 255, 255))
            self.screen.blit(text_surface, (self.screen_size[0] / 2 - 170, 450))
            text_surface = self.render.font_subtitle.render('8 - More Portals!', False, (255, 255, 255))
            self.screen.blit(text_surface, (self.screen_size[0] / 2 - 230, 550))
            text_surface = self.render.font_subtitle.render('9 - Final Frontier', False, (255, 255, 255))
            self.screen.blit(text_surface, (self.screen_size[0] / 2 - 230, 650))
            # Left Button
            self.screen.blit(self.pg_left_btn, (self.screen_size[0] / 2 - 130, self.screen_size[1] - 150))
        if self.menu and (self.menu_page == 3):
            menu_bg = pg.image.load("Assignments/final/sprites/menu_bg.png")
            self.screen.blit(menu_bg, (0,0))
            text_surface = self.render.font_title.render('EXTRA MODES', False, (255, 255, 255))
            self.screen.blit(text_surface, (self.screen_size[0] / 2 - 350, 100))
    
    def draw_arrow(self):
        """
        Renders and performs operations relating to the launch velocity arrow indicator in pre-game phases.
        """
        if self.lvl != 10:
            # Putting arrow indicator
            indicator_vector =  Vector.asSpherical(self.velocity,0,(self.angle + 90) * (np.pi / 180))
            if indicator_vector.all() == 0:
                indicator_vector =  Vector.asSpherical(1,0,(self.angle + 90) * (np.pi / 180))
            iv_normalized = indicator_vector / indicator_vector.r
            iv_scaled = iv_normalized * 75
            i_pos_x = self.render.player.rect.x + iv_scaled.x
            i_pos_y = self.render.player.rect.y + iv_scaled.z
            # Rotate arrow
            angle_rad = math.atan2(-indicator_vector.z, indicator_vector.x)
            angle_deg = math.degrees(angle_rad)
            self.render.arrow.image = pg.transform.rotate(self.render.arrow.original_image, angle_deg)
            self.screen.blit(self.render.arrow.image, (i_pos_x,i_pos_y))

            # Draw power bar
            self.screen.blit(self.render.pbar.image, (50,50))
    
    def gui_displays(self):
        """
        Renders miscellaneous GUI elements and text.
        """
        # Display info - game timer
        if self.lvl != 10:
            if self.play:
                current_time = time.time()
                time_dif = current_time - self.time_start
                tutorial_time_dif = current_time - self.tutorial_time
                self.playtime = round(self.time_limit - time_dif, 1)
                self.pt_last = self.playtime
            elif (not self.play) and (not self.started):
                self.playtime = self.time_limit
        else:
            if self.play:
                current_time = time.time()
                self.playtime = round(current_time - self.time_start,1)
            elif (not self.play) and (not self.started):
                self.playtime = 0
        text_surface = self.render.font_subtitle.render(f'{self.playtime}s', False, (255, 255, 255))
        self.screen.blit(text_surface, (1360, 33))

        # Tutorial text
        if self.lvl == 0:
            current_time = time.time()
            tutorial_time_dif = current_time - self.tutorial_time

            text_surface = self.render.font_subtitle.render(f'Power', False, (255, 255, 255))
            self.screen.blit(text_surface, (210, 682))
            text_surface = self.render.font_subtitle.render(f'Angle', False, (255, 255, 255))
            self.screen.blit(text_surface, (210, 782))
            text_surface = self.render.font_subtitle.render(f'Restart', False, (255, 255, 255))
            self.screen.blit(text_surface, (130, 582))
            text_surface = self.render.font_subtitle.render(f'Menu', False, (255, 255, 255))
            self.screen.blit(text_surface, (170, 482))

            if (not self.play) and (not self.started):
                if (tutorial_time_dif >= 0) and (tutorial_time_dif < 2):
                    text_surface = self.render.font_title.render(f'Hey!', False, (255, 255, 255))
                    self.screen.blit(text_surface, (self.screen_size[0] / 2 - 100, self.screen_size[1] / 2 - 250))
                if (tutorial_time_dif >= 2) and (tutorial_time_dif < 5):
                    text_surface = self.render.font_title.render(f'Welcome to ASTROGOLF!', False, (255, 255, 255))
                    self.screen.blit(text_surface, (self.screen_size[0] / 2 - 635, self.screen_size[1] / 2 - 250))
                if (tutorial_time_dif >= 5) and (tutorial_time_dif < 8):
                    text_surface = self.render.font_title.render(f'Try to hit that flag.', False, (255, 255, 255))
                    self.screen.blit(text_surface, (self.screen_size[0] / 2 - 675, self.screen_size[1] / 2 - 250))
        
        if (self.lvl == 9) and (not self.play) and (not self.started):
            text_surface = self.render.font_title.render(f'Jetpack Unlocked!', False, (255, 255, 255))
            self.screen.blit(text_surface, (self.screen_size[0] / 2 - 465, 100))
            text_surface = self.render.font_subtitle.render(f'use W A S D to fly into the horizon', False, (255, 255, 255))
            self.screen.blit(text_surface, (self.screen_size[0] / 2 - 440, 250))
        
        # Jetpack Fuel Bar
        if self.jetpack_en and (not self.menu) and (not self.lvl == 0) and (not self.lvl == 10):
                text_surface = self.render.font_subtitle.render(f'FUEL', False, (255, 255, 255))
                self.screen.blit(text_surface, (50, 720))
                self.screen.blit(self.render.fbar.image, (50,800))
        
        # Draw arrow indicator and menu escape button
        if (not self.menu) and (not self.play) and (not self.started):
            self.draw_arrow()
            self.screen.blit(self.render.menu_btn2.image, (self.render.menu_btn2.rect.x,self.render.menu_btn2.rect.y))

        '''
        # Centerline
        centerline = pg.sprite.Sprite()
        centerline.image = pg.Surface([2, self.screen_size[1]])
        centerline.image.fill((255,255,255))
        self.screen.blit(centerline.image, (self.screen_size[0] / 2,0))
        '''

        # Start Menu
        if (not self.play) and (not self.started):
            self._startup()

    def update_fuelbar(self):
        """
        Handles changes to the jetpack fuel bar.
        """
        fuelbar_res = (150,55)

        if self.jetfuel > -10:
            # Play sound effect
            if not self.mute:
                sfx = pg.mixer.Sound("Assignments/final/sfx/jetpack.wav")
                if self.lvl != 10:
                    sfx.set_volume(0.7)
                else:
                    sfx.set_volume(0.2)
                sfx.play(loops=0)

        if self.jetfuel == 0:
            self.render.fbar.image = pg.image.load(f'Assignments/final/sprites/fuelbar/0.png').convert_alpha()
            self.render.fbar.image = pg.transform.scale(self.render.fbar.image, fuelbar_res)
        elif (self.jetfuel > 0) and (self.jetfuel < (self.jetfuel_max / 9)):
            self.render.fbar.image = pg.image.load(f'Assignments/final/sprites/fuelbar/1.png').convert_alpha()
            self.render.fbar.image = pg.transform.scale(self.render.fbar.image, fuelbar_res)
        elif (self.jetfuel > (self.jetfuel_max / 9)) and (self.jetfuel < ((2 * self.jetfuel_max) / 9)):
            self.render.fbar.image = pg.image.load(f'Assignments/final/sprites/fuelbar/1.png').convert_alpha()
            self.render.fbar.image = pg.transform.scale(self.render.fbar.image, fuelbar_res)
        elif (self.jetfuel > ((2 * self.jetfuel_max) / 9)) and (self.jetfuel < ((3 * self.jetfuel_max) / 9)):
            self.render.fbar.image = pg.image.load(f'Assignments/final/sprites/fuelbar/2.png').convert_alpha()
            self.render.fbar.image = pg.transform.scale(self.render.fbar.image, fuelbar_res)
        elif (self.jetfuel > ((3 * self.jetfuel_max) / 9)) and (self.jetfuel < ((4 * self.jetfuel_max) / 9)):
            self.render.fbar.image = pg.image.load(f'Assignments/final/sprites/fuelbar/3.png').convert_alpha()
            self.render.fbar.image = pg.transform.scale(self.render.fbar.image, fuelbar_res)
        elif (self.jetfuel > ((4 * self.jetfuel_max) / 9)) and (self.jetfuel < ((5 * self.jetfuel_max) / 9)):
            self.render.fbar.image = pg.image.load(f'Assignments/final/sprites/fuelbar/4.png').convert_alpha()
            self.render.fbar.image = pg.transform.scale(self.render.fbar.image, fuelbar_res)
        elif (self.jetfuel > ((5 * self.jetfuel_max) / 9)) and (self.jetfuel < ((6 * self.jetfuel_max) / 9)):
            self.render.fbar.image = pg.image.load(f'Assignments/final/sprites/fuelbar/5.png').convert_alpha()
            self.render.fbar.image = pg.transform.scale(self.render.fbar.image, fuelbar_res)
        elif (self.jetfuel > ((6 * self.jetfuel_max) / 9)) and (self.jetfuel < ((7 * self.jetfuel_max) / 9)):
            self.render.fbar.image = pg.image.load(f'Assignments/final/sprites/fuelbar/6.png').convert_alpha()
            self.render.fbar.image = pg.transform.scale(self.render.fbar.image, fuelbar_res)
        elif (self.jetfuel > ((7 * self.jetfuel_max) / 9)) and (self.jetfuel < ((8 * self.jetfuel_max) / 9)):
            self.render.fbar.image = pg.image.load(f'Assignments/final/sprites/fuelbar/7.png').convert_alpha()
            self.render.fbar.image = pg.transform.scale(self.render.fbar.image, fuelbar_res)
        elif (self.jetfuel > ((8 * self.jetfuel_max) / 9)) and (self.jetfuel < ((9 * self.jetfuel_max) / 9)):
            self.render.fbar.image = pg.image.load(f'Assignments/final/sprites/fuelbar/7.png').convert_alpha()
            self.render.fbar.image = pg.transform.scale(self.render.fbar.image, fuelbar_res)
        elif self.jetfuel == self.jetfuel_max:
            self.render.fbar.image = pg.image.load(f'Assignments/final/sprites/fuelbar/8.png').convert_alpha()
            self.render.fbar.image = pg.transform.scale(self.render.fbar.image, fuelbar_res)

    def initialize_sprites(self):
        """
        Initializes menu button sprites and some GUI elements.
        """
        self.levels_btn = pg.image.load("Assignments/final/sprites/levels_btn.png").convert_alpha()
        self.levels_btn = pg.transform.scale(self.levels_btn, (271,124))
        self.levels_btn_hbox = self.levels_btn.get_rect()
        self.levels_btn_hbox.topleft = (self.screen_size[0] / 2 - 330, self.screen_size[1] - 200) # x and y are the coordinates where the image is blitted

        self.extra_btn = pg.image.load("Assignments/final/sprites/extra_btn.png").convert_alpha()
        self.extra_btn = pg.transform.scale(self.extra_btn, (271,124))
        self.extra_btn_hbox = self.extra_btn.get_rect()
        self.extra_btn_hbox.topleft = (self.screen_size[0] / 2 + 40, self.screen_size[1] - 200)

        self.pg_right_btn = pg.image.load("Assignments/final/sprites/right_btn.png").convert_alpha()
        self.pg_right_btn = pg.transform.scale(self.pg_right_btn, (75,75))
        self.pg_right_btn_hbox = self.pg_right_btn.get_rect()
        self.pg_right_btn_hbox.topleft = (self.screen_size[0] / 2 + 80, self.screen_size[1] - 150)

        self.pg_left_btn = pg.image.load("Assignments/final/sprites/left_btn.png").convert_alpha()
        self.pg_left_btn = pg.transform.scale(self.pg_left_btn, (75,75))
        self.pg_left_btn_hbox = self.pg_left_btn.get_rect()
        self.pg_left_btn_hbox.topleft = (self.screen_size[0] / 2 - 130, self.screen_size[1] - 150)
    
    def set_statics(self):
        """
        Sets the positions of static level elements (e.g. black holes).
        """
        if (self.lvl == 3) and (not self.menu) and (not self.play) and (not self.started):
            self.model.gphobjects.state[0,:3] = [-10,0,3]
        elif self.play and (self.lvl == 4):
            self.model.gphobjects.state[1,:3] = [0,0,0]
        elif self.play and (self.lvl == 5):
            self.model.gphobjects.state[1,:3] = [11,0,-3]
        elif self.play and (self.lvl == 6):
            self.model.gphobjects.state[1,:3] = [2,0,6]
            self.model.gphobjects.state[2,:3] = [-3,0,0]
        elif self.play and (self.lvl == 6):
            self.model.gphobjects.state[1,:3] = [2,0,6]
            self.model.gphobjects.state[2,:3] = [-3,0,0]
        elif self.play and (self.lvl == 9):
            self.model.gphobjects.state[1,:3] = [0,0,0]
        elif self.play and (self.lvl == 10):
            self.model.gphobjects.state[2,:3] = [0,0,0]

    def restart_game(self):
        """
        Handles game restart events.
        """
        if self.lvl != 10:
            level = self.lvls[self.lvl]
            self.started = False
            self.play = False
            #self.velocity = 0
            #self.angle = 0
            # Reset model
            if self.lvl == 0:
                gphobjects = phobject.GravPhobjects(self.lvls[self.lvl].pos, self.lvls[self.lvl].vel, self.lvls[self.lvl].m)
                self.tutorial_time = time.time()
            gphobjects = phobject.GravPhobjects(level.pos, level.vel, level.m)
            self.model = model_final.NModel(gphobjects)
            self.render.rocket_pos = self.render._coord_transform((self.model.gphobjects.state[0,0],self.model.gphobjects.state[0,2]))
            # Reset player sprite
            if not self.jetpack_en:
                self.render.player.image = pg.image.load("Assignments/final/sprites/pixel_pack/Astronaut1.png").convert_alpha()
                self.render.player.image = pg.transform.scale(self.render.player.image, (50,50))
            else:
                self.render.player.image = pg.image.load("Assignments/final/sprites/pixel_pack/Astronaut1_jetpack.png").convert_alpha()
                self.render.player.image = pg.transform.scale(self.render.player.image, (50,50))
            # Reset bars
            self.render.pbar.image = pg.image.load(f'Assignments/final/sprites/pbar2/{self.velocity}.png').convert_alpha()
            self.render.pbar.image = pg.transform.scale(self.render.pbar.image, (328,60))
            self.render.fbar.image = pg.image.load(f'Assignments/final/sprites/fuelbar/8.png').convert_alpha()
            self.render.fbar.image = pg.transform.scale(self.render.fbar.image, (150,55))
            # Reset portal cooldown
            self.portal_cooldown = time.time()
            self.portal_last = time.time()
            # Reset jetpack
            self.jetfuel = 100
        else:
            # Multiplayer
            self.started = False
            self.play = False
            # Multiplayer
            pos, vel = self.randomize_asteroids()
            level = Level(pos=np.array([[-10,0,0],[10,0,0],[0,0,0],pos[0],pos[1],pos[2]]),
            vel=np.array([[0,0,0],[0,0,0],[0,0,0],vel[0],vel[1],vel[2]]),
            m=np.array([1,1,3,1,1,1]),
            time_limit=1)
            self.render.lvl = self.lvl
            self.time_limit = level.time_limit
            self.jetpack_en = True
            # Add sprites
            self.render.add_sprites(level=self.lvl, jp_en=self.jetpack_en)
            # Set up model
            gphobjects = phobject.GravPhobjects(level.pos, level.vel, level.m)
            self.model = model_final.NModel(gphobjects)
    
    def _mouse_handler(self):
        """
        Handles mouse hover effects.
        """
        # Hover effects
        if self.menu and (self.menu_page == 0):
            if (self.levels_btn_hbox.collidepoint(pg.mouse.get_pos())):
                self.levels_btn = self.levels_btn = pg.image.load("Assignments/final/sprites/levels_btn_hover.png").convert_alpha()
                self.levels_btn = pg.transform.scale(self.levels_btn, (271,124))
            elif (self.extra_btn_hbox.collidepoint(pg.mouse.get_pos())):
                if self.beat_game:
                    self.extra_btn = pg.image.load("Assignments/final/sprites/extra_btn_hover.png").convert_alpha()
                    self.extra_btn = pg.transform.scale(self.extra_btn, (271,124))
            else:
                self.levels_btn = self.levels_btn = pg.image.load("Assignments/final/sprites/levels_btn.png").convert_alpha()
                self.levels_btn = pg.transform.scale(self.levels_btn, (271,124))
                if self.beat_game:
                    self.extra_btn = pg.image.load("Assignments/final/sprites/extra_btn.png").convert_alpha()
                    self.extra_btn = pg.transform.scale(self.extra_btn, (271,124))
                else:
                    self.extra_btn = pg.image.load("Assignments/final/sprites/extra_btn_gray.png").convert_alpha()
                    self.extra_btn = pg.transform.scale(self.extra_btn, (271,124))
        elif self.menu and (self.menu_page != 3):
            if (self.pg_right_btn_hbox.collidepoint(pg.mouse.get_pos())):
                self.pg_right_btn = self.levels_btn = pg.image.load("Assignments/final/sprites/right_btn_hover.png").convert_alpha()
                self.pg_right_btn = pg.transform.scale(self.pg_right_btn, (75,75))
            elif (self.pg_left_btn_hbox.collidepoint(pg.mouse.get_pos())):
                self.pg_left_btn = pg.image.load("Assignments/final/sprites/left_btn_hover.png").convert_alpha()
                self.pg_left_btn = pg.transform.scale(self.pg_left_btn, (75,75))
            else:
                self.pg_right_btn = self.levels_btn = pg.image.load("Assignments/final/sprites/right_btn.png").convert_alpha()
                self.pg_right_btn = pg.transform.scale(self.pg_right_btn, (75,75))
                self.pg_left_btn = pg.image.load("Assignments/final/sprites/left_btn.png").convert_alpha()
                self.pg_left_btn = pg.transform.scale(self.pg_left_btn, (75,75))
        elif not self.menu:
            if (self.render.menu_btn.rect.collidepoint(pg.mouse.get_pos())):
                self.render.menu_btn.image = pg.image.load('Assignments/final/sprites/menubtn_hover.png').convert_alpha()
                self.render.menu_btn.image = pg.transform.scale(self.render.menu_btn.image, (165,102))
            else:
                self.render.menu_btn.image = pg.image.load('Assignments/final/sprites/menubtn.png').convert_alpha()
                self.render.menu_btn.image = pg.transform.scale(self.render.menu_btn.image, (165,102))
            if (self.render.menu_btn2.rect.collidepoint(pg.mouse.get_pos())):
                self.render.menu_btn2.image = pg.image.load('Assignments/final/sprites/menubtn_hover.png').convert_alpha()
                self.render.menu_btn2.image = pg.transform.scale(self.render.menu_btn2.image, (165,102))
            else:
                self.render.menu_btn2.image = pg.image.load('Assignments/final/sprites/menubtn.png').convert_alpha()
                self.render.menu_btn2.image = pg.transform.scale(self.render.menu_btn2.image, (165,102))
    
    def level_select(self):
        """
        Sets up the user-selected level with its associated model and parameters.
        """
        if self.lvl != 10:
            # Normal Levels
            level = self.lvls[self.lvl]
            self.render.lvl = self.lvl
            self.time_limit = level.time_limit

            # Add sprites
            self.render.add_sprites(level=self.lvl, jp_en=self.jetpack_en)

            # Set up model
            gphobjects = phobject.GravPhobjects(level.pos, level.vel, level.m)
            self.model = model_final.NModel(gphobjects)
            self.render.rocket_pos = self.render._coord_transform((self.model.gphobjects.state[0,0],self.model.gphobjects.state[0,2]))
        else:
            pos, vel = self.randomize_asteroids()
            # Multiplayer
            level = Level(pos=np.array([[-10,0,0],[10,0,0],[0,0,0],pos[0],pos[1],pos[2]]),
            vel=np.array([[0,0,0],[0,0,0],[0,0,0],vel[0],vel[1],vel[2]]),
            m=np.array([1,1,3,1,1,1]),
            time_limit=1)
            self.render.lvl = self.lvl
            self.time_limit = level.time_limit
            self.jetpack_en = True
            # Add sprites
            self.render.add_sprites(level=self.lvl, jp_en=self.jetpack_en)
            # Set up model
            gphobjects = phobject.GravPhobjects(level.pos, level.vel, level.m)
            self.model = model_final.NModel(gphobjects)

        # Close menu
        self.menu = False

        # Play sound effect
        if not self.mute:
            sfx = pg.mixer.Sound("Assignments/final/sfx/sfx_interface/menu_confirm_01.wav")
            sfx.set_volume(1)
            sfx.play(loops=0)
    
    def randomize_asteroids(self):
        """
        Randomizes the position and velocity of asteroids at the beginning of an endless game.
        """
        pos = []
        vel = []

        i = 0
        while i < 3:
            # Randomize asteroids
            a_spawn = random.randint(0,3)
            if a_spawn == 0:
                r_pos = [random.randint(-22,22),0,15]       # Set new position
            elif a_spawn == 1:
                r_pos = [random.randint(-22,22),0,-15]       # Set new position
            elif a_spawn == 2:
                r_pos = [22,0,random.randint(-15,15)]       # Set new position
            else:
                r_pos = [-22,0,random.randint(-15,15)]       # Set new position
            # SET NEW VELOCITY
            pos_vec_normalized = 10 * -(Vector(r_pos) / Vector(r_pos).mag)
            r_vel_x = pos_vec_normalized.x
            r_vel_z = pos_vec_normalized.z
            transformed_coords = self.render._coord_transform(r_pos)
            pos.append([transformed_coords[0],0,transformed_coords[1]])
            vel.append([r_vel_x,0,r_vel_z])

            i += 1

        return pos, vel

class Level():
    """
    Framework for a game level.

    Attributes
    ----------
    pos : list of float tuples
        An array of (x,y,z) coordinates, being the initial positions of each gravitational body in the level.
    vel : list of float tuples
        An array of (x,y,z) velocity vectors, being the initial velocities of each gravitational body in the level.
    m : list of floats
        An array containing the masses of each gravitational body in the level.
    time_limit : float
        Time limit of the level.
    """
    def __init__(self, pos, vel, m, time_limit):
        self.pos = pos
        self.vel = vel
        self.m = m
        self.time_limit = time_limit