"""
"""
import re
import sys


class Position3d(object):
    X = 0
    Y = 1
    Z = 2
    _dimension = -1

    def __init__(self, _x, _y, _z):
        self._data = [_x, _y, _z]

    @staticmethod
    def set_dimension(dim):
        if dim not in range(3):
            raise ValueError
        Position3d._dimension = dim

    @property
    def data(self):
        try:
            return self._data[Position3d._dimension]
        except IndexError:
            print("Error: Dimension is not set.", file=sys.stderr)
            sys.exit(1)

    @data.setter
    def data(self, x):
        self._data[Position3d._dimension] = x

    def __repr__(self):
        return "<X={}, Y={}, Z={}>".format(
            self._data[self.X], self._data[self.Y], self._data[self.Z])


class Velocity3d(Position3d):
    pass


class Moon(object):
    """
    A moon has two interesting characteristics:
    1. Its position, and
    2. Its velocity.
    And a moon has three operations:
    1. Apply the gravity exerted on it by the other moons (actually, by AN
    other moon),
    2. How to update its position by applying its velocities, and
    3. How to compute its total energy.
    """
    def __init__(self, _x, _y, _z):
        """
        Initialize a new moon.  The initial position coordinates are passed
        in.  The initial velocities are all zero.
        :param _x: The initial X coordinate
        :param _y: The initial Y coordinate
        :param _z: The initial Z coordinate.
        """
        self.position = Position3d(int(_x), int(_y), int(_z))
        self.velocity = Velocity3d(0, 0, 0)

    def cmp_position(self, other):
        """
        Similar to traditional cmp() (or in python __cmp__()) operations.
        specifically compares moons' positions.  Only the current dimension
        is considered.
        :param self: The moon under consideration.
        :param other: The moon
        affecting it.
        :return: -1, 0, or 1 based on comparative positions.
        """
        if self.position.data == other.position.data:
            return 0
        elif self.position.data < other.position.data:
            return 1
        else:
            return -1

    def __eq__(self, other):
        """
        Just a straight test for equality.  Only considers the current
        dimension.
        :param self: The moon under consideration.
        :param other: The moon affecting it.
        :return: True if position and velocity are equal.
        """
        return self.position.data == other.position.data and \
            self.velocity.data == other.velocity.data

    def apply_gravity(self, other):
        """
        Unlike in the real world, gravity calculations only involve one
        dimension at a time. Therefore they can be done completely
        independently.
        :param other: The moon affecting this moon.
        :return: None
        :side effects: self's velocity is updated in this dimension only.
        """
        self.velocity.data += self.cmp_position(other)

    def apply_velocity(self):
        """
        Unlike in the real world, gravity calculations only involve one
        dimension at a time. Therefore they can be done completely
        independently. Apply our velocity to affect our position in one
        dimension.
        :return: None
        :side effect: self's position is updated in one dimension only
        """
        self.position.data += self.velocity.data

    def __repr__(self):
        return "(Pos: {}, Vel: {})".format(self.position, self.velocity)


def initialize_moons():
    """
    The initial positions of the moons.
    :return: A list of 4 moons.
    """
    moons = []
    pat = re.compile(r"<x=(-?\d*), y=(-?\d*), z=(-?\d*)>")
    with open('12 input.txt') as f:
        for n in range(4):
            moon_line = f.readline().strip()
            match = re.match(pat, moon_line)
            moon = Moon(match.group(1), match.group(2), match.group(3))
            moons.append(moon)

    return moons


# The following two are lifted from Beth.  Thanks!
# EUCLID YO
def gcf(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    return a * b // gcf(a, b)


def main():
    """
    All the interesting stuff is in class Moon.
    :return: None
    """
    moons = initialize_moons()

    # Do it again, to get a stable initial set of values to compare against.
    initial_state = initialize_moons()
    needed_cycles = [0] * 3

    # Because in the mechanics of this fake universe gravity and velocity in
    # one dimension do not affect anything in the other two dimensions, we
    # can loop altering one dimension at a time until
    for dimension in (Position3d.X, Position3d.Y, Position3d.Z):
        Position3d.set_dimension(dimension)
        cycled = False
        cycle_count = 0
        while not cycled:
            if cycle_count > 30000000000:
                print("bailing!")
                break
            cycle_count += 1
            for moon in moons:
                for other_moon in moons:
                    if moon is other_moon:
                        continue
                    moon.apply_gravity(other_moon)
            for moon in moons:
                moon.apply_velocity()
            match = True
            for idx, moon in enumerate(moons):
                if moon != initial_state[idx]:
                    # Didn't complete a cycle back to original state for this
                    # dimension. Try again.
                    match = False
                    break
            if match:
                # Yea! Done with this dimension
                needed_cycles[dimension] = cycle_count
                cycled = True

    print(lcm(needed_cycles[2], lcm(needed_cycles[0], needed_cycles[1])),
          "cycles needed to loop.")
    print("Hawking would be proud.")


if __name__ == '__main__':
    main()
