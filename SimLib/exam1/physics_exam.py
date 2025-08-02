# -*- coding: utf-8 -*-

import numpy as np
import Vector

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

    
class Cooling(Physics):
    """
    Implements cool cooling.

    Attributes
    ----------
    solver : Solver
        An instance of a class derived from Solver to solve the differential
        equation
        
    Ta : float
        The ambient temperature
    """
    
    def __init__(self,solver,Ta):
        super().__init__(solver)
        self.Ta = Ta
        
    def step(self,t,body,dt):
        """
        See class Physics for full docstring.
        """
        (tnext, temp_next) = self.solver.step(t,body.temperature,dt,params=body)
        body.temperature = temp_next
        return tnext, body
            
    def diff_eq(self,t,T,params):
        '''
        Calculates the derivative of temperature using the cooling differential equation.

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
            The slope at t
        '''
        dT = params.k * (self.Ta - T)
        return dT

class UniformGravity(Physics):
    """
    Encodes the 6 coupled differential equations for a fixed cental attractor.

    Attributes
    ----------
    solver : Solver
        An instance of a class derived from Solver to solve the differential
        equation

    mass : float
        The central attractor's mass.
    """
    
    def __init__(self,solver,mass,dc=0):
        super().__init__(solver)
        self.mass = mass
        self.dc = dc
        self.g = 9.7
        
    def step(self,t,body,dt,params=None):
        """
        See class Physics for full docstring.
        """
        pos = [body.pos.x, body.pos.y, body.pos.z]
        vel = [body.vel.x, body.vel.y, body.vel.z]
        state_array = np.array(pos + vel)
        
        (tnext, fnew) = self.solver.step(t,state_array,dt,params=body)
        body.pos.x = fnew[0]
        body.pos.y = fnew[1]
        body.pos.z = fnew[2]
        body.vel.x = fnew[3]
        body.vel.y = fnew[4]
        body.vel.z = fnew[5]
        return tnext, body
            
    def diff_eq(self,t,f,params):
        '''
        Calculates the derivative of temperature using the uniform gravity differential equation.

        Parameters
        ----------
        t : float
            The current time.   
        f : NDArray
            Force.
        params : object
            A reference to an object containing non-state attributes.
        
        Returns
        -------
        dfdt : float
            The slope at t
        '''
        velocity = Vector.Vector(f[3],f[4],f[5])

        # Acceleration
        ax = (-self.dc / params.mass) * velocity.mag * velocity.x
        ay = (-self.dc / params.mass) * velocity.mag * velocity.y
        az = -self.g - ((self.dc / params.mass) * velocity.mag * velocity.z)

        # Velocity
        vx = velocity.x
        vy = velocity.y
        vz = velocity.z

        return np.array([vx, vy, vz, ax, ay, az])
    
class CentralGravity(Physics):
    """
    Encodes the 6 coupled differential equations for a fixed cental attractor.

    Attributes
    ----------
    solver : Solver
        An instance of a class derived from Solver to solve the differential
        equation

    mass : float
        The central attractor's mass.
    """
    
    def __init__(self,solver,mass):
        super().__init__(solver)
        self.mass = mass
        self.G = 6.6743E-11
        
    def step(self,t,body,dt,params=None):
        """
        See class Physics for full docstring.
        """
        pos = [body.pos.x, body.pos.y, body.pos.z]
        vel = [body.vel.x, body.vel.y, body.vel.z]
        state_array = np.array(pos + vel)
        
        (tnext, fnew) = self.solver.step(t,state_array,dt,params=body)
        body.pos.x = fnew[0]
        body.pos.y = fnew[1]
        body.pos.z = fnew[2]
        body.vel.x = fnew[3]
        body.vel.y = fnew[4]
        body.vel.z = fnew[5]
        return tnext, body
            
    def diff_eq(self,t,f,params):
        '''
        Calculates the derivative of temperature using the central gravity differential equation.

        Parameters
        ----------
        t : float
            The current time.   
        f : NDArray
            Position and velocity vectors, with f[0-2] being (x,y,z) coordinates and f[3-5] being velocity components.
        params : object
            A reference to an object containing non-state attributes.
        
        Returns
        -------
        dfdt : float
            The slope at t
        '''
        Fconstant = -(self.G * self.mass) / (((f[0]**2) + (f[1]**2) + (f[2]**2))**(3/2))
        Fx = Fconstant * f[0]
        Fy = Fconstant * f[1]
        Fz = Fconstant * f[2]

        # Acceleration
        ax = Fx
        ay = Fy
        az = Fz

        # Velocity
        vx = f[3]
        vy = f[4]
        vz = f[5]

        return np.array([vx, vy, vz, ax, ay, az])