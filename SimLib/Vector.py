# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 13:50:50 2016

@author: gtruch
"""
import numpy as np
import math

class Vector(np.ndarray):
    """Three dimensional vector to represent a point in 3-space

    Attributes
    ----------
    x,y,z : float
        cartesian components

    r,theta,phi : float
        Spherical components
    """

    def __new__(cls,x,y=0.0,z=0.0):
        """Let's get set up!

        ndarray uses __new__ rather than __init__.
        See numpy docs for further information

        Parameters
        ----------
        x,y,z : float
            Cartesian components

            If x is an iterable, x,y,and z will be set with its contents and
            named parameters y and z will be ignored. If the iterable in x
            contains fewer than three elements, the remaining elements will
            be filled with zeros.

            If x is not iterable, x, y, and z will be taken from the named
            parameters where y and z default to zero if not specified.
        """

        if isinstance(x,np.ndarray) and len(x) == 3:
            data = x   # Go fast if this is a numpy array
        else:

            try:

                # x is iterable. Use the data found in x
                d = np.array([float(d) for d in x])

                if len(d) > 3:
                    raise ValueError("Vectors can be initialized with " +
                                     "a maximum of 3 components")

                data = np.zeros(3)
                data[:len(d)] = d

            except TypeError:

                # x is not iterable.  Take data from named parameters
                data = np.array([float(x),float(y),float(z)])

        return np.asarray(data).view(cls)

    @classmethod
    def as_ndarray(cls,data):
        return np.asarray(data).view(cls)

    @classmethod
    def asSpherical(cls,r,theta,phi=np.pi/2):
        """Initialize with spherical coordinates

        Parameters
        ----------
        r, theta : float
            The magnitude and azimuthal angle (in radians) respectively

        phi : optional, float
            The polar angle in radians (default = pi/2)
        """

        x,y,z = cls._sphericalToCartesian(r,theta,phi)
        return cls(x,y,z)

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, value):
        self[0] = value

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, value):
        self[1] = value

    @property
    def z(self):
        return self[2]

    @z.setter
    def z(self, value):
        self[2] = value

    @property
    def r(self):
#        return float(np.sqrt(np.sum(self*self)))
        return float(np.sqrt(self[0]**2+self[1]**2+self[2]**2))

    @property
    def theta(self):
        return math.atan2(self.y,self.x)

    @property
    def phi(self):
        return math.atan2(math.sqrt(self.x**2+self.y**2),self.z)

    @r.setter
    def r(self,r):
        x,y,z = self._sphericalToCartesian(r,self.theta,self.phi)
        self.x = x
        self.y = y
        self.z = z

    @theta.setter
    def theta(self,theta):
        x,y,z = self._sphericalToCartesian(self.r,theta,self.phi)
        self.x = x
        self.y = y
        self.z = z

    @phi.setter
    def phi(self,phi):
        x,y,z = self._sphericalToCartesian(self.r,self.theta,phi)
        self.x = x
        self.y = y
        self.z = z

    @property
    def mag(self):
        return float(np.sqrt(np.sum(self*self)))

    @mag.setter
    def mag(self, magnitude):
        x,y,z = self._sphericalToCartesian(magnitude,self.theta,self.phi)
        self.x = x
        self.y = y
        self.z = z

    @property
    def unit(self):
        m = self.mag
        return Vector(self.x/m,self.y/m,self.z/m)
    
    @staticmethod
    def _sphericalToCartesian(r,theta,phi):
        """Convert sperical coordinates to cartesian

        Parameters
        ----------
        r, theta, phi : float
            The magnitude, azimuthal angle, and polar angle respectively

        Returns
        -------
        x, y, x : float
            The cartesian x, y, and z components respectively
        """

        return (r*math.sin(phi)*math.cos(theta),
                r*math.sin(phi)*math.sin(theta),
                r*math.cos(phi))

    def __sub__(self,other):
        return super().__sub__(Vector(other))
    
    def __add__(self,other):
        return super().__add__(Vector(other))
    
