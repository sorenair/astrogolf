import pygame as pg
import numpy as np

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
    
    def __init__(self, model, render, screen_size=[600,400], timescale=1):
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

        self.model = model
        self.render = render
        self.screen_size = screen_size
        self.done = False
        self.time = 0
        self.timescale = timescale

        self.screen = pg.display.set_mode(self.screen_size)
        pg.init()

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
            self._event_handler()

            # Update the model
            self.model.advance(self.elapsed_time*self.timescale)

            # Launch satellite
            if (round(self.model.time,2) == 0.82) and (len(self.model.gphobjects.state) < 4):
                self.model.launch(velo_scalar=1.387)

            # Draw the picture
            self.screen.fill((0,0,0))       # Clear screen
            self.render.render(self.model, self.screen)

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
        time = pg.time.get_ticks()
        self.elapsed_time = time-self.previous_time
        self.previous_time = time

    def _event_handler(self):
        """
        Handles user input events, including quitting the animation and
        detecting key presses such as the escape key to exit.
        """
        for event in pg.event.get():
            # Closing the pygame window causes a Quit event
            if event.type == pg.QUIT:
                self.done = True

            # Look for the escape key
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.done = True
                elif event.key == pg.K_SPACE:
                    self.model.launch()