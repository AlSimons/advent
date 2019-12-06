"""
--- Day 5: Sunny with a Chance of Asteroids ---

You're starting to sweat as the ship makes its way toward Mercury. The Elves
suggest that you get the air conditioner working by upgrading your ship
computer to support the Thermal Environment Supervision Terminal.

The Thermal Environment Supervision Terminal (TEST) starts by running a
diagnostic program (your puzzle input). The TEST diagnostic program will run
on your existing Intcode computer after a few modifications:

First, you'll need to add two new instructions:

    Opcode 3 takes a single integer as input and saves it to the position
    given by its only parameter. For example, the instruction 3,50 would
    take an input value and store it at address 50.

    Opcode 4 outputs the value of its only parameter. For example,
    the instruction 4,50 would output the value at address 50.

Programs that use these instructions will come with documentation that
explains what should be connected to the input and output. The program 3,0,
4,0,99 outputs whatever it gets as input, then halts.

Second, you'll need to add support for parameter modes:

Each parameter of an instruction is handled based on its parameter mode.
Right now, your ship computer already understands parameter mode 0, position
mode, which causes the parameter to be interpreted as a position - if the
parameter is 50, its value is the value stored at address 50 in memory.
Until now, all parameters have been in position mode.

Now, your ship computer will also need to handle parameters in mode 1,
immediate mode. In immediate mode, a parameter is interpreted as a value -
if the parameter is 50, its value is simply 50.

Parameter modes are stored in the same value as the instruction's opcode.
The opcode is a two-digit number based only on the ones and tens digit of
the value, that is, the opcode is the rightmost two digits of the first
value in an instruction. Parameter modes are single digits, one per
parameter, read right-to-left from the opcode: the first parameter's mode is
in the hundreds digit, the second parameter's mode is in the thousands
digit, the third parameter's mode is in the ten-thousands digit, and so on.
Any missing modes are 0.

For example, consider the program 1002,4,3,4,33.

The first instruction, 1002,4,3,4, is a multiply instruction - the rightmost
two digits of the first value, 02, indicate opcode 2, multiplication. Then,
going right to left, the parameter modes are 0 (hundreds digit),
1 (thousands digit), and 0 (ten-thousands digit, not present and therefore
zero):

ABCDE
 1002

DE - two-digit opcode,      02 == opcode 2
 C - mode of 1st parameter,  0 == position mode
 B - mode of 2nd parameter,  1 == immediate mode
 A - mode of 3rd parameter,  0 == position mode,
                                  omitted due to being a leading zero

This instruction multiplies its first two parameters. The first parameter,
4 in position mode, works like it did before - its value is the value stored
at address 4 (33). The second parameter, 3 in immediate mode, simply has
value 3. The result of this operation, 33 * 3 = 99, is written according to
the third parameter, 4 in position mode, which also works like it did before
- 99 is written to address 4.

Parameters that an instruction writes to will never be in immediate mode.

Finally, some notes:

    It is important to remember that the instruction pointer should increase
    by the number of values in the instruction after the instruction
    finishes. Because of the new instructions, this amount is no longer
    always 4.

    Integers can be negative: 1101,100,-1,4,0 is a valid program (find 100 +
    -1, store the result in position 4).

The TEST diagnostic program will start by requesting from the user the ID of
the system to test by running an input instruction - provide it 1, the ID
for the ship's air conditioner unit.

It will then perform a series of diagnostic tests confirming that various
parts of the Intcode computer, like parameter modes, function correctly. For
each test, it will run an output instruction indicating how far the result
of the test was from the expected value, where 0 means the test was
successful. Non-zero outputs mean that a function is not working correctly;
check the instructions that were run before the output instruction to see
which one failed.

Finally, the program will output a diagnostic code and immediately halt.
This final output isn't an error; an output followed immediately by a halt
means the program finished. If all outputs were zero except the diagnostic
code, the diagnostic program ran successfully.

After providing 1 to the only input instruction and passing all the tests,
what diagnostic code does the program produce?
"""
import sys

# Define machine characteristics
OP_ADD = 1
OP_MULTIPLY = 2
OP_INPUT = 3
OP_OUTPUT = 4
OP_HALT = 99

PARAM_MODE_INDIRECT = 0
PARAM_MODE_IMMEDIATE = 1


class HaltException (Exception):
    pass

# Implement the instruction operations


def add(params):
    return params[0] + params[1]


def multiply(params):
    return params[0] * params[1]


def input_func(params):
    while True:
        try:
            val = input("A genie gives three wishes, but you only get one. "
                        "Enter an integer: ")
            val = int(val)
            break
        except ValueError:
            print("I said enter an integer.  C'mon.  Try again.")
    return val


def output_func(params):
    # No computation needed.  We're just printing a memory value.
    print("The machine says: {}".format(params[0]))
    return None


def halt(params):
    # We're done.  Blow through the instruction decoder and catch this
    # in the main execute() loop.
    raise HaltException


def decode_inst(pc, memory):
    """
    decode a single instruction
    :param pc: the current program counter (location in memory)
    :param memory: the machine's memory
    :return: (param_list, op_function, result_loc, instruction_width)
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
        },
        OP_INPUT: {
            'p_locs': [],
            'result_loc': 1,
            'op_function': input_func,
            'instruction_width': 2,
        },
        OP_OUTPUT: {
            'p_locs': [1],
            # OP_OUTPUT has no result. Specifying the same location as the
            # p_loc does no harm.
            'result_loc': 1,
            'op_function': output_func,
            'instruction_width': 2,
        }
    }

    opcode = memory[pc]

    def split_opcode(opcode):
        """
        Opcodes in the program may contain information about the mode of the
        parameters, whether they are indirect or immediate. As a nested
        function this has access to the opcode definitions.

        :param opcode: The opcode, which may contain parameter modes that need
            to be separated out.
        :return: base_opcode, modes_list
        """
        base_opcode = opcode % 100
        packed_modes = opcode // 100
        modes_list = []
        # Have to use the known length of the operation's parameter list, since
        # the packed_modes value may not have a digit for each parameter.
        # missing digits are mode zero (relative).
        for n in range(len(op_defs[base_opcode]['p_locs'])):
            modes_list.append(packed_modes % 10)
            packed_modes = packed_modes // 10

        return base_opcode, modes_list

    # Split the incoming opcode apart, if necessary.
    opcode, param_modes = split_opcode(opcode)

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

    for idx, relative_parameter_loc in enumerate(op_def['p_locs']):
        absolute_parameter_loc = memory[relative_parameter_loc + pc]
        param_mode = param_modes[idx]
        if param_mode == PARAM_MODE_INDIRECT:
            params.append(memory[absolute_parameter_loc])
        elif param_mode == PARAM_MODE_IMMEDIATE:
            params.append(absolute_parameter_loc)
        else:
            # Oops!  Bad param mode.  Report and halt.
            print("Bad parameter mode encountered: {}. Halting".
                  format(param_mode))
            halt([])

    result_loc = memory[op_def['result_loc'] + pc]

    return (params,
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
            params, op_function, result_loc, inst_width = \
                decode_inst(pc, memory)

            # We know everything we need to execute the instruction.
            result = op_function(params)
            # The output instruction doesn't return a value to store.
            if result is not None:
                memory[result_loc] = result
        except HaltException:
            return

        # Advance the PC
        pc += inst_width


def main():
    with open('5-1 sample input.txt') as f:
        memory = list(map(int, f.readline().split(',')))
    execute(memory)
    print(memory)


if __name__ == '__main__':
    main()
