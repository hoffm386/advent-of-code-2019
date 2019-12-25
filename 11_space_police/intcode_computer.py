################################################################################
# Utility functions
#
# These functions are used repeatedly, wherever there is overlapping logic
# between the different opcodes
################################################################################

def get_param_mode(param_modes_str, param_num):
    """
    There is no real reason that these digits need to be converted into strings,
    but I think it's more readable this way

    Args:
        param_modes_str (str): a string representing the param "modes" for the 
            Intcode command.  The modes are ordered right to left, where any
            missing digit is an implicit leading 0
        param_num (int): a number representing which param we want the mode for.
            This is always hard-coded in my current logic, based on which
            command we are running (since they have varying numbers of params)

    Returns:
        A string representing the "mode", either "position", "immediate", or
        "relative"
    """

    if param_num <= len(param_modes_str):
        mode_code = param_modes_str[-param_num]
        if mode_code == "0":
            return "position"
        elif mode_code == "1":
            return "immediate"
        elif mode_code == "2":
            return "relative"
    else:
        # missing is the same as "0"
        return "position"


def fill_with_zeroes_to_index(program_codes, index):
    """
    If we're trying to use an index that's "off the end" of the program, extend
    the program with a bunch of zeroes

    Args:
        program_codes (list): the list of integer program codes
        index (int): the index where the current command wants to read/write
    
    Returns:
        Nothing, it just modifies program_codes in place if needed
    """
    
    zero_fill_needed = index - len(program_codes) + 1
    for _ in range(zero_fill_needed):
        program_codes.append(0)


def get_input_value(program_codes, param_modes, current_position, relative_base, param_num):
    """
    The prompt calls everything a "param" but I distinguish between "input" and
    "destination" params.  This is the logic to find an input param.

    Args:
        program_codes (list): the list of integer program codes
        param_modes (str): a string representing the param "modes" for the 
            Intcode command.  The modes are ordered right to left, where any
            missing digit is an implicit leading 0
        current_position (int): a pointer to the current instruction in 
            program_codes
        relative_base (int): a pointer that is used only by "relative" mode
        param_num (int): a number representing which param we want the mode for.
            This is always hard-coded in my current logic, based on which
            command we are running (since they have varying numbers of params)

    Returns:
        An integer representing the value of this "input" param
    """
    param_mode = get_param_mode(param_modes, param_num)
    # "position" means that the input represents an index, from which we need to
    # retrieve the actual value
    if param_mode == "position":
        fill_with_zeroes_to_index(program_codes, current_position + param_num)
        input_index = program_codes[current_position + param_num]

        fill_with_zeroes_to_index(program_codes, input_index)
        input_value = program_codes[input_index]
    # "immediate" means that the input represents the actual value
    elif param_mode == "immediate":
        fill_with_zeroes_to_index(program_codes, current_position + param_num)
        input_value = program_codes[current_position + param_num]
    # "relative" means that the input represents an index relative to the 
    # current relative base, from which we need to retrieve the actual value
    elif param_mode == "relative":
        fill_with_zeroes_to_index(program_codes, current_position + param_num)
        input_index = program_codes[current_position +
                                    param_num] + relative_base

        fill_with_zeroes_to_index(program_codes, input_index)
        input_value = program_codes[input_index]

    return input_value


def get_destination_index(program_codes, param_modes, current_position, relative_base, param_num):
    """
    The prompt calls everything a "param" but I distinguish between "input" and
    "destination" params.  This is the logic to find a destination param.

    Args:
        program_codes (list): the list of integer program codes
        param_modes (str): a string representing the param "modes" for the 
            Intcode command.  The modes are ordered right to left, where any
            missing digit is an implicit leading 0
        current_position (int): a pointer to the current instruction in 
            program_codes
        relative_base (int): a pointer that is used only by "relative" mode
        param_num (int): a number representing which param we want the mode for.
            This is always hard-coded in my current logic, based on which
            command we are running (since they have varying numbers of params)

    Returns:
        An integer representing the value of this "destination" param
    """
    param_mode = get_param_mode(param_modes, param_num)

    # "position" means that the input represents an index
    # this works but I'm still kind of confused by the concept.  it makes no
    # sense for you to be able to use immediate mode for a destination, since
    # you can write to index 5 but you can't just write to 5.  but for some
    # reason things seem to break if I don't accept "immediate"
    if param_mode == "immediate" or param_mode == "position":
        fill_with_zeroes_to_index(program_codes, current_position + param_num)
        destination_index = program_codes[current_position + param_num]
    # "relative" means that the input represents an index relative to the
    # current relative base
    elif param_mode == "relative":
        fill_with_zeroes_to_index(program_codes, current_position + param_num)
        destination_index = program_codes[current_position +
                                          param_num] + relative_base

    return destination_index

