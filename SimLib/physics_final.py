# -*- coding: utf-8 -*-

import numpy as np

"""
The Physics base class and its children
This set of classes implements various differential equations that represent 
different physical environments.  They are inteded for use with the 
differential equation solving classes derived from Solver.
"""

class Physics(object):
    """Base class for Physics objects. 
    
    Attributes
    ----------
    Solver : type
        A class derived from Solver which will be internally instantiated.        
    """
    def __init__(self,solver):
        self.solver = solver(self.diff_eq)

    def step(self,t,phob,dt):
        """Advance the solution one time step
        
        This advance implementation in the Physics base class is a stub.
        It exists only to define the interface for the advance method.
        Classes derived from Physics should define their own versions of 
        advance following the same interface.
        
        Parameters
        ----------
        t : float
            The current time
            
        phob : Phobject
            An instance of a class derived from Phobject
            
        dt : float
            The amount of time to advance. (the time step)
        
        Returns
        -------
        time : float
            The new time

        phob : Phobject
            The Phobject advanced one time step        
        """
        
        t, phob.state = self.solver.step(t, phob.state, dt)
        
        return t, phob
    
    def diff_eq(self,t,f,phob=None):
        """The cooling differential equation
        
        This diff_eq implementation in the Physics base class is a stub.
        It exists only to define the interface for the advance method.
        Classes derived from Physics should define their own versions of 
        advance following the same interface.

        Parameters
        ----------
        T : float
            The current temperature of the object
            
        t : float
            The current time
            
        params : object
            A reference to an object containing non-state attributes
        
        Returns
        -------
        dfdt : float
            The slope at T        
        """
        print("Physics.diff_eq is a stub!  This line should never be executed")
        return          # Do nothing, simply return.
    
class NBody(Physics):
    """
    Encodes the differential equations for an N-body physical system.

    Attributes
    ----------
    solver : Solver
        An instance of a class derived from Solver to solve the differential
        equation
    grav_bodies : GravPhobjects
        The physical bodies.
    G : Netwon's gravitational constant in Kepler units.
    """

    def __init__(self,solver,grav_bodies):
        super().__init__(solver)
        self.gphobjects = grav_bodies
        self.G = 4*(np.pi**2)
        
    def step(self,t,body,dt,params=None):
        """
        See class Physics for full docstring.
        """
        (tnext, fnew) = self.solver.step(t,body.state,dt,params=body)
        body.state = fnew

        return tnext, body
            
    def diff_eq(self,t,f,params):
        '''
        Calculates the velocities and accelerations of each N-body phobject.

        Parameters
        ----------
        t : float
            The current time.   
        f : NDArray
            State array of all GravPhobjects
            The first 3 columns are position and the latter 3 are velocity.
            Each row represents a different Phobject.
        params : GravPhobjects
            A reference to the GravPhobjects object containing non-state attributes.
        
        Returns
        -------
        state : NDArray
            Updated velocities and accelerations of each GravPhobject.
        '''
        pos = f[:,:3]
        n = f.shape[0]

        pos = pos[:,:,None]
        pos = pos.transpose((1,0,2))
        o = np.ones((3,n,n))

        cube = pos * o
        cube2 = cube.transpose((0,2,1))

        diff = cube - cube2     # r matrix / distances between objects
        diff_sq = diff**2
        d2 = np.sum(diff_sq,axis=0)
        d2 = d2 + np.eye(n)
        denominator = (d2**(-3/2))

        masses = params.m[:,np.newaxis]
        masses = masses.transpose((1,0))
        masses = masses * o

        accel = -(denominator * diff * masses * self.G)
        a_sum = np.sum(accel,axis=2)
        a_sum = a_sum.T

        v = f[:,3:]
        state = np.hstack((v,a_sum))

        return state