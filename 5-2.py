"""The air conditioner comes online! Its cold air feels good for a while,
but then the TEST alarms start to go off. Since the air conditioner can't
vent its heat anywhere but back into the spacecraft, it's actually making
the air inside the ship warmer.

Instead, you'll need to use the TEST to extend the thermal radiators.
Fortunately, the diagnostic program (your puzzle input) is already equipped
for this. Unfortunately, your Intcode computer is not.

Your computer is only missing a few opcodes:

    Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets
    the instruction pointer to the value from the second parameter.
    Otherwise, it does nothing.

    Opcode 6 is jump-if-false: if the first parameter is zero, it sets the
    instruction pointer to the value from the second parameter. Otherwise,
    it does nothing.

    Opcode 7 is less than: if the first parameter is less than the second
    parameter, it stores 1 in the position given by the third parameter.
    Otherwise, it stores 0.

    Opcode 8 is equals: if the first parameter is equal to the second
    parameter, it stores 1 in the position given by the third parameter.
    Otherwise, it stores 0.

Like all instructions, these instructions need to support parameter modes as
described above.

Normally, after an instruction is finished, the instruction pointer
increases by the number of values in that instruction. However, if the
instruction modifies the instruction pointer, that value is used and the
instruction pointer is not automatically increased.

For example, here are several programs that take one input, compare it to
the value 8, and then produce one output:

    3,9,8,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the
    input is equal to 8; output 1 (if it is) or 0 (if it is not).

    3,9,7,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the
    input is less than 8; output 1 (if it is) or 0 (if it is not).

    3,3,1108,-1,8,3,4,3,99 - Using immediate mode, consider whether the
    input is equal to 8; output 1 (if it is) or 0 (if it is not).

    3,3,1107,-1,8,3,4,3,99 - Using immediate mode, consider whether the
    input is less than 8; output 1 (if it is) or 0 (if it is not).

Here are some jump tests that take an input, then output 0 if the input was
zero or 1 if the input was non-zero:

    3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9 (using position mode)
    3,3,1105,-1,9,1101,0,0,12,4,12,99,1 (using immediate mode)

Here's a larger example:

3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99

The above example program uses an input instruction to ask for a single
number. The program will then output 999 if the input value is below 8,
output 1000 if the input value is equal to 8, or output 1001 if the input
value is greater than 8.

This time, when the TEST diagnostic program runs its input instruction to
get the ID of the system to test, provide it 5, the ID for the ship's
thermal radiator controller. This diagnostic test suite only outputs one
number, the diagnostic code.

What is the diagnostic code for system ID 5?
"""
import sys
import machine_operation_implementations as op
import machine_defs as md


def decode_inst(pc, memory):
    """
    decode a single instruction
    :param pc: the current program counter (location in memory)
    :param memory: the machine's memory
    :return: (param_list, op_function, result_loc, instruction_width)
    """
    opcode = memory[pc]

    def split_opcode(opcode):
        """
        Opcodes in the program may contain information about the mode of the
        parameters, whether they are positional or immediate. As a nested
        function this has access to the opcode definitions.

        :param opcode: The opcode as contained in the program, which may
            contain parameter modes that need to be separated out.
        :return: base_opcode, modes_list
        """
        base_opcode = opcode % 100
        packed_modes = opcode // 100
        modes_list = []
        # Have to use the known length of the operation's parameter list, since
        # the packed_modes value may not have a digit for each parameter.
        # missing digits are mode zero (positional).
        for n in range(len(md.OP_DEFS[base_opcode]['p_locs'])):
            modes_list.append(packed_modes % 10)
            packed_modes = packed_modes // 10

        return base_opcode, modes_list

    # Split the incoming opcode apart, if necessary.
    opcode, param_modes = split_opcode(opcode)

    # Silence PyCharm warning use before def
    op_def = None

    try:
        op_def = md.OP_DEFS[opcode]
    except KeyError:
        # Oops! an invalid opcode. Report the error and halt.
        print("Invalid opcode: {}".format(opcode), file=sys.stderr)
        op.halt([])

    # Get the actual parameters.
    params = []

    for idx, relative_parameter_loc in enumerate(op_def['p_locs']):
        absolute_parameter_loc = memory[relative_parameter_loc + pc]
        param_mode = param_modes[idx]
        if param_mode == md.PARAM_MODE_POSITIONAL:
            params.append(memory[absolute_parameter_loc])
        elif param_mode == md.PARAM_MODE_IMMEDIATE:
            params.append(absolute_parameter_loc)
        else:
            # Oops!  Bad param mode.  Report and halt.
            print("Bad parameter mode encountered: {}. Halting".
                  format(param_mode))
            op.halt([])

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

            # SPECIAL CASE
            # The instructions listed below don't return a value to store.
            if op_function not in (
                op.output,
                op.jump_if_true,
                op.jump_if_false
            ):
                memory[result_loc] = result
        except op.HaltException:
            return

        # Advance the PC
        #
        # SPECIAL CASE
        # The two jump instructions return a new PC if the jump is taken,
        # or None otherwise (in which the PC is incremented as usual by
        # the instruction width
        if op_function in (op.jump_if_true, op.jump_if_false) \
                and result is not None:
            pc = result
        else:
            pc += inst_width


def main():
    with open('5-2 sample input.txt') as f:
        memory = list(map(int, f.readline().split(',')))
    execute(memory)


if __name__ == '__main__':
    main()