################################################################################
# Opcode functions
#
# It pains me how much these have repetitive code, but rewriting them this way
# eliminated some mysterious buggy behavior.  Each is only used once, but it 
# keeps the code more modular and prevents run_intcode_program from being a
# gazillion lines long.
################################################################################


def run_opcode_1(program_codes, param_modes, current_position, relative_base):
    """
    Opcode 1: take in two inputs, add them together, set the destination index
    to the result
    """
    first_input = get_input_value(
        program_codes, param_modes, current_position, relative_base, 1)
    second_input = get_input_value(
        program_codes, param_modes, current_position, relative_base, 2)

    destination_index = get_destination_index(
        program_codes, param_modes, current_position, relative_base, 3)

    output = first_input + second_input

    fill_with_zeroes_to_index(program_codes, destination_index)
    program_codes[destination_index] = output

    current_position += 4

    return current_position, relative_base


def run_opcode_2(program_codes, param_modes, current_position, relative_base):
    """
    Opcode 2: take in two inputs, multiply them together, set the destination
    index to the result
    """
    first_input = get_input_value(
        program_codes, param_modes, current_position, relative_base, 1)
    second_input = get_input_value(
        program_codes, param_modes, current_position, relative_base, 2)

    destination_index = get_destination_index(
        program_codes, param_modes, current_position, relative_base, 3)

    output = first_input * second_input

    fill_with_zeroes_to_index(program_codes, destination_index)
    program_codes[destination_index] = output

    current_position += 4

    return current_position, relative_base


def run_opcode_3(program_codes, param_modes, current_position, relative_base):
    """
    Opcode 3: get input from the user, set the destination index to the result
    """
    user_input = int(input("Enter a number: "))
    destination_index = get_destination_index(
        program_codes, param_modes, current_position, relative_base, 1)

    fill_with_zeroes_to_index(program_codes, destination_index)
    program_codes[destination_index] = user_input

    current_position += 2

    return current_position, relative_base


def run_opcode_4(program_codes, param_modes, current_position, relative_base):
    """
    Opcode 4: print the value of the 1 and only input
    """
    input_value = get_input_value(
        program_codes, param_modes, current_position, relative_base, 1)

    print(input_value)

    current_position += 2

    return current_position, relative_base


def run_opcode_5(program_codes, param_modes, current_position, relative_base):
    """
    Opcode 5: if the first input is not 0, set the current position to the
    second input
    """
    first_input = get_input_value(
        program_codes, param_modes, current_position, relative_base, 1)
    second_input = get_input_value(
        program_codes, param_modes, current_position, relative_base, 2)

    should_jump = first_input != 0

    if should_jump:
        current_position = second_input
    else:
        current_position += 3

    return current_position, relative_base


def run_opcode_6(program_codes, param_modes, current_position, relative_base):
    """
    Opcode 6: if the first input is 0, set the current position to the second input
    """
    first_input = get_input_value(
        program_codes, param_modes, current_position, relative_base, 1)
    second_input = get_input_value(
        program_codes, param_modes, current_position, relative_base, 2)

    should_jump = first_input == 0

    if should_jump:
        current_position = second_input
    else:
        current_position += 3

    return current_position, relative_base


