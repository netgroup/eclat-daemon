

def preprocessor(text):
    """
    1) insert INDENT DEDENT
    2) transform tab in spaces
    """


def process_indentation(lines):
    """Insert INDENT and DEDENT when indentation occurs.
    """
    INDENT = "_INDENT"
    DEDENT = "_DEDENT"
    curr_indentation_level = 0
    indentations = [0, ]
    output = ""

    for lineno, line in enumerate(lines):
        # remove spaces at the end and skip white lines
        line = line.rstrip()
        if not line:
            continue

        initial_spaces = len(line) - len(line.lstrip(' '))
        if initial_spaces > curr_indentation_level:
            indentations.append(initial_spaces)
            output += INDENT + line + '\n'
            #print("indenting of {} space".format(initial_spaces))
        elif initial_spaces < curr_indentation_level:
            indentations.pop()
            expected_spaces = indentations[-1]
            if expected_spaces != initial_spaces:
                raise Exception("Syntax error on line {}: expected {} space for deindent ({} received)".format(
                    lineno, expected_spaces, initial_spaces))
            output += DEDENT + line + '\n'
        else:
            output += line + '\n'
        curr_indentation_level = initial_spaces
    while (len(indentations) > 1):
        indentation = indentations.pop()
        output += "DEDENT\n"

    return output


text = """
def prova(ciao):
    ciao
    cao
pippo
    io
"""
ret = process_indentation(text.split('\n'))
print(ret)
