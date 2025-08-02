# -*- coding: utf-8 -*-
"""
The Solver base class and its children
This set of classes implements various differential equation solving 
algorithms.  They are intended for use with the classes derived from Physics.
"""

class Solver(object):
    """Differential equation solver base class.
    
    Attributes
    ----------
    diff_eq : Callable
        A reference to a diff_eq function 
    
    """
    
    def __init__(self,diff_eq):
        self.diff_eq = diff_eq
                        
    def step(self,x,f,dx,params=None):
        ''' Advance a differential equation one step
        
        This advance implementation in the Solver base class is a stub.
        It exists only to define the interface for the advance method.
        Classes derived from Solver should define their own versions of 
        advance following the same interface.
        
        Parameters
        ----------
        x : float
            The independent variable

        f : float or ndarray of floats
            A the dependent variables
                        
        dx : float
            The step size
            
        params : optional object
            A reference to an object containing non-state attributes for the 
            differential equation
            default = None
            
        Returns
        -------
        xnext : float
            The value of the independent variable at the next step

        fnext : float
            The value of the dependent variable at the next step            
        '''
        print("Solver.step is a stub!  This line should never be executed")
        return          # Do nothing, simply return.
                

class Euler(Solver):
    """
    Euler's method for differential equation solving.
    
    ...

    Attributes
    ----------
    diff_eq : method
        Differential equation to solve.

    Methods
    -------
    step():
        see Solver class for full docstring.
    """
    def __init__(self,diff_eq):
        super().__init__(diff_eq)
            
    def step(self,x,f,dx,params=None):
        """
        See class Solver for full docstring
        """
        xnext = x + dx
        fnext = f + (dx * self.diff_eq(x, f, params))

        return xnext, fnext
    
class RK2(Solver):
    """
    Second order Runge-Kutta method for differential equation solving.

    ...

    Attributes
    ----------
    diff_eq : method
        Differential equation to solve.

    Methods
    -------
    step():
        see Solver class for full docstring.
    """
    def __init__(self,diff_eq):
        super().__init__(diff_eq)
            
    def step(self,x,f,dx,params=None):
        """
        See class Solver for full docstring.
        """
        k1 = self.diff_eq(x, f, params)
        k2 = self.diff_eq(x + (0.5*dx), f + (0.5*k1*dx), params)
        xnext = x + dx
        fnext = f + (k2*dx)

        return xnext, fnext
    
class RK4(Solver):
    """
    Fourth order Runge-Kutta method for differential equation solving.

    ...

    Attributes
    ----------
    diff_eq : method
        Differential equation to solve.

    Methods
    -------
    step():
        see Solver class for full docstring.
    """
    def __init__(self,diff_eq):
        super().__init__(diff_eq)
            
    def step(self,x,f,dx,params=None):
        """
        See class Solver for full docstring.
        """
        k1 = self.diff_eq(x, f, params)
        k2 = self.diff_eq(x + (0.5*dx), f + (0.5*k1*dx), params)
        k3 = self.diff_eq(x + (0.5*dx), f + (0.5*k2*dx), params)
        k4 = self.diff_eq(x + dx, f + (k3*dx), params)

        xnext = x + dx
        fnext = f + (((k1 + (2*k2) + (2*k3) + k4) * dx) / 6)

        return xnext, fnext