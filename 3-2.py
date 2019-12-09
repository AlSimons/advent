"""
--- Day 3: Crossed Wires ---

The gravity assist was successful, and you're well on your way to the Venus
refuelling station. During the rush back on Earth, the fuel management
system wasn't completely installed, so that's next on the priority list.

Opening the front panel reveals a jumble of wires. Specifically, two wires
are connected to a central port and extend outward on a grid. You trace the
path each wire takes as it leaves the central port, one wire per line of
text (your puzzle input).

The wires twist and turn, but the two wires occasionally cross paths. To fix
the circuit, you need to find the intersection point closest to the central
port. Because the wires are on a grid, use the Manhattan distance for this
measurement. While the wires do technically cross right at the central port
where they both start, this point does not count, nor does a wire count as
crossing with itself.

For example, if the first wire's path is R8,U5,L5,D3, then starting from the
central port (o), it goes right 8, up 5, left 5, and finally down 3:

...........
...........
...........
....+----+.
....|....|.
....|....|.
....|....|.
.........|.
.o-------+.
...........

Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6,
down 4, and left 4:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........

These wires cross at two locations (marked X), but the lower-left one is
closer to the central port: its distance is 3 + 3 = 6.

Here are a few more examples:

    R75,D30,R83,U83,L12,D49,R71,U7,L72
    U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
    R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
    U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135

What is the Manhattan distance from the central port to the closest
intersection?
"""


class Point(object):
    """
    Simple point class.
    """
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)


class PathSegment(object):
    """
    Records a location and previous location, in order to be able to determine
    the path that was traversed. Translates from, e.g., R6 to a new point in
    X,Y coordinates, and remembers the old location.
    Can detect intersections.
    """
    def __init__(self, prev_location, path):
        """
        Determines new location and remembers the previous location.
        :param prev_location: The previous Location.
        :param path: The path traversed this move, in the form Lx, Rx, Ux, Dx.
        """
        if prev_location is None:
            # This is true for the first point in the path. Its prev location
            # is (0,0).
            self.prev_location = Point(0, 0)
        else:
            self.prev_location = prev_location.location
        direction = path[0]
        distance = int(path[1:])
        if direction in ('D', 'L'):
            distance = -distance
        if direction in ('L', 'R'):
            new_x = self.prev_location.x + distance
            new_y = self.prev_location.y
        else:
            new_x = self.prev_location.x
            new_y = self.prev_location.y + distance
        self.location = Point(new_x, new_y)

    def is_vertical(self):
        return self.location.x == self.prev_location.x

    def intersects(self, other):
        """
        Determines whether two path segments intersect, and if so at
        what Point. Two segments intersect if the end points span tht others.
        An example is a better description.  Let's arbitratily call the
        X and Y coordinates of the prev_location "left" and "bottom", and the
        coordinates of the current location "right" and "top". Either one or
        the other will be true:
            - If the path segment direction was U or D (vertical), the two X
              values (left and right) will be the same, or
            - If the direction was L or R (horizontal), the two Y values (top
              and bottom) will be the same.
        If both are vertical or both horizontal, then there is no intersection.
        Otherwise, if the changing X or Y value spans the other's fixed value
        when comparing self to other and other to self, then there is an
        intersection.
        :param other: The other path segment that this one may intersect.
        :return: (boolean, Point) Boolean is True if there is an intersection.
                 Point is only valid is boolean is True.
        """
        # Use XOR to see if they are both vertical or horizontal.
        # Will evaluate to False if they are parallel, so we negate the value.
        if not (self.is_vertical() ^ other.is_vertical()):
            # They are the same direction,
            return False, Point(0, 0)

        # There is a possibility of a collision since they are perpendicular
        # Get self's values in the changing dimension and its constant value in
        # the other.  Do the same for other.

        # Get easier access to type
        my_x = self.location.x
        my_prev_x = self.prev_location.x
        my_y = self.location.y
        my_prev_y = self.prev_location.y

        # Figure out "my" needed values
        if self.is_vertical():
            # X is fixed, Y is changing
            my_fixed = my_x
            my_lesser = my_y
            my_greater = my_prev_y

        else:
            # Y is fixed, X is changing
            my_fixed = my_y
            my_lesser = my_x
            my_greater = my_prev_x

        # Those may be backwards!
        if my_lesser > my_greater:
            my_lesser, my_greater = my_greater, my_lesser

        # Now the same for other.  Refer to the comments above.
        # Get easier access to type
        other_x = other.location.x
        other_prev_x = other.prev_location.x
        other_y = other.location.y
        other_prev_y = other.prev_location.y

        if other.is_vertical():
            # X is fixed, Y is changing
            other_fixed = other_x
            other_lesser = other_y
            other_greater = other_prev_y

        else:
            other_fixed = other_y
            other_lesser = other_x
            other_greater = other_prev_x

        if other_lesser > other_greater:
            other_lesser, other_greater = other_greater, other_lesser

        # FINALLY!  We can tell if there is an intersection.
        if (other_lesser > my_fixed) or (my_fixed > other_greater):
            # No possibility of an intersection
            return False, Point(0, 0)
        if (my_lesser > other_fixed) or (other_fixed > my_greater):
            return False, Point(0, 0)

        # OK, there is an intersection, at the two fixed coordinates
        if self.is_vertical():
            # My x coordinate is fixed
            return True, Point(my_fixed, other_fixed)
        else:
            # My y coordinate is fixed.
            return True, Point(other_fixed, my_fixed)

    def __repr__(self):
        return "Loc {}, Prev loc {}".format(self.location, self.prev_location)


def main():
    """

    :return:
    """
    first_path = []
    second_path = []
    with open('3-1 sample input.txt') as f:
        for path in (first_path, second_path):
            path_line = f.readline()
            for segment in path_line.split(','):
                if not path:
                    # Our first time; there is no previous path segment
                    prev = None
                else:
                    prev = path[-1]
                path.append(PathSegment(prev, segment))

    # Now we have two complete paths.  Time to check for intersections.
    # Currently O(N^2). Could figure out some sorting mechanism and maybe
    # get more efficient.  But not now.
    shortest = 999999999999999

    for segment_1 in first_path:
        for segment_2 in second_path:
            does_intersect, location = segment_1.intersects(segment_2)
            if does_intersect:
                print("Seg_1", segment_1)
                print("Seg_2", segment_2)
                print("Location", location)
                possible = location.x + location.y
                # A distance of 0 happens at the very beginning, at the origin.
                if possible < shortest and possible > 0:
                    shortest = possible

    # If I've done everything right, we can now print out the shortest
    # Manhattan distance, and move on to the next problem!
    print("The shortest Manhattan distance is {}".format(shortest))

    # That's all, folks!


if __name__ == '__main__':
    main()
