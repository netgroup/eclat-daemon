import re


def lexer_preprocessor(source):
    """
    Pre-process the script to feed the lexer
    """

    def remove_comment(line):
        """
        Remove comments from a line
        """
        comments = r'(#.*)(?:\n|\Z)'
        comment = re.search(comments, line)
        while comment is not None:
            start, end = comment.span(1)
            assert start >= 0 and end >= 0
            # rimuovi la stringa che matcha con il commento
            line = line[0:start] + line[end:]
            comment = re.search(comments, line)
        return line

    def indentation(s, tabsize=4):
        """
        Return the indentation value
        """
        sx = s.expandtabs(tabsize)
        return 0 if sx.isspace() else len(sx) - len(sx.lstrip())

    block = False
    indent_space = 4
    indent_stack = [0]
    dedent = ""
    text = ""
    for line_num, line in enumerate(source.splitlines(), 0):
        line = line.rstrip()
        line = line.replace("\t", " "*indent_space)
        # ------------------------------------------- #
        # rimuovo i commenti dalla riga               #
        line = remove_comment(line)
        # ------------------------------------------- #
        # Se la riga non è vuota                      #
        if line.strip():
            # ------------------------------------------- #
            # Calcolo il valore dell'indentazione         #
            indent_number = indentation(line, indent_space)

            # ------------------------------------------- #
            # Se l'indentazione trovata è diversa dall'   #
            # ultimo elemento dello stack, e non sono     #
            # alla riga successiva ad una apertura di un  #
            # blocco (:),  significa che forse si sta     #
            # "chiudendo" un blocco, perciò controllo che #
            # sia in modulo 4
            if indent_number != indent_stack[-1]:
                if not block and indent_number < indent_stack[-1] and indent_number % indent_space == 0:
                    while indent_stack[-1] != indent_number:
                        indent_stack.pop()
                        dedent += " _dedent "
                    line = dedent + line
                    dedent = ""
                else:
                    raise IndentationError("at line " + str(1+line_num))

            if block:
                line = " _indent " + line
                block = False

            # ------------------------------------------- #
            # Se lo statement successivo è un Block (:)   #
            if line[len(line)-1:len(line)] == ":":
                indent_stack.append(indent_stack[-1]+indent_space)
                block = True
            text = text + line + "\n"

    # ------------------------------------------- #
    # Inserisco gli eventuali dedent rimasti      #
    for dedent in range(len(indent_stack)-1):
        text += " _dedent "
    return text
