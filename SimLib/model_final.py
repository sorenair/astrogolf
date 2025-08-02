# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 20:26:52 2023

@author: Fred
"""

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from SimLib import physics_final
from SimLib import phobject
from SimLib import solver
import math
import numpy as np

class NModel():
    '''
    Model the interactions of an array of massive bodies.
    
    Attributes
    ----------
    gphobjects : GravPhobjects
        The physical bodies.     
    nbody : NBody
        NBody physics simulation engine.
    time : float
        Current simulation time.
    '''

    def __init__(self, grav_bodies):
        '''
        Assembles the model
        
        Parameters
        ----------
        grav_bodies : GravPhobjects
            The physical bodies. 
        '''
        self.gphobjects = grav_bodies
        self.nbody = physics_final.NBody(solver.RK4,self.gphobjects)
        self.time = 0

        ''' NORMALIZE POSITIONS
        # Center origin position
        num = np.sum(self.gphobjects.state * self.gphobjects.m[:,np.newaxis],0)
        den = np.sum(self.gphobjects.m[:,np.newaxis],0)
        cm_state = num / den

        # Normalize phobjects / adjust origin
        self.gphobjects.state = self.gphobjects.state - cm_state
        '''

    def advance(self, dt):
        '''
        Advance the model by the requested time increment.

        If dt>dt_max, the model will advance in increments of dt_max until
        the requested time is reached.
        
        Parameters
        ----------
        dt : float
            The desired time increment
        '''
        dt_max = 0.001
        t_new = self.time

        if dt < dt_max:
            t_new, self.gphobjects = self.nbody.step(t=self.time, body=self.gphobjects, dt=dt)
        else:
            while t_new < self.time + dt:
                t_new, self.gphobjects = self.nbody.step(t=t_new, body=self.gphobjects, dt=dt_max)
        
        self.time = t_new

    def advance_to(self, t):
        '''Advance the model to the requested time.

        Calculates the difference between the requested time and the current
        time, then calls advance() with that difference.

        Parameters
        ----------
        t : float
            The desired time stamp
        '''
        delta_t = t - self.time
        self.advance(delta_t)