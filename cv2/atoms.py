import playground
import random

from typing import List, Tuple, NewType

Pos = NewType('Pos', Tuple[int, int])


class Atom:

    def __init__(self, pos: Pos, vel: Pos, rad: int, col: str):
        """
        Initializer of Atom class

        :param x: x-coordinate
        :param y: y-coordinate
        :param rad: radius
        :param color: color of displayed circle
        """
        self.posx = pos[0]
        self.posy = pos[1]
        self.vel = vel
        self.rad = rad
        self.color = col

    def to_tuple(self) -> Tuple[int, int, int, str]:
        """
        Returns tuple representing an atom.

        Example: pos = (10, 12,), rad = 15, color = 'green' -> (10, 12, 15, 'green')
        """
        res = (self.posx, self.posy, self.rad, self.color)
        return res
    def apply_speed(self, size_x: int, size_y: int):
        """
        Applies velocity `vel` to atom's position `pos`.

        :param size_x: width of the world space
        :param size_y: height of the world space
        """
        self.posx += self.vel[0]
        self.posy += self.vel[1]

        if self.posx < 0 + self.rad or self.posx > size_x - self.rad:
            self.vel = (-self.vel[0], self.vel[1])
        if self.posy < 0 + self.rad or self.posy > size_y - self.rad:
            self.vel = (self.vel[0], -self.vel[1])


class FallDownAtom(Atom):
    """
    Class to represent atoms that are pulled by gravity.
     
    Set gravity factor to ~3.

    Each time an atom hits the 'ground' damp the velocity's y-coordinate by ~0.7.
    """
    def __init__(self, pos, vel, rad, col):
        super().__init__(pos, vel, rad, col)
        self.g = 3.0
        self.damping = 0.7

    def apply_speed(self, size_x: int, size_y: int):
        self.posx += self.vel[0]
        self.posy += self.vel[1]

        if self.posx < 0 + self.rad or self.posx > size_x - self.rad:
            self.vel = (-self.vel[0], self.vel[1])
            
        if self.posy < 0 + self.rad:
            self.vel = (self.vel[0], -self.vel[1])
    
        if self.posy > size_y - self.rad:
            self.vel = (self.vel[0], -self.vel[1] * self.damping)
            self.posy = size_y - self.rad
        else:
            self.vel = (self.vel[0], self.vel[1] + self.g)


class ExampleWorld:

    def __init__(self, size_x: int, size_y: int, no_atoms: int, no_falldown_atoms: int):
        """
        ExampleWorld initializer.

        :param size_x: width of the world space
        :param size_y: height of the world space
        :param no_atoms: number of 'bouncing' atoms
        :param no_falldown_atoms: number of atoms that respect gravity
        """

        self.width = size_x
        self.height = size_y
        self.no_atoms = no_atoms
        self.no_falldown_atoms = no_falldown_atoms
        self.atoms = []

    def generate_atoms(self, no_atoms: int, no_falldown_atoms) -> List[Atom|FallDownAtom]:
        """
        Generates `no_atoms` Atom instances using `random_atom` method.
        Returns list of such atom instances.

        :param no_atoms: number of Atom instances
        :param no_falldown_atoms: numbed of FallDownAtom instances
        """
        for i in range(no_atoms):
            self.atoms.append(self.random_atom())
        for i in range(no_falldown_atoms):
            self.atoms.append(self.random_falldown_atom())
        return self.atoms

    def random_atom(self) -> Atom:
        """
        Generates one Atom instance at random position in world, with random velocity, random radius
        and 'green' color.
        """
        rad = random.randint(5, 30)
        posx = random.randint(0 + rad, self.width - rad)
        posy = random.randint(0 + rad, self.height - rad)
        vel = (random.randint(5, 10), random.randint(5, 10))
        color = 'green'
        return Atom((posx, posy), vel, rad, color)
    
    def random_falldown_atom(self):
        """
        Generates one FalldownAtom instance at random position in world, with random velocity, random radius
        and 'yellow' color.
        """
        rad = random.randint(5, 30)
        posx = random.randint(0 + rad, self.width - rad)
        posy = random.randint(0 + rad, self.height - rad)
        vel = (random.randint(5, 10), random.randint(5, 10))
        color = 'yellow'
        return FallDownAtom((posx, posy), vel, rad, color)

    def add_atom(self, pos_x, pos_y):
        """
        Adds a new Atom instance to the list of atoms. The atom is placed at the point of left mouse click.
        Velocity and radius is random.

        :param pos_x: x-coordinate of a new Atom
        :param pos_y: y-coordinate of a new Atom

        Method is called by playground on left mouse click.
        """

        pass

    def add_falldown_atom(self, pos_x, pos_y):
        """
        Adds a new FallDownAtom instance to the list of atoms. The atom is placed at the point of right mouse click.
        Velocity and radius is random.

        Method is called by playground on right mouse click.

        :param pos_x: x-coordinate of a new FallDownAtom
        :param pos_y: y-coordinate of a new FallDownAtom
        """

        pass

    def tick(self):
        """
        Method is called by playground. Sends a tuple of atoms to rendering engine.

        :return: tuple or generator of atom objects, each containing (x, y, radius, color) attributes of atom 
        """
        res = []
        for atom in self.atoms:
            atom.apply_speed(self.width, self.height)
            res.append(atom.to_tuple())
        return tuple(res)


if __name__ == '__main__':
    size_x, size_y = 700, 400
    no_atoms = 2
    no_falldown_atoms = 3

    world = ExampleWorld(size_x, size_y, no_atoms, no_falldown_atoms)
    world.generate_atoms(no_atoms, no_falldown_atoms)

    playground.run((size_x, size_y), world)