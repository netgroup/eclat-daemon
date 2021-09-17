
from sys import argv


class Chain():
    def __init__(self, name, block):
        self.name = name
        self.block = block

    def to_c(self):
        return self.block.to_c()


class Block():
    def __init__(self, statements):
        self.statements = statements

    def to_c(self):
        return "\n".join([s.to_c() for s in self.statements])


class Statement():
    pass


class FunctionCall():
    def __init__(self, lvalue, rvalue, ltype=None):
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.ltype = ltype

    def to_c(self):
        pass


class Assigment(Statement):
    def __init__(self, lvalue, rvalue, ltype=None):
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.ltype = ltype

    def to_c(self):
        if self.ltype:
            type = self.ltype.to_c()
            return f"{type} {self.lvalue} = {self.rvalue};"
        else:
            return f"{self.lvalue} = {self.rvalue};"


class Pass(Statement):
    def to_c(self):
        return ""


class Argument():
    def __init__(self, arg, type=None):
        self.arg = argv
        self.type = type

    def to_c(self):
        if self.type:
            return f"{self.type} {self.arg}"
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
