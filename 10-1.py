"""
--- Day 10: Monitoring Station ---

You fly into the asteroid belt and reach the Ceres monitoring station. The
Elves here have an emergency: they're having trouble tracking all of the
asteroids and can't be sure they're safe.

The Elves would like to build a new monitoring station in a nearby area of
space; they hand you a map of all of the asteroids in that region (your
puzzle input).

The map indicates whether each position is empty (.) or contains an asteroid
(#). The asteroids are much smaller than they appear on the map, and every
asteroid is exactly in the center of its marked position. The asteroids can
be described with X,Y coordinates where X is the distance from the left edge
and Y is the distance from the top edge (so the top-left corner is 0,
0 and the position immediately to its right is 1,0).

Your job is to figure out which asteroid would be the best place to build a
new monitoring station. A monitoring station can detect any asteroid to
which it has direct line of sight - that is, there cannot be another
asteroid exactly between them. This line of sight can be at any angle,
not just lines aligned to the grid or diagonally. The best location is the
asteroid that can detect the largest number of other asteroids.

For example, consider the following map:

.#..#
.....
#####
....#
...##

The best location for a new monitoring station on this map is the
highlighted asteroid at 3,4 because it can detect 8 asteroids, more than any
other location. (The only asteroid it cannot detect is the one at 1,0; its
view of this asteroid is blocked by the asteroid at 2,2.) All other
asteroids are worse locations; they can detect 7 or fewer other asteroids.
Here is the number of other asteroids a monitoring station on each asteroid
could detect:

.7..7
.....
67775
....7
...87

Here is an asteroid (#) and some examples of the ways its line of sight
might be blocked. If there were another asteroid at the location of a
capital letter, the locations marked with the corresponding lowercase letter
would be blocked and could not be detected:

#.........
...A......
...B..a...
.EDCG....a
..F.c.b...
.....c....
..efd.c.gb
.......c..
....f...c.
...e..d..c

Here are some larger examples:

    Best is 5,8 with 33 other asteroids detected:

    ......#.#.
    #..#.#....
    ..#######.
    .#.#.###..
    .#..#.....
    ..#....#.#
    #..#....#.
    .##.#..###
    ##...#..#.
    .#....####

    Best is 1,2 with 35 other asteroids detected:

    #.#...#.#.
    .###....#.
    .#....#...
    ##.#.#.#.#
    ....#.#.#.
    .##..###.#
    ..#...##..
    ..##....##
    ......#...
    .####.###.

    Best is 6,3 with 41 other asteroids detected:

    .#..#..###
    ####.###.#
    ....###.#.
    ..###.##.#
    ##.##.#.#.
    ....###..#
    ..#.#..#.#
    #..#.#.###
    .##...##.#
    .....#.#..

    Best is 11,13 with 210 other asteroids detected:

    .#..##.###...#######
    ##.############..##.
    .#.######.########.#
    .###.#######.####.#.
    #####.##.#.##.###.##
    ..#####..#.#########
    ####################
    #.####....###.#.#.##
    ##.#################
    #####.##.###..####..
    ..######..##.#######
    ####.##.####...##..#
    .#####..#.######.###
    ##...#.##########...
    #.##########.#######
    .####.#.###.###.#.##
    ....##.##.###..#####
    .#.#.###########.###
    #.#.#.#####.####.###
    ###.##.####.##.#..##

Find the best location for a new monitoring station. How many other
asteroids can be detected from that location?
"""
import math  # for atan2()


def get_data(path):
    """
    Get our asteroid data and convert into a list of lists of booleans.
    :param path: Path to a file containing our data
    :return: a list of lists of booleans indicating where asteroids are.
    """

    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line == 'END':
                break

            # Convert asteroid data into lists of True/False
            # True if an asteroid is there.
            bools = []
            for char in line:
                bools.append(char == '#')
            rows.append(bools)
    return rows


def get_bearing(my_y, my_x, other_y, other_x):
    """
    Get the bearing in polar coordinates to the other asteroid.
    :param my_y: my y location on the grid
    :param my_x: my x
    :param other_y: the target's y location on the grid
    :param other_x: the target's x
    :return: a bearing in radians from me to thee
    """
    run = other_x - my_x
    rise = other_y - my_y
    bearing = math.atan2(rise, run)
    return bearing


def scan_skies(data, my_y, my_x):
    """
    Find all the asteroids we can see from the asteroid at (row_n, col_n)
    :param data: The map of asteroids in the sky.
    :param my_y: The row of the asteroid we are on.
    :param my_x: The column of the asteroid we are on.
    :return: The number of asteroids visible from the one we are on.
    """
    # We'll track all the asteroids in the sky in a set.  If there are multiple
    # at the same bearing, we can only see one of them, so we will just dump
    # the bearing (polar coordinates) of each into the set, and then the size
    # of the set will be the count of visible asteroids.
    bag = set()
    for other_y in range(len(data)):
        for other_x in range(len(data[0])):
            if data[other_y][other_x]:
                if (my_x == other_x) and (my_y == other_y):
                    continue
                bag.add(get_bearing(my_y, my_x, other_y, other_x))

    visible = len(bag)
    return visible


def main():
    # Get the data as a list of lists, one per row.
    data = get_data("10 input.txt")
    most_visible = 0
    best = (-1, -1)

    for my_y in range(len(data)):
        for my_x in range(len(data[0])):
            if data[my_y][my_x]:
                # We are on an asteroid.
                # Scan the skies for other asteroids.  We probably can't
                # see them all, but we only care about the ones we can see.
                visible = scan_skies(data, my_y, my_x)
                if visible > most_visible:
                    most_visible = visible
                    best = (my_x, my_y)

    print("Best asteroid for base is {} Visible: {}".format(
        best, most_visible))


if __name__ == "__main__":
    main()
