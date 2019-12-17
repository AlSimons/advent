"""
Once you give them the coordinates, the Elves quickly deploy an Instant
Monitoring Station to the location and discover the worst: there are simply
too many asteroids.

The only solution is complete vaporization by giant laser.

Fortunately, in addition to an asteroid scanner, the new monitoring station
also comes equipped with a giant rotating laser perfect for vaporizing
asteroids. The laser starts by pointing up and always rotates clockwise,
vaporizing any asteroid it hits.

If multiple asteroids are exactly in line with the station, the laser only
has enough power to vaporize one of them before continuing its rotation. In
other words, the same asteroids that can be detected can be vaporized,
but if vaporizing one asteroid makes another one detectable,
the newly-detected asteroid won't be vaporized until the laser has returned
to the same position by rotating a full 360 degrees.

For example, consider the following map, where the asteroid with the new
monitoring station (and laser) is marked X:

.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....X...###..
..#.#.....#....##   (Al: Laser at 8, 3)

The first nine asteroids to get vaporized, in order, would be:

.#....###24...#..
##...##.13#67..9#
##...#...5.8####.
..#.....X...###..
..#.#.....#....##

Note that some asteroids (the ones behind the asteroids marked 1, 5, and 7)
won't have a chance to be vaporized until the next full rotation. The laser
continues rotating; the next nine to be vaporized are:

.#....###.....#..
##...##...#.....#
##...#......1234.
..#.....X...5##..
..#.9.....8....76

The next nine to be vaporized are then:

.8....###.....#..
56...9#...#.....#
34...7...........
..2.....X....##..
..1..............

Finally, the laser completes its first full rotation (1 through 3), a second
rotation (4 through 8), and vaporizes the last asteroid (9) partway through
its third rotation:

......234.....6..
......1...5.....7
.................
........X....89..
.................

In the large example above (the one with the best monitoring station
location at 11,13):

    The 1st asteroid to be vaporized is at 11,12.
    The 2nd asteroid to be vaporized is at 12,1.
    The 3rd asteroid to be vaporized is at 12,2.
    The 10th asteroid to be vaporized is at 12,8.
    The 20th asteroid to be vaporized is at 16,0.
    The 50th asteroid to be vaporized is at 16,9.
    The 100th asteroid to be vaporized is at 10,16.
    The 199th asteroid to be vaporized is at 9,6.
    The 200th asteroid to be vaporized is at 8,2.
    The 201st asteroid to be vaporized is at 10,9.
    The 299th and final asteroid to be vaporized is at 11,1.

The Elves are placing bets on which will be the 200th asteroid to be
vaporized. Win the bet by determining which asteroid that will be; what do
you get if you multiply its X coordinate by 100 and then add its Y
coordinate? (For example, 8,2 becomes 802.) """
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
            # Get rid of blank lines
            if not line:
                continue
            if line == 'END':
                break

            # Convert asteroid data into lists of True/False
            # True if an asteroid is there.
            bools = []
            for char in line:
                bools.append(char == '#')
            rows.append(bools)
    return rows


def order_bearings(bearings):
    """
    Polar coordinates have zero at the positive X axis (in rectangular coords).
    The problem presented here wants the "laser" (just consider those
    to be air quotes) to start out "up," i.e., at pi/2 radians in polar
    coords.  So we have to sort the bearings, to put them in order as
    follows:
        1. pi/2 decreasing to -pi (in compass terms, 0 deg to 270 deg)
        2. pi decreasing to pi/2 (270 deg to 360 deg)
    :param bearings: a list of bearings in radians.
    :return: a sorted list of bearings in radians, where bearings after 1.5pi
    radians are at the head of the list.
    """
    # Silence bogus PyCharm warnings. Sigh.
    n = None

    # First sort the list, descending.
    bearings.sort(reverse=True)

    # Now find the first element at or below pi/2 radians.
    for n in range(len(bearings)):
        if bearings[n] <= math.pi/2:
            break

    # The list items before here need to be moved to the end.
    new_list = bearings[n:] + bearings[:n]
    return new_list


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
    # Y increases going DOWN, not up as in normal cartesian coords.
    rise = my_y - other_y
    bearing = math.atan2(rise, run)
    return bearing


def get_distance(my_y, my_x, other_y, other_x):
    """
    Thank you, Pythagoras.
    :param my_y: My location's Y coordinate
    :param my_x: My location's X coordinate
    :param other_y: Other Asteroid's Y coordinate
    :param other_x: Other Asteroid's Y coordinate
    :return: The distance to the other asteroid
    """
    a = ((other_y - my_y) ** 2) + ((other_x - my_x) ** 2)
    return math.sqrt(a)


def scan_skies(data, my_y, my_x):
    """
    Find all the asteroids and record their bearings and distances from us.
    :param data: The map of asteroids in the sky.
    :param my_y: The row of the asteroid we are on.
    :param my_x: The column of the asteroid we are on.
    :return: The number of asteroids visible from the one we are on.
    """
    # We'll track all the asteroids in the sky in a dict. The keys will be the
    # bearings, and the values will be lists of collections / tuples,
    # (distance, x, y). As we enter them, the distances will be in an
    # arbitrary order.  We'll sort them just before returning.
    all_asteroids = {}
    for other_y in range(len(data)):
        for other_x in range(len(data[0])):
            if data[other_y][other_x]:
                if (my_x == other_x) and (my_y == other_y):
                    continue
                bearing = get_bearing(my_y, my_x, other_y, other_x)
                distance = get_distance(my_y, my_x, other_y, other_x)

                if bearing not in all_asteroids:
                    all_asteroids[bearing] = []
                all_asteroids[bearing].append((distance, other_x, other_y))

    # Now sort all the distance lists.
    for bearing in all_asteroids:
        # Sort on the distance element of the tuple
        all_asteroids[bearing].sort(key=lambda x: x[0])

    return all_asteroids


def main():
    # Get the data as a list of lists, one per row.
    data = get_data("10 input.txt")

    # Test coords for the "large" example shown in the 10-1 intro:
    # my_x = 11
    # my_y = 13

    # From program 10-1, we know that the best asteroid is at (27, 19)
    # Real data coords
    my_x = 27
    my_y = 19

    if not data[my_y][my_x]:
        raise ValueError("Huh? We;re not on an asteroid!")

    all_asteroids = scan_skies(data, my_y, my_x)

    bearings = order_bearings(list(all_asteroids.keys()))

    # We need to know which is the 200th asteroid blasted to smithereens.
    count = 1
    index = 0
    # We will delete elements from all_asteroids as we blast the last asteroid
    # on a bearing, so we can loop until it is done. Could equally well loop on
    # bearings.
    while all_asteroids:
        try:
            bearing = bearings[index]
            asteroids = all_asteroids[bearing]
            asteroid = asteroids.pop(0)
            if not asteroids:
                bearings.remove(bearing)
                # We've removed the entry at index, moving all the remaining
                # up. So we need to adjust index to account for the removed
                # entry.
                index -= 1

                # And clean up all_asteroids
                del(all_asteroids[bearing])
            if count == 200:
                print("The two hundredth asteroid was ({}, {})".format(
                    asteroid[1], asteroid[2]
                ))
            index += 1
            count += 1
        except IndexError:
            # Because the length of bearings is constantly changing, we simply
            # keep walking through it until we fall off the end, and then
            # reset the index to 0.
            index = 0


if __name__ == "__main__":
    main()
