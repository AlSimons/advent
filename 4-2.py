"""
--- Day 4: Secure Container ---

You arrive at the Venus fuel depot only to discover it's protected by a
password. The Elves had written the password on a sticky note, but someone
threw it out.

However, they do remember a few key facts about the password:

    It is a six-digit number.
    The value is within the range given in your puzzle input.
    Two adjacent digits are the same (like 22 in 122345).
    Going from left to right, the digits never decrease; they only ever
    increase or stay the same (like 111123 or 135679).

Other than the range rule, the following are true:

    111111 meets these criteria (double 11, never decreases).
    223450 does not meet these criteria (decreasing pair of digits 50).
    123789 does not meet these criteria (no double).

How many different passwords within the range given in your puzzle input meet
these criteria?

--- Part Two ---

An Elf just remembered one more important detail: the two adjacent matching
digits are not part of a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule,
the following are now true:

    112233 meets these criteria because the digits never decrease and all
    repeated digits are exactly two digits long.

    123444 no longer meets the criteria (the repeated 44 is part of a larger
    group of 444).

    111122 meets the criteria (even though 1 is repeated more than twice,
    it still contains a double 22).

How many different passwords within the range given in your puzzle input meet
all of the criteria?

Your puzzle input is still 356261-846303.
"""


def check_combo_criteria(combo):
    """
    Check the criteria.
    1. Six digits long (known because of the input range given, but what the
       heck.
    2. Digits never decrease going left to right.
    3. Must contain at least one pair of digits, but that pair must not be
       part of a larger grouping of digits.
    :param combo: the combination to check.
    :return: Boolean True if the combo meets the criteria.
    """
    # These tests are easier performing textually, I think.
    trial = str(combo)

    # 1. The combo must be six digits long.
    if len(trial) != 6:
        return False

    large_group = False
    found_pair = False
    in_group = False
    decreased = False
    for pos in range(len(trial) - 1):
        # Textual comparisons for value work, since we know that they are
        # all numbers.

        # 2. Digits never decrease
        if trial[pos + 1] < trial[pos]:
            # Failure.
            decreased = True
            break

        # 3. Most have a pair that is not part of a larger grouping.
        if trial[pos + 1] == trial[pos]:
            # We've found a repeat.  May be a pair, may be part of a larger
            # group.
            if in_group:
                # We've found at least a third repeated character.
                # Can't break here, because there may be a pair later in the
                # combo
                large_group = True
            in_group = True
        else:
            # No match, no longer in a pair
            if large_group:
                # The set of repeats we just left doesn't count; more than two.
                large_group = False
            elif in_group:
                # We had a pair, but not a large group.  We've found a pair.
                found_pair = True
            in_group = False
    #
    # Were we in a pair at the end of the string?
    if in_group and not large_group:
        found_pair = True
    return found_pair and not decreased


def main():
    input_range = '356261-846303'
    low_str, high_str = input_range.split('-')
    low = int(low_str)
    high = int(high_str)
    count = 0
    for combo_candidate in range(low, high + 1):
        if check_combo_criteria(combo_candidate):
            count += 1
    print("{} possible combinations".format(count))


if __name__ == '__main__':
    main()