def run_opcode_7(program_codes, param_modes, current_position, relative_base):
    """
    Opcode 7: if the first input is less than the second parameter, store 1 in
    the destination index.  Otherwise, store 0.
    """
    first_input = get_input_value(
        program_codes, param_modes, current_position, relative_base, 1)
    second_input = get_input_value(
        program_codes, param_modes, current_position, relative_base, 2)

    destination_index = get_destination_index(
        program_codes, param_modes, current_position, relative_base, 3)
    fill_with_zeroes_to_index(program_codes, destination_index)

    comparison_true = first_input < second_input

    if comparison_true:
        program_codes[destination_index] = 1
    else:
        program_codes[destination_index] = 0

    current_position = current_position + 4

    return current_position, relative_base


def run_opcode_8(program_codes, param_modes, current_position, relative_base):
    """
    Opcode 8: if the first input is equal to the second parameter, store 1 in
    the destination index.  Otherwise, store 0.
    """
    first_input = get_input_value(
        program_codes, param_modes, current_position, relative_base, 1)
    second_input = get_input_value(
        program_codes, param_modes, current_position, relative_base, 2)

    destination_index = get_destination_index(
        program_codes, param_modes, current_position, relative_base, 3)
    fill_with_zeroes_to_index(program_codes, destination_index)

    comparison_true = first_input == second_input

    if comparison_true:
        program_codes[destination_index] = 1
    else:
        program_codes[destination_index] = 0

    current_position = current_position + 4

    return current_position, relative_base


def run_opcode_9(program_codes, param_modes, current_position, relative_base):
    """
    Opcode 9: adjusts the relative base by the value of its only parameter.
    The relative base increases (or decreases, if the value is negative)
    by the value of the parameter.
    """
    first_input = get_input_value(
        program_codes, param_modes, current_position, relative_base, 1)
    relative_base += first_input

    current_position += 2

    return current_position, relative_base

################################################################################
# Driver function
#
# run_intcode_program executes everything from a complete list program
################################################################################


def run_intcode_program(program_codes, verbose=False):
    """
    Run the whole program

    Args:
        program_codes (list): a list of integers, representing the "program"
        verbose (bool): True if the program should print a lot of logging
            statements, False by default

    Returns:
        Nothing, although outputs will be printed for each instance of opcode 4
    """
    # set up the pointers to both be 0 at the beginning
    current_position = 0
    relative_base = 0
    while True:
        # the first number represents the opcode and param modes for the instruction
        opcode_and_param_modes = str(program_codes[current_position])
        opcode = int(opcode_and_param_modes[-2:])
        param_modes = opcode_and_param_modes[:-2]

        if verbose:
            print("**********Opcode", opcode, "and param modes",
                  param_modes, "***************")

        # 99 means quit immediately
        if opcode == 99:
            break

        # run the relevant function for the opcode.
        # this would be a good candidate for a switch statement if the language
        # supported them, but doesn't seem worthwhile to do a workaround
        if opcode == 1:
            current_position, relative_base = run_opcode_1(
                program_codes, param_modes, current_position, relative_base)
        elif opcode == 2:
            current_position, relative_base = run_opcode_2(
                program_codes, param_modes, current_position, relative_base)
        elif opcode == 3:
            current_position, relative_base = run_opcode_3(
                program_codes, param_modes, current_position, relative_base)
        elif opcode == 4:
            current_position, relative_base = run_opcode_4(
                program_codes, param_modes, current_position, relative_base)
        elif opcode == 5:
            current_position, relative_base = run_opcode_5(
                program_codes, param_modes, current_position, relative_base)
        elif opcode == 6:
            current_position, relative_base = run_opcode_6(
                program_codes, param_modes, current_position, relative_base)
        elif opcode == 7:
            current_position, relative_base = run_opcode_7(
                program_codes, param_modes, current_position, relative_base)
        elif opcode == 8:
            current_position, relative_base = run_opcode_8(
                program_codes, param_modes, current_position, relative_base)
        elif opcode == 9:
            current_position, relative_base = run_opcode_9(
                program_codes, param_modes, current_position, relative_base)
        else:
            # this should never happen, but I want to avoid an infinite loop
            print("Error, encountered opcode", opcode)
            break
