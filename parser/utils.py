def indent_script(input_script):
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
    text
