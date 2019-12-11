import machine_operation_implementations as op

# Define machine characteristics
OP_ADD = 1
OP_MULTIPLY = 2
OP_INPUT = 3
OP_OUTPUT = 4
OP_JUMP_IF_TRUE = 5
OP_JUMP_IF_FALSE = 6
OP_LESS_THAN = 7
OP_EQUALS = 8
OP_ADJUST_RELATIVE_BASE = 9
OP_HALT = 99

PARAM_MODE_POSITIONAL = 0
PARAM_MODE_IMMEDIATE = 1
PARAM_MODE_RELATIVE = 2

RETURN_LOCATION_PC = -1

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
OP_DEFS = {
    OP_ADD: {
        'p_locs': [1, 2],
        'result_loc': 3,
        'op_function': op.add,
        'instruction_width': 4,
    },
    OP_MULTIPLY: {
        'p_locs': [1, 2],
        'result_loc': 3,
        'op_function': op.multiply,
        'instruction_width': 4,
    },
    OP_INPUT: {
        'p_locs': [1],
        'result_loc': 1,
        'op_function': op.input_func,
        'instruction_width': 2,
    },
    OP_OUTPUT: {
        'p_locs': [1],
        # OP_OUTPUT has no result. Specifying the same location as the
        # p_loc does no harm.
        'result_loc': 1,
        'op_function': op.output,
        'instruction_width': 2,
    },
    OP_JUMP_IF_TRUE: {
        'p_locs': [1, 2],
        # The result location is not used by jump_if_true or _false.
        'result_loc': 2,
        'op_function': op.jump_if_true,
        'instruction_width': 3,
    },
    OP_JUMP_IF_FALSE: {
        'p_locs': [1, 2],
        'result_loc': 2,
        'op_function': op.jump_if_false,
        'instruction_width': 3,
    },
    OP_LESS_THAN: {
        'p_locs': [1, 2],
        'result_loc': 3,
        'op_function': op.less_than,
        'instruction_width': 4,
    },
    OP_EQUALS: {
        'p_locs': [1, 2],
        'result_loc': 3,
        'op_function': op.equals,
        'instruction_width': 4,
    },
    OP_ADJUST_RELATIVE_BASE: {
        'p_locs': [1],
        'result_loc': 1,
        'op_function': op.adjust_relative_base,
        'instruction_width': 2,
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
        'op_function': op.halt,
        'instruction_width': 1,
    },
}

