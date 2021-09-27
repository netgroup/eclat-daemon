
   @_('ELIF expression COLON block')
   def elif_statement(self, p):
        return Elif(p.expression, p.block)


    @_('IF expression COLON block NEWLINE elif_statement', 
        'IF expression COLON block NEWLINE')
    def if_statement(self, p):
        return If(p.expression, p.block)

    @_('if_statement')
    def statement(self, p):
        # Non funziona l'IF normale
        print("XXXXXXXXXXXXXXXXXX")
        return p
        # return If(p.expression, p.block)

    # @_('IF expression COLON NEWLINE block',)
    # def statement(self, p):
    #    return If(p.expression, p.block)

    

    # @ _('FROM NAME IMPORT module_list')
    # def import_stmt(self, p):
    #     self.imports[p.NAME] = self._imports_name[:]
    #     self._imports_name = []

    # @ _('NAME COMMA module_list',
    #     'NAME')
    # def module_list(self, p):
    #     self._imports_name.append(p.NAME)
    #     return p

    ########### TODO #########
    # expression
    # statements: if, while, for, return

    # chiamare i moduli
    # modificare mappe (?)

    # const
    # variabili globali
