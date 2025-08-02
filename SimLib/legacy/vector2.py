import math

def main():
    x = 1
    y = 2
    z = 3
    v1 = Vector(x, y, z)
    v2 = Vector(4, 5, 6)
    v3 = 8 * (v1 + v2)
    print('\nv3')
    print(f'x: {round(v3.x,3)}, y: {round(v3.y,3)}, z: {round(v3.z,3)}')
    print(f'Mag: {round(v1.mag,3)}')
    print(f'Theta: {round(v1.theta,3)}')
    print(f'Phi: {round(v1.phi,3)}')

class Vector:
    """
    Represents a three-dimensional vector, storing magnitude and direction data in Spherical coordinates.

    ...

    Attributes
    ----------
    x : float
        Vector magnitude in the x direction (Cartesian)
    y : float
        Vector magnitude in the y direction (Cartesian)
    z : float
        Vector magnitude in the z direction (Cartesian)
    mag : float
        Vector magnitude (Spherical)
    theta : float
        Horizontal angle between the x-axis and the vector, increasing from 0 to 360 degrees moving counter-clockwise through the x-y plane. (Spherical)
    phi : float
        Vertical angle between the z-axis and the vector, increasing from 0 to 180 degrees moving clockwise down from the z-axis. (Spherical)

    Methods
    -------
    cartesian_to_spherical():
        Converts the vector's cartesian components to spherical components.
    spherical_to_cartesian():
        Converts the vector's spherical components to cartesian components.
    """

    def __init__(self, x, y, z):
        """
        Constructs all the necessary attributes for the Vector object, converting input Cartesian components into Spherical components.

        Parameters
        ----------
            x : float
                Vector magnitude in the x direction (Cartesian)
            y : float
                Vector magnitude in the y direction (Cartesian)
            z : float
                Vector magnitude in the z direction (Cartesian)
        """
        self.mag = math.sqrt(x**2 + y**2 + z**2)
        if (y >= 0):
            self.theta = math.atan2(y, x)   # radians
        else:
            self.theta = (2 * math.pi) - abs(math.atan2(y, x))  # radians
        self.phi = math.acos(z / self.mag) # radians
    
    @property
    def x(self):
        x = self.mag * math.sin(self.phi) * math.cos(self.theta)
        return x
    @x.setter
    def x(self,x_new):
        (x, y, z) = self.spherical_to_cartesian()
        (self.mag, self.theta, self.phi) = self.cartesian_to_spherical(x_new, y, z)

    @property
    def y(self):
        y = self.mag * math.sin(self.phi) * math.sin(self.theta)
        return y
    @y.setter
    def y(self,y_new):
        (x, y, z) = self.spherical_to_cartesian()
        (self.mag, self.theta, self.phi) = self.cartesian_to_spherical(x, y_new, z)

    @property
    def z(self):
        z = self.mag * math.cos(self.phi)
        return z
    @z.setter
    def z(self,z_new):
        (x, y, z) = self.spherical_to_cartesian()
        (self.mag, self.theta, self.phi) = self.cartesian_to_spherical(x, y, z_new)

    def cartesian_to_spherical(self, x, y, z):
        """
        Converts the vector's cartesian components to spherical components.

        Returns
        -------
        mag : float
            Vector magnitude (Spherical)
        theta : float
            Horizontal angle between the x-axis and the vector, increasing from 0 to 360 degrees moving counter-clockwise through the x-y plane. (Spherical)
        phi : float
            Vertical angle between the z-axis and the vector, increasing from 0 to 180 degrees moving clockwise down from the z-axis. (Spherical)
        """
        mag = math.sqrt(x**2 + y**2 + z**2)
        if (y >= 0):
            theta = math.atan2(y, x)
        else:
            theta = (2 * math.pi) - abs(math.atan2(y, x))
        phi = math.acos(z / self.mag) # radians

        return mag, theta, phi
    
    def spherical_to_cartesian(self):
        """
        Converts the vector's spherical components to cartesian components.

        Parameters
        ----------
        mag : float
            Vector magnitude (Spherical)
        theta : float
            Horizontal angle between the x-axis and the vector, increasing from 0 to 360 degrees moving counter-clockwise through the x-y plane. (Spherical)
        phi : float
            Vertical angle between the z-axis and the vector, increasing from 0 to 180 degrees moving clockwise down from the z-axis. (Spherical)

        Returns
        -------
        x : float
            Vector magnitude in the x direction (Cartesian)
        y : float
            Vector magnitude in the y direction (Cartesian)
        z : float
            Vector magnitude in the z direction (Cartesian)
        """
        return self.x, self.y, self.z
    
    def __add__(self, other):
        if isinstance(other, Vector):
            (x_self, y_self, z_self) = self.spherical_to_cartesian()
            (x_other, y_other, z_other) = other.spherical_to_cartesian()
            
            return Vector(x_self + x_other, y_self + y_other, z_self + z_other)
        
    def __mul__(self,scalar):
        if not isinstance(scalar, Vector):
            (x, y, z) = self.spherical_to_cartesian()
            return Vector(x * scalar, y * scalar, z * scalar)
        
    def __rmul__(self,scalar):
        if not isinstance(scalar, Vector):
            (x, y, z) = self.spherical_to_cartesian()
            return Vector(x * scalar, y * scalar, z * scalar)

if __name__ == "__main__":
    main()