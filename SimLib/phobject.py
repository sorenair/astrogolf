# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from SimLib.Vector import Vector

"""
Classes representing physical objects
This set of classes represents physical objects.  It is primarily a way to 
keep track of the attributes (temperature, position, velocity, etc) of objects
in the simulator.  They are inteded for use with the Physics classes.
"""

class ThermalPhobject(object):
    '''
    An object that has a temperature.

    Attributes
    ----------
    temperature : float
        The current temperature of the object
        
    k : float
        The cooling constant
    '''
    
    def __init__(self, temperature, k):
        self.temperature = temperature
        self.k = k

class GravPhobject(object):
    '''
    A massive object of arbitrary position and velocity.

    Attributes
    ----------
    mass : float
        The mass of the object (kg). 
    pos : Vector
        The object's position in Cartesian coordinates, i.e. (x,y,z) format.
    vel : Vector
        The object's velocity with Cartesian components.
    '''
    
    def __init__(self, mass, pos, vel):
        self.mass = mass
        self.pos = Vector(pos)
        self.vel = Vector(vel)

class GravPhobjects():
    '''A collection of gravitational phobjects.
    
    Primarily an interface into to the state matrix 
    
    Attributes
    ----------
    state : nx6 ndarray of floats
        Each row is an object, the first three columns are position
        the second three columns are velocity
    '''
    
    def __init__(self,pos,vel,m):
        '''Let's get this party started        
        Parameters
        ----------
        pos : nx3 array of floats
            The cartesian components of each object's position 
        
        vel : nx3 array of floats
            The cartesian components of each object's velocity
        
        m : array of masses
            The mass of each object
        '''
        
        # Create a state matrix with the positions and velocities
        self.state = np.hstack((np.array(pos),np.array(vel)))
        self.m = np.array(m)
    
    def get_gphob(self,index):
        '''Fetch the gravphob at the the correct index.'''
        
        
        # Fetch the correct phobject
        return GravPhobject(
                pos=Vector(self.state[index,:3]),
                vel=Vector(self.state[index,3:]),
                mass=self.m[index])
        
        
    def __getitem__(self,index):
        '''Override the square brackets to fetch a phobject from the set'''
        return self.get_gphob(index)      