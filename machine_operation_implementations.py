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
            val = input(
                "A genie gives three wishes, but you only get one. "
                "Enter an integer: ")
            val = int(val)
            break
        except ValueError:
            print("I said enter an integer.  C'mon.  Try again.")
    return val


def output(params):
    # No computation needed.  We're just printing a memory value.
    print("The machine says: {}".format(params[0]))
    return None


def jump_if_true(params):
    if params[0]:
        return params[1]
    else:
        return None


def jump_if_false(params):
    if not params[0]:
        return params[1]
    else:
        return None


def less_than(params):
    if params[0] < params[1]:
        return 1
    else:
        return 0


def equals(params):
    if params[0] == params[1]:
        return 1
    else:
        return 0


def halt(params):
    # We're done.  Blow through the instruction decoder and catch this
    # in the main execute() loop.
    raise HaltException
