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
    Represents a three-dimensional vector, storing magnitude and direction data in Cartesian coordinates.

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
        Constructs all the necessary attributes for the Vector object.

        Parameters
        ----------
            x : float
                Vector magnitude in the x direction (Cartesian)
            y : float
                Vector magnitude in the y direction (Cartesian)
            z : float
                Vector magnitude in the z direction (Cartesian)
        """
        self.x = x
        self.y = y
        self.z = z
    
    @property
    def mag(self):
        mag = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        return mag
    
    @mag.setter
    def mag(self,mag_new):
        unit_vector = self * (1/self.mag)
        self.x = unit_vector[0] * mag_new
        self.y = unit_vector[1] * mag_new
        self.z = unit_vector[2] * mag_new
    
    @property
    def theta(self):
        if (self.y >= 0):
            theta = math.atan2(self.y, self.x)
        else:
            theta = (2 * math.pi) - abs(math.atan2(self.y, self.x))

        return theta        # radians
    
    @theta.setter
    def theta(self, theta_new):
        (mag, theta, phi) = self.cartesian_to_spherical()
        (self.x, self.y, self.z) = self.spherical_to_cartesian(mag, theta_new, phi)
    
    @property
    def phi(self):
        phi = math.acos(self.z / self.mag) # radians
        return phi

    @phi.setter
    def phi(self, phi_new):
        (mag, theta, phi) = self.cartesian_to_spherical()
        (self.x, self.y, self.z) = self.spherical_to_cartesian(mag, theta, phi_new)
        
    def cartesian_to_spherical(self):
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
        return self.mag, self.theta, self.phi
    
    def spherical_to_cartesian(self, mag, theta, phi):
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
        x = mag * math.sin(phi) * math.cos(theta)
        y = mag * math.sin(phi) * math.sin(theta)
        z = mag * math.cos(phi)
        return x, y, z
    
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
        
    def __mul__(self,scalar):
        if not isinstance(scalar, Vector):
            return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
        
    def __rmul__(self,scalar):
        if not isinstance(scalar, Vector):
            return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

if __name__ == "__main__":
    main()