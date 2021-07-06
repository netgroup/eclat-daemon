def get_Id(program, hike_program):
    if program in hike_program:
        return hike_program[program][0]
    else:
        raise Exception("Hike Program '" + program + "' not found.")


def exec_by_id(arg_number, str_arg):
    if arg_number > 0:
        return 'hike_elem_call_' + str(arg_number) + "(" + str_arg[2:]
    else:
        raise Exception("The expected number of parameter in 'exec_by_id' is minimum: 1" +
                        ", found: " + str(arg_number))
