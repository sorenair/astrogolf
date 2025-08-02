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
from SimLib import physics
from SimLib import phobject
from SimLib import solver
import math
import numpy as np

class TrajectoryModel():
    '''Model the trajectory of a single projectile in a uniform g field.
    
    Attributes
    ----------
    projectile : Phobject
        The projectile.  
                
    time : float
        The current simulation time
    
    '''
    
    def __init__(self,p0,v0,dt_max=0.1):
        '''Assemble the model!
        
        Parameters
        ----------
        p0 : Vector
            The initial position of the projectile
            
        v0 : Vector
            The initial velocity of the projectile
            
        dt_max : optional float
            The maximum allowable time step.  
        '''                

        self.gravity = physics.UniformGravity(solver.RK4,0)
        self.projectile = phobject.GravPhobject(0,p0,v0)
        self.dt_max = dt_max
        self.time = 0

    def advance(self, dt):
        '''Advance the model by the requested increment.

        If dt>dt_max, the model will advance in increments of dt_max until
        the requested time is reached.
        
        Parameters
        ----------
        dt : float
            The desired time increment
        
        '''
        self.time, self.projectile = self.gravity.step(self.time,self.projectile,dt)

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
        
class OrbitModel():
    '''
    Model the orbit of an array of planets.
    
    Attributes
    ----------
    projectile : Phobject
        The orbitals.  
                
    time : float
        The current simulation time
    
    '''
    
    def __init__(self,M,a,e,m,names=[],dt_max=0.1):
        '''Assemble the model!
        
        Parameters
        ----------
        M : float
            Central attractor mass (kg).
        a : float
            Orbital semi-major axis.           
        e : float
            Orbital eccentricity.
            
        dt_max : optional float
            The maximum allowable time step.  
        '''
        # Instantiate system and central attractor
        self.M = M
        self.G = 6.6743E-11
        self.gravity = physics.CentralGravity(solver.RK4, M)
        self.dt_max = dt_max
        self.time = 0

        # Instantiate orbital bodies
        self.a = a
        self.e = e
        self.m = m
        self.names = names
        r0 = [(a * (1 - self.e[index])) for index,a in enumerate(self.a)]
        #r0 = a * (1 - e)
        v0 = [(math.sqrt(((self.G * self.M) / a) * ((1 + self.e[index]) / (1 - self.e[index])))) for index,a in enumerate(self.a)]
        #v0 = math.sqrt(((self.G * self.M) / a) * ((1 + e) / (1 - e)))
        
        self.orbitals = []
        for i,planet_name in enumerate(self.names):
            self.orbitals.append(phobject.GravPhobject(self.m[i], (r0[i],0,0), (0,0,v0[i])))

    def advance(self, dt):
        '''
        Advance the model by the requested increment.

        If dt>dt_max, the model will advance in increments of dt_max until
        the requested time is reached.
        
        Parameters
        ----------
        dt : float
            The desired time increment
        
        '''
        for i,orbital in enumerate(self.orbitals):
            t_new, self.orbitals[i] = self.gravity.step(self.time,orbital,dt)
        
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

class SolarSystem(OrbitModel):
    """
    Model our solar system.
    
    Inherits from the OrbitModel class and is responsible for simulating several orbitals.
    """

    def __init__(self):
        solar_mass = 1.989E+30
        a = [57909036552, 1.08159e+11, 1.496e+11, 2.27987e+11, 4.488e+11]
        e = [0.206, 0.0068, 0.0167, 0.0934, 0.9]
        planet_masses = [3.285E23,4.867E24,5.972E+24,6.41693E23,2.2E14]
        names = ['Mercury','Venus','Earth','Mars','Comet']

        super().__init__(solar_mass,a,e,planet_masses,names)

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
        self.nbody = physics.NBody(solver.RK4,self.gphobjects)
        self.time = 0

        # Center origin position
        num = np.sum(self.gphobjects.state * self.gphobjects.m[:,np.newaxis],0)
        den = np.sum(self.gphobjects.m[:,np.newaxis],0)
        cm_state = num / den
        #self.r_cm = cm_state[:3]
        #self.v_cm = cm_state[3:]

        # Normalize phobjects / adjust origin
        self.gphobjects.state = self.gphobjects.state - cm_state

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

class SlingShot(NModel):
    """
    Model of a gravitational slingshot N-body system.
    
    Inherits from the NModel class and is responsible for simulating several gravitational bodies.
    """

    def __init__(self):
        '''
        Assembles the model.

        In order, the GravPhobjects array of N-bodies created represents the Sun, Earth, Jupiter, and a satellite (following the launch method).
        '''
        # Planets - Sun, Earth, Jupiter, Satellite
        pos = np.array([[0,0,0],[1,0,0],[5,0,0]])
        vel = np.array([[0,0,0],[0,0,6.3],[0,0,3]])
        m = np.array([1,0.000003003,0.000954])
        planets = phobject.GravPhobjects(pos, vel, m)
        super().__init__(planets)

    def launch(self, velo_scalar=1.4):
        '''
        Launches a satellite from Earth - i.e. adds a satellite GPhob to the model's gphobjects array at the specified launch time.

        Parameters
        ----------
        velo_scalar : float
            Scalar applied to Earth's velocity vector at the launch time to generate the satellite's initial velocity.
        '''
        # Add satellite
        earth = self.gphobjects[1]
        dir = earth.vel * (earth.vel.r**-1)
        pos = earth.pos + (0.001 * dir)
        vel = earth.vel * velo_scalar
        satellite_state = np.hstack((pos,vel))
        self.gphobjects.state = np.vstack((self.gphobjects.state,satellite_state))
        self.gphobjects.m = np.hstack((self.gphobjects.m, 5.02785e-28))