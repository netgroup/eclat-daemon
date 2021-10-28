from sys import argv


class Chain():
    def __init__(self, name, arguments, block):
        self.name = name
        self.block = block
        self.arguments = arguments

    def to_c(self, package):
        list_of_arguments = [a.to_c(for_chain=True)
                             for a in self.arguments]
        flat_arguments = [
            item for sublist in list_of_arguments for item in sublist]

        n_args = len(self.arguments)
        placeholder = f"hike_chain_{package}_{self.name}".upper()
        flat_c_params = ', '.join([placeholder] + flat_arguments)
        # e.g. HIKE_CHAIN_3(HIKE_CHAIN_BAR_ID, __u8, allow, __u16, eth_type)
        return f"""HIKE_CHAIN_{n_args + 1}({flat_c_params})
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
        print(self.statement)
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


class For(Statement):
    def __init__(self, expression, block):
        self.expression = expression
        self.block = block

    def to_c(self):
        return f"for ({self.expression.to_c()}) {{ {self.block.to_c()} }}"


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


class Return(Statement):
    def __init__(self, expression):
        self.expression = expression

    def to_c(self):
        return f"return {self.expression.to_c()}"


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


class UnaryExpression(Expression):
    def __init__(self, operator, value):
        super().__init__()
        self.value = value
        self.operator = operator
        self.operator_map = {
            '~': '~',
            'not': '!',
        }

    def to_c(self):
        value = self.value.to_c() if hasattr(self.value, 'to_c') else self.value
        operator = self.operator_map[self.operator]
        return self.handle_brackets(f"{operator} {value}")


class BinaryExpression(Expression):
    def __init__(self, lvalue, operator, rvalue):
        super().__init__()
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.operator = operator
        # python <-> C operators conversion
        self.operator_map = {
            '+': '+',
            '-': '-',
            '*': '*',
            '/': '/',
            '%': '%',
            '>': '>',
            '<': '<',
            '>=': '>=',
            '<=': '<=',
            '==': '==',
            '!=': '!=',
            'and': '&&',
            'or': '||',
        }

    def to_c(self):
        rvalue = self.rvalue.to_c() if hasattr(self.rvalue, 'to_c') else self.rvalue
        lvalue = self.lvalue.to_c() if hasattr(self.lvalue, 'to_c') else self.lvalue
        operator = self.operator_map[self.operator]
        return self.handle_brackets(f"{lvalue} {operator} {rvalue}")


class FunctionCall(Expression):
    def __init__(self, function_name, parameters, globals, imports={}, object=None, mapper={}, loaders={}):
        super().__init__()
        self.function_name = function_name
        self.parameters = parameters
        self.object = object  # this function belongs to a pseudo-object
        self.mapper = mapper
        self.globals = globals
        self.imports = imports
        self.loaders = loaders

    def to_c(self):
        flat_parameters = ', '.join([a.to_c() for a in self.parameters])

        if self.object:
            # object are syntatic sugar for a set of functions
            # e.g., Packet.read -> hike_packet_read_u16
            # the mapper function is defined in the mapper dir
            # objects are also loaders, supporting only the attach method

            # is a classifier?
            for l_package, l_names in self.imports['loaders'].items():
                if self.object in l_names:
                    package = l_package
                    if self.function_name == 'attach':
                        # ipv6_classifier.attach('enp6s0f0', 'xdp')
                        self.loaders.append({
                            'name': self.object,
                            'package': package,
                            'attach_type': self.parameters[1].to_c().replace("'", "").replace('"', ""),
                            'dev': self.parameters[0].to_c().replace("'", "").replace('"', ""),
                        })
                        return ""
                    else:
                        raise NotImplemented(
                            "No other method but attach has been implemented in a loader")

            # or maybe an object
            obj_map = self.mapper.get(self.object, {})
            try:
                if self.parameters:
                    ret = obj_map['methods'][self.function_name]['template'].format(
                        *[a.to_c() for a in self.parameters])
                else:
                    ret = obj_map['methods'][self.function_name]['template']
                # inject dependencies (if any)
                deps = obj_map['methods'][self.function_name].get(
                    'dependencies', None)
                if deps:
                    self.globals.append(deps)
                return ret
            except KeyError:
                return f"{self.object}_{self.function_name}({flat_parameters})"
        else:
            # conventional function call
            params_n = len(self.parameters)
            # get the package
            package = None

            for f_package, f_names in self.imports['programs'].items():
                if self.function_name in f_names:
                    package = f_package
                    import_class = "programs"

            if not package:
                raise Exception(
                    f"function {self.function_name} has not been imported")

            placeholder = f"HIKE_EBPF_PROG_{package}_{self.function_name}".upper(
            )
            args = self.parameters if self.parameters else []
            flatted_c_args = ",".join(
                [placeholder, ] + [a.to_c() for a in args])
            return f"hike_elem_call_{params_n + 1}({flatted_c_args})".upper()


class Argument():
    def __init__(self, arg, type=None):
        self.arg = arg
        self.type = type

    def to_c(self, for_chain=False):
        if self.type:
            if for_chain:
                return [self.type.to_c(), self.arg]
            else:
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
        return f"__{self.type.lower()}"
