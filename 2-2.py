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

PARAM_1_POS = 1
PARAM_2_POS = 2
RESULT_POS = 3

INSTRUCTION_WIDTH = 4


def decode_inst(pc, memory):
    """
    decode a single instruction
    :param pc: the current program counter (location in memory)
    :param memory: the machine's memory
    :return: (op, param_1_value, param_2_value, result_loc)
    """
    opcode = memory[pc]
    if opcode != OP_HALT:
        param_1_loc = memory[pc + PARAM_1_POS]
        param_1_value = memory[param_1_loc]
        param_2_loc = memory[pc + PARAM_2_POS]
        param_2_value = memory[param_2_loc]
        result_loc = memory[pc + RESULT_POS]
    else:
        param_1_value = None
        param_2_value = None
        result_loc = None
    return opcode, param_1_value, param_2_value, result_loc


def execute(memory):
    """
    Loop over the instructions until we get a halt.
    :param memory: The memory of our machine implemented as a list.
    :return: None
    """
    pc = 0

    # Silence PyCharm warnings
    result = None

    while True:
        opcode, param_1, param_2, result_loc = decode_inst(pc, memory)

        # Are we done?
        if opcode == OP_HALT:
            # Yes
            return

        # OP_ADD
        elif opcode == OP_ADD:
            result = param_1 + param_2

        # OP_MULTIPLY
        elif opcode == OP_MULTIPLY:
            result = param_1 * param_2

        # Undefined operation.  Report the error and exit.
        else:
            print("Unknown opcode '{}' encountered. Exiting.".format(opcode))

        # Store the result
        memory[result_loc] = result

        # Advance the PC
        pc += INSTRUCTION_WIDTH


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
