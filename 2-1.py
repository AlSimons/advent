"""
--- Day 2: 1202 Program Alarm ---

On the way to your gravity assist around the Moon, your ship computer beeps
angrily about a "1202 program alarm". On the radio, an Elf is already
explaining how to handle the situation: "Don't worry, that's perfectly
norma--" The ship computer bursts into flames.

You notify the Elves that the computer's magic smoke seems to have escaped.
"That computer ran Intcode programs like the gravity assist program it was
working on; surely there are enough spare parts up there to build a new
Intcode computer!"

An Intcode program is a list of integers separated by commas (like 1,0,0,3,
99). To run one, start by looking at the first integer (called position 0).
Here, you will find an opcode - either 1, 2, or 99. The opcode indicates
what to do; for example, 99 means that the program is finished and should
immediately halt. Encountering an unknown opcode means something went wrong.

Opcode 1 adds together numbers read from two positions and stores the result
in a third position. The three integers immediately after the opcode tell
you these three positions - the first two indicate the positions from which
you should read the input values, and the third indicates the position at
which the output should be stored.

For example, if your Intcode computer encounters 1,10,20,30, it should read
the values at positions 10 and 20, add those values, and then overwrite the
value at position 30 with their sum.

Opcode 2 works exactly like opcode 1, except it multiplies the two inputs
instead of adding them. Again, the three integers after the opcode indicate
where the inputs and outputs are, not their values.

Once you're done processing an opcode, move to the next one by stepping
forward 4 positions.

For example, suppose you have the following program:

1,9,10,3,2,3,11,0,99,30,40,50

For the purposes of illustration, here is the same program split into
multiple lines:

1,9,10,3,
2,3,11,0,
99,
30,40,50

The first four integers, 1,9,10,3, are at positions 0, 1, 2, and 3.
Together, they represent the first opcode (1, addition), the positions of
the two inputs (9 and 10), and the position of the output (3). To handle
this opcode, you first need to get the values at the input positions:
position 9 contains 30, and position 10 contains 40. Add these numbers
together to get 70. Then, store this value at the output position; here,
the output position (3) is at position 3, so it overwrites itself.
Afterward, the program looks like this:

1,9,10,70,
2,3,11,0,
99,
30,40,50

Step forward 4 positions to reach the next opcode, 2. This opcode works just
like the previous, but it multiplies instead of adding. The inputs are at
positions 3 and 11; these positions contain 70 and 50 respectively.
Multiplying these produces 3500; this is stored at position 0:

3500,9,10,70,
2,3,11,0,
99,
30,40,50

Stepping forward 4 more positions arrives at opcode 99, halting the program.

Here are the initial and final states of a few more small programs:

    1,0,0,0,99 becomes 2,0,0,0,99 (1 + 1 = 2).
    2,3,0,3,99 becomes 2,3,0,6,99 (3 * 2 = 6).
    2,4,4,5,99,0 becomes 2,4,4,5,99,9801 (99 * 99 = 9801).
    1,1,1,4,99,5,6,0,99 becomes 30,1,1,4,2,5,6,0,99.

Once you have a working computer, the first step is to restore the gravity
assist program (your puzzle input) to the "1202 program alarm" state it had
just before the last computer caught fire. To do this, before running the
program, replace position 1 with the value 12 and replace position 2 with
the value 2. What value is left at position 0 after the program halts?
"""
import sys

# Define machine characteristics
OP_ADD = 1
OP_MULTIPLY = 2
OP_HALT = 99


class HaltException (Exception):
    pass

# Implement the instruction operations


def add(params):
    return params[0] + params[1]


def multiply(params):
    return params[0] * params[1]


def halt(params):
    # We're done.  Blow through the instruction decoder and catch this
    # in the main execute() loop.
    raise HaltException


def decode_inst(pc, memory):
    """
    decode a single instruction
    :param pc: the current program counter (location in memory)
    :param memory: the machine's memory
    :return: (op, param_list, op_function, result_loc, instruction_width)
    """
    #
    # Describe each operation a dict keyed by opcode, of dicts:
    #   {opcode: {
    #       p_locs: [],
    #       result_loc:,
    #       op_function:,
    #       instruction_width:,
    #       },
    #   }
    #
    op_defs = {
        OP_ADD: {
            'p_locs': [1, 2],
            'result_loc': 3,
            'op_function': add,
            'instruction_width': 4,
        },
        OP_MULTIPLY: {
            'p_locs': [1, 2],
            'result_loc': 3,
            'op_function': multiply,
            'instruction_width': 4,
        },
        OP_HALT: {
            'p_locs': [],
            # Lie about the halt instruction's result location. It has no
            # result, so it would seem that putting None here would be better.
            # But that would require special case code below when we make
            # the result location be relative to the pc because you can't add
            # the pc to None.  The halt operation raises an exception, so
            # the result location is never used.
            'result_loc': 0,
            'op_function': halt,
            'instruction_width': 1,
        }
    }

    opcode = memory[pc]

    # Silence PyCharm warning use before def
    op_def = None

    try:
        op_def = op_defs[opcode]
    except KeyError:
        # Oops! an invalid opcode. Report the error and halt.
        print("Invalid opcode: {}".format(opcode), file=sys.stderr)
        halt([])

    # Get the actual parameters (NB, sneak peek: This section will need
    # to be changed in day 5's exercise.
    params = []
    for relative_parameter_loc in op_def['p_locs']:
        absolute_parameter_loc = memory[relative_parameter_loc + pc]
        params.append(memory[absolute_parameter_loc])

    result_loc = memory[op_def['result_loc'] + pc]

    # At least at this stage, opcode isn't necessary to return,
    # we'll leave it for now-- may rip it out downstream.

    #DEBUG
    print("Instruction: {}".format(memory[pc:pc + 4]))

    print("  PC: {}, Op: {}, locs: {}, vals: {} Rl: {}".format(
        pc, opcode, op_def['p_locs'], params, result_loc
    ))
    return (opcode,
            params,
            op_def['op_function'],
            result_loc,
            op_def['instruction_width'],
            )


def execute(memory):
    """
    Loop over the instructions until we get a halt.
    :param memory: The memory of our machine implemented as a list.
    :return: None
    """
    pc = 0

    while True:
        try:
            opcode, params, op_function, result_loc, inst_width = \
                decode_inst(pc, memory)

            # We know everything we need to execute the instruction.
            result = op_function(params)
            print("    Result: {} stored at {}".format(result, result_loc))
            memory[result_loc] = result
            #  memory[result_loc] = op_function(params)
        except HaltException:
            return

        # Advance the PC
        pc += inst_width


def main():
    with open('2-1 sample input.txt') as f:
        memory = list(map(int, f.readline().split(',')))
    execute(memory)
    print(memory)


if __name__ == '__main__':
    main()
