"""
"Good, the new computer seems to be working correctly! Keep it nearby during
this mission - you'll probably use it again. Real Intcode computers support
many more features than your new one, but we'll let you know what they are
as you need them."

"However, your current priority should be to complete your gravity assist
around the Moon. For this mission to succeed, we should settle on some
terminology for the parts you've already built."

Intcode programs are given as a list of integers; these values are used as
the initial state for the computer's memory. When you run an Intcode
program, make sure to start by initializing memory to the program's values.
A position in memory is called an address (for example, the first value in
memory is at "address 0").

Opcodes (like 1, 2, or 99) mark the beginning of an instruction. The values
used immediately after an opcode, if any, are called the instruction's
parameters. For example, in the instruction 1,2,3,4, 1 is the opcode; 2, 3,
and 4 are the parameters. The instruction 99 contains only an opcode and has
no parameters.

The address of the current instruction is called the instruction pointer; it
starts at 0. After an instruction finishes, the instruction pointer
increases by the number of values in the instruction; until you add more
instructions to the computer, this is always 4 (1 opcode + 3 parameters) for
the add and multiply instructions. (The halt instruction would increase the
instruction pointer by 1, but it halts the program instead.)

"With terminology out of the way, we're ready to proceed. To complete the
gravity assist, you need to determine what pair of inputs produces the
output 19690720."

The inputs should still be provided to the program by replacing the values
at addresses 1 and 2, just like before. In this program, the value placed in
address 1 is called the noun, and the value placed in address 2 is called
the verb. Each of the two input values will be between 0 and 99, inclusive.

Once the program has halted, its output is available at address 0, also just
like before. Each time you try a pair of inputs, make sure you first reset
the computer's memory to the values in the program (your puzzle input) - in
other words, don't reuse memory from a previous attempt.

Find the input noun and verb that cause the program to produce the output
19690720. What is 100 * noun + verb? (For example, if noun=12 and verb=2,
the answer would be 1202.)
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
            memory[result_loc] = result
            #  memory[result_loc] = op_function(params)
        except HaltException:
            return

        # Advance the PC
        pc += inst_width


def main():
    for noun in range(100):
        for verb in range(100):
            with open('2-1 sample input.txt') as f:
                memory = list(map(int, f.readline().split(',')))
            memory[1] = noun
            memory[2] = verb
            execute(memory)
            if memory[0] == 19690720:
                # We're done.
                print("Noun: {}, Verb: {}".format(noun, verb))
                print("Combined as requested: {}".format(noun * 100 + verb))
                sys.exit()
    print("No such values were found")


if __name__ == '__main__':
    main()
