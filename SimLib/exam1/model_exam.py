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
from SimLib.exam1 import physics_exam as physics
from SimLib import phobject
from SimLib import solver
import math

class TrajectoryModel():
    '''Model the trajectory of a single projectile in a uniform g field.
    
    Attributes
    ----------
    projectile : Phobject
        The projectile.  
                
    time : float
        The current simulation time
    
    '''
    
    def __init__(self,p0,v0,dc=0,dt_max=0.1):
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

        self.gravity = physics.UniformGravity(solver.RK4,0,dc)
        self.projectile = phobject.GravPhobject(0.145,p0,v0)
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
    '''Model the orbit of a single projectile.
    
    Attributes
    ----------
    projectile : Phobject
        The projectile.  
                
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
        '''Advance the model by the requested increment.

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