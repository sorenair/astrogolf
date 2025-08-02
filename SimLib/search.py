# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 17:49:54 2020

"""
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from SimLib import Vector


class Bisection():
    """Performs a bisection search to precicely locate the zero of a function

    Attributes
    ----------
    right : float
        The right bracket

    left : float
        The left bracket

    right_error : float
        The error signal at the right bracket

    left_error : float
        The error signal at the left bracket

    """

    def __init__(self,left_bracket,right_bracket,func):
        """Create a Bisection object

        Parameters
        ----------
        left_bracket : float
            The left bracket

        right_bracket : float
            The right bracket

        func : function
            The function to be evaluated
        """
        self.left = left_bracket
        self.right = right_bracket
        self.func = func
        self.left_error = abs(self.func(self.left))
        self.right_error = abs(self.func(self.right))

    def iterate_until(self,tolerance):
        midpoint, error = self.iterate()
        while error > tolerance:
            midpoint, error = self.iterate()

        return midpoint

    def iterate(self):
        """Performs a single iteration of the bisection search
        
        Returns
        -------
        current best parameter estimate and current error estimate
        """
        param, midpoint = self.param()
        if (round(param,2)) == 0:           # Set resolution with rounding decimal count
            return midpoint, 0
        elif (param * self.func(self.left) < 0):
            self.right = midpoint
            error = self.error(param)
            return midpoint, error
        elif (param * self.func(self.left) > 0):
            self.left = midpoint
            error = self.error(param)
            return midpoint, error

    def param(self):
        """The current best estimate of the parameter"""
        midpoint = (self.left + self.right) / 2
        param = self.func(midpoint)

        return param, midpoint

    def error(self,param):
        """The estimated error"""
        error = abs(param)
        return error
    
class GoldenSection():
    """
    Performs a Golden Section search to find minimum of a function

    Attributes
    ----------

    """

    def __init__(self,left_bracket,right_bracket,func):
        """Create a Bisection object

        Parameters
        ----------
        func : function
            The function to be evaluated
        """
        self.left = left_bracket
        self.right = right_bracket
        self.func = func

        # Calculate initial midpoint positions
        self.R = 0.5*(5**0.5 - 1)
        l = (self.right - self.left) * self.R
        self.m1 = self.left + l
        self.m2 = self.right - l
        # Calculate initial values
        self.f_m1 = self.func(self.m1)
        self.f_m2 = self.func(self.m2)

    def iterate_until(self,tolerance):
        error = self.iterate()
        while error > tolerance:
            error = self.iterate()

        time_min = (self.left + self.right) / 2
        return time_min
    
    def iterate(self):
        """Performs a single iteration of the bisection search
        
        Returns
        -------
        current best parameter estimate and current error estimate
        """
        if (self.f_m1  <= self.f_m2):
            self.left = self.m2
            self.m2 = self.m1
            self.f_m2 = self.f_m1
            self.m1 = self.left + (self.R * (self.right - self.left))
            self.f_m1 = self.func(self.m1)
            
            error = abs(self.right - self.left)
            
            return error
        elif (self.f_m1 > self.f_m2):
            self.right = self.m1
            self.m1 = self.m2
            self.f_m1 = self.f_m2
            self.m2 = self.right - (self.R * (self.right - self.left))
            self.f_m2 = self.func(self.m2)
            
            error = abs(self.right - self.left)
            
            return error
        
    def param(self):
        """Parameter values (e.g. positions) at both midpoints"""
        self.f_m1 = self.func(self.m1)
        self.f_m2 = self.func(self.m2)