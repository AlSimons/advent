"""
--- Day 9: Sensor Boost ---

You've just said goodbye to the rebooted rover and left Mars when you
receive a faint distress signal coming from the asteroid belt. It must be
the Ceres monitoring station!

In order to lock on to the signal, you'll need to boost your sensors. The
Elves send up the latest BOOST program - Basic Operation Of System Test.

While BOOST (your puzzle input) is capable of boosting your sensors,
for tenuous safety reasons, it refuses to do so until the computer it runs
on passes some checks to demonstrate it is a complete Intcode computer.

Your existing Intcode computer is missing one key feature: it needs support
for parameters in relative mode.

Parameters in mode 2, relative mode, behave very similarly to parameters in
position mode: the parameter is interpreted as a position. Like position
mode, parameters in relative mode can be read from or written to.

The important difference is that relative mode parameters don't count from
address 0. Instead, they count from a value called the relative base. The
relative base starts at 0.

The address a relative mode parameter refers to is itself plus the current
relative base. When the relative base is 0, relative mode parameters and
position mode parameters with the same value refer to the same address.

For example, given a relative base of 50, a relative mode parameter of -7
refers to memory address 50 + -7 = 43.

The relative base is modified with the relative base offset instruction:

    Opcode 9 adjusts the relative base by the value of its only parameter.
    The relative base increases (or decreases, if the value is negative) by
    the value of the parameter.

For example, if the relative base is 2000, then after the instruction 109,
19, the relative base would be 2019. If the next instruction were 204,-34,
then the value at address 1985 would be output.

Your Intcode computer will also need a few other capabilities:

    The computer's available memory should be much larger than the initial
    program. Memory beyond the initial program starts with the value 0 and
    can be read or written like any other memory. (It is invalid to try to
    access memory at a negative address, though.)

    The computer should have support for large numbers. Some instructions
    near the beginning of the BOOST program will verify this capability.

Here are some example programs that use these features:

    109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99 takes no input
    and produces a copy of itself as output.

    1102,34915192,34915192,7,4,7,99,0 should output a 16-digit number.

    104,1125899906842624,99 should output the large number in the middle.

The BOOST program will ask for a single input; run it in test mode by
providing it the value 1. It will perform a series of checks on each opcode,
output any opcodes (and the associated parameter modes) that seem to be
functioning incorrectly, and finally output a BOOST keycode.

Once your Intcode computer is fully functional, the BOOST program should
report no malfunctioning opcodes when run in test mode; it should only
output a single value, the BOOST keycode. What BOOST keycode does it produce?
"""
import sys
import machine_operation_implementations as op
import machine_defs as md


def get_virtual_memory(memory, needed_size):
    """
    If memory is smaller than an index requires, extend the memory list.
    This is expensive, so we'll get an additional 25%.
    :param memory: The current memory list.
    :param needed_size: the size that we need
    :return: a new list for use as memory
    """
    curr_len = len(memory)
    allocation = int(needed_size * 1.25)
    additional_needed = allocation - curr_len
    new_memory = memory + [0] * additional_needed
    print("Extended memory. Original size {}, new {}".format(
        curr_len, len(new_memory)))
    return new_memory


def decode_inst(pc, memory):
    """
    decode a single instruction
    This may extend the memory list, so we need to return memory every time
    so that our outer routines know about the new list.
    :param pc: the current program counter (location in memory)
    :param memory: the machine's memory
    :return: (param_list, op_function, result_loc, instruction_width, memory)
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
        # missing digits are mode zero (positional). Do one extra, to
        # accommodate the return value possibly being relative
        for n in range(len(md.OP_DEFS[base_opcode]['p_locs']) + 1):
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
        #
        # We may get a memory location that is past the end of the current
        # allocation. Catch the exception, extend the array and retry.
        retry = True
        retried_once = False
        while retry:
            try:
                retry = False
                # disable retry. We'll re-enable it if we  take an IndexError.
                if param_mode == md.PARAM_MODE_POSITIONAL:
                    index = absolute_parameter_loc
                    params.append(memory[index])
                elif param_mode == md.PARAM_MODE_IMMEDIATE:
                    # This won't take an exception. Doesn't reference memory
                    params.append(absolute_parameter_loc)
                elif param_mode == md.PARAM_MODE_RELATIVE:
                    index = absolute_parameter_loc + op.get_relative_base()
                    params.append(memory[index])
                else:
                    # Oops!  Bad param mode.  Report and halt.
                    print("Bad parameter mode encountered: {}. Halting".
                          format(param_mode))
                    op.halt([])
            except IndexError:
                # Make sure we don't loop retrying.
                if retried_once:
                    raise
                # Enable a retry
                retry = True
                retried_once = True
                # Extend memory
                memory = get_virtual_memory(memory, index)

    if param_modes[op_def['result_loc'] - 1] == md.PARAM_MODE_RELATIVE:
        base = op.get_relative_base()
    else:
        base = pc
    result_loc = memory[op_def['result_loc'] + pc] + base

    return (params,
            op_def['op_function'],
            result_loc,
            op_def['instruction_width'],
            memory,
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
            print(pc, len(memory))
            # Have to get memory returned, because we may have to extend the
            # list, and need a handle on the new list.
            params, op_function, result_loc, inst_width, memory = \
                decode_inst(pc, memory)

            # We know everything we need to execute the instruction.
            result = op_function(params)

            # SPECIAL CASE
            # The instructions listed below don't return a value to store.
            if op_function not in (
                op.output,
                op.jump_if_true,
                op.jump_if_false,
                op.adjust_relative_base,
            ):
                # Set up for possible need to expand memory.
                retry = True
                retried_once = False
                while retry:
                    try:
                        retry = False
                        memory[result_loc] = result
                    except IndexError:
                        # Make sure we don't loop retrying.
                        if retried_once:
                            raise
                        # Enable a retry
                        retry = True
                        retried_once = True
                        # Extend memory
                        memory = get_virtual_memory(memory, result_loc)

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
    with open('9 input.txt') as f:
        line = f.readline()
        print(line)
        memory = list(map(int, line.split(',')))
    for idx, opcode in enumerate(memory):
        if opcode == 1102:
            print("inst is at pc", idx)
    execute(memory)


if __name__ == '__main__':
    main()
