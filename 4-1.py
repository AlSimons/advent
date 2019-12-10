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
"""

#
# Is this harder than it seems at first?
# Try a brute force attack.
#

input_range = '356261-846303'
low_str, high_str = input_range.split('-')
low = int(low_str)
high = int(high_str)
count = 0
for n in range(low, high + 1):
    # These tests are easier performing textually, I think.
    trial = str(n)
    found_pair = False
    decreased = False
    for pos in range(len(trial) - 1):
        # Textual comparisons for value work, since we know that they are
        # all numbers.
        # Digits never decrease
        if trial[pos + 1] < trial[pos]:
            # Failure.
            decreased = True
            break
        if trial[pos + 1] == trial[pos]:
            found_pair = True
    if found_pair and not decreased:
        count += 1
print("{} possible combinations".format(count))

# Nope.  Not harder than it seems.
