"""
--- Part Two ---

During the second Go / No Go poll, the Elf in charge of the Rocket Equation
Double-Checker stops the launch sequence. Apparently, you forgot to include
additional fuel for the fuel you just added.

Fuel itself requires fuel just like a module - take its mass, divide by
three, round down, and subtract 2. However, that fuel also requires fuel,
and that fuel requires fuel, and so on. Any mass that would require negative
fuel should instead be treated as if it requires zero fuel; the remaining
mass, if any, is instead handled by wishing really hard, which has no mass
and is outside the scope of this calculation.

So, for each module mass, calculate its fuel and add it to the total. Then,
treat the fuel amount you just calculated as the input mass and repeat the
process, continuing until a fuel requirement is zero or negative. For example:

    A module of mass 14 requires 2 fuel. This fuel requires no further fuel
    (2 divided by 3 and rounded down is 0, which would call for a negative
    fuel), so the total fuel required is still just 2.
    At first, a module of mass 1969 requires 654 fuel. Then, this fuel
    requires 216 more fuel (654 / 3 - 2). 216 then requires 70 more fuel,
    which requires 21 fuel, which requires 5 fuel, which requires no
    further fuel. So, the total fuel required for a module of mass 1969 is
    654 + 216 + 70 + 21 + 5 = 966.
    The fuel required by a module of mass 100756 and its fuel is: 33583 +
    11192 + 3728 + 1240 + 411 + 135 + 43 + 12 + 2 = 50346.

What is the sum of the fuel requirements for all of the modules on your
spacecraft when also taking into account the mass of the added fuel?
(Calculate the fuel requirements for each module separately, then add them
all up at the end.)
"""


def fuel_for_module(module_mass):
    """
    Compute the fuel needed for a module of a given mass according to the
    formula given in the introductory description: mass / 3 - 2. Use iteration
    instead of recursion; it is faster and not subject to blowing the stack.
    :param module_mass: The mass of the module without fuel.
    :return: The needed amount of fuel for the module, accounting for the
        additional mass of the fuel.
    """
    total_fuel_needed = 0

    # Initialize the additional (fuel) mass to the incoming module mass.
    additional_mass = module_mass

    # Loop until the additional mass we require is <= 0.
    while True:
        additional_mass = (additional_mass // 3) - 2
        if additional_mass <= 0:
            return total_fuel_needed
        total_fuel_needed += additional_mass


def main():
    fuel_required = 0
    with open('1-1 sample input.txt') as f:
        for mass in f.readlines():
            mass = int(mass.strip())
            fuel_required += fuel_for_module(mass)
    print("{} units of fuel required".format(fuel_required))


if __name__ == '__main__':
    main()
