
from sys import argv


class Chain():
    def __init__(self, name, arguments, block):
        self.name = name
        self.block = block
        self.arguments = arguments

    def to_c(self):
        flat_arguments = ', '.join([a.to_c() for a in self.arguments])
        return f"""{self.name}({flat_arguments})
        {{
            {self.block.to_c()}
        }}
        """


class Block():
    def __init__(self, statements):
        self.statements = statements

    def to_c(self):
        return "\n".join([s.to_c() for s in self.statements])


class Statement():
    def __init__(self, statement):
        self.statement = statement

    def to_c(self):
        # every statement must ends with a semicolon
        return self.statement.to_c() + ';'


class If(Statement):
    def __init__(self, expression, block, elif_part=None, else_part=None):
        self.expression = expression
        self.block = block
        self.elif_part = elif_part
        self.else_part = else_part

    def to_c(self):
        ret = f"if ({self.expression.to_c()}) {{ {self.block.to_c()} }}"
        if self.elif_part:
            ret += ' ' + self.elif_part.to_c()
        if self.else_part:
            ret += ' ' + self.else_part.to_c()
        return ret


class Elif(Statement):
    def __init__(self, expression, block, elif_part=None, else_part=None):
        self.expression = expression
        self.block = block
        self.elif_part = elif_part
        self.else_part = else_part

    def to_c(self):
        ret = f"else if ({self.expression.to_c()}) {{ {self.block.to_c()} }}"
        if self.elif_part:
            ret += ' ' + self.elif_part.to_c()
        if self.else_part:
            ret += ' ' + self.else_part.to_c()
        return ret


class Else(Statement):
    def __init__(self, block):
        self.block = block

    def to_c(self):
        return f"else {{ {self.block.to_c()} }}"


class While(Statement):
    def __init__(self, expression, block):
        self.expression = expression
        self.block = block

    def to_c(self):
        return f"while ({self.expression.to_c()}) {{ {self.block.to_c()} }}"


class Assigment(Statement):
    def __init__(self, lvalue, rvalue, ltype=None):
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.ltype = ltype

    def to_c(self):
        is_rvalue_expression = isinstance(self.rvalue, Expression)
        rvalue = self.rvalue.to_c() if is_rvalue_expression else self.rvalue
        if self.ltype:
            # e.g., u8 : b = 9
            type = self.ltype.to_c()
            return f"{type} {self.lvalue} = {rvalue};"
        else:
            return f"{self.lvalue} = {rvalue};"


class Pass(Statement):
    def __init__(self):
        pass

    def to_c(self):
        return ";"


# EXPRESSION
class Expression():
    def __init__(self, expression=None, brackets=False):
        self.expression = expression
        self.brackets = brackets

    def set_brackets(self):
        self.brackets = True

    def handle_brackets(self, code):
        return code if not self.brackets else f"({code})"

    def to_c(self):
        try:
            return self.handle_brackets(self.expression.to_c())
        except AttributeError:
            return self.handle_brackets(self.expression)


class BinaryExpression(Expression):
    def __init__(self, lvalue, operator, rvalue):
        super().__init__()
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.operator = operator

    def to_c(self):
        rvalue = self.rvalue.to_c() if hasattr(self.rvalue, 'to_c') else self.rvalue
        lvalue = self.lvalue.to_c() if hasattr(self.lvalue, 'to_c') else self.lvalue
        return self.handle_brackets(f"{lvalue} {self.operator} {rvalue}")


class FunctionCall(Expression):
    def __init__(self, function_name, arguments):
        super().__init__()
        self.function_name = function_name
        self.arguments = arguments

    def to_c(self):
        flat_arguments = ', '.join([a.to_c() for a in self.arguments])
        return f"{self.function_name}({flat_arguments})"


class Argument():
    def __init__(self, arg, type=None):
        self.arg = arg
        self.type = type

    def to_c(self):
        if self.type:
            return f"{self.type.to_c()} {self.arg}"
        else:
            return self.arg


class Type():
    def __init__(self, type):
        if type in ['u8', 'u16', 'u32', 'u64', 's8', 's16', 's32', 's64']:
            self.type = type
        else:
            raise Exception(f"Unsupported type {self.type}")

    def to_c(self):
        return self.type