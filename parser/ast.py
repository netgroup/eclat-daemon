from rply.token import BaseBox
from integer import Integer
import settings
import importlib
import os.path
import csv
import sys
import warnings

HIKE_DATA_LIST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), settings.HIKE_DATA_LIST)
ECLAT_DATA= os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), settings.ECLAT_DATA)
HIKE_PROGRAM = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), settings.HIKE_PROGRAM)
HIKE_REGISTRY = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), settings.HIKE_REGISTRY)
HEADER_LIST_LIB = """#include <stddef.h>
#include <linux/in.h>
#include <linux/if_ether.h>
#include <linux/if_packet.h>
#include <linux/ipv6.h>
#include <linux/seg6.h>
#include <linux/errno.h>

#define HIKE_DEBUG 1
#include "hike_vm.h"
"""



# class Path():
#import_path = "eCLAT_Code/Code/Lib/Import/"
# registry_path = 'eCLAT_Code/Code/Lib/regisrty.csv' # spostare in RAM
#hike_program_path = "eCLAT_Code/Code/Lib/eclat_program_list.csv"
#token_path = "eCLAT_Code/Code/Lib/token.csv"

# --------------------------------------- #
#           CLASSE DI APPOGGIO            #
#     PER SCRIVERE LE DICHIARAZIONI       #
# --------------------------------------- #
class Appoggio():
    import_module = {}
    # Variabile di appoggio in cui viene memorizzato il nome
    # della funzione corrente
    funzione_corrente = ""

    # variabile per vedere se c'è un return
    return_presente = False

    # Contatore per l'indentazione del file .c
    indent_level = 0

    # Questa stringa mi serve, durante un assignement, per
    # memorizzare il nome della variabile a sinistra per
    # riutilizzarala nella Packet.read
    var_packet_read = ""

    # dict per gli Alias quando assegno una funzione ad un parametro
    funzioni_alias = {}

    # dict contenente le variabili globali con associato la
    # stringa #define per il file .c
    variabili_globali = {}

    # dict avente come chiavi le chain dichiarate e come valore per
    # ogni chiave un dict che ha come chiavi le variabili e gli
    # argomenti locali a cui è associato un array contenente la
    # dimensione (u8, u16 ecc), il valore della variabile, se è
    # una variabile (VAR) o un argomento (ARG), se la dimensione è
    # stata messa manualmente (DECLARED) o no (UNDECLARED).
    # [dimension, value, "VAR"/"ARG", "DECLARED"/"UNDECLARED"]
    variabili_locali = {}

    # dict dei programmi Hike presenti nel file eclat_program_list
    hike_program = {}

    # dict delle Chain prese dal file regisrty
    chain_registry = {}

    # --------------------------------------- #
    # Queste ultime due variabili mi servono  #
    # per eliminare le parentesi di troppo.   #
    # Tale inconveniente è dovuto al fatto    #
    # che in Python la condizione può NON     #
    # essere racchiusa tra parentesi.         #
    # Infatti se c'è più di un Expression     #
    # tra quelle trovate le parentesi non     #
    # necessarie.                             #
    # --------------------------------------- #
    # variabile usata per dire se sono all'interno di una condizione (if/while)
    in_condition = False
    # contatore per le condizioni (if/while)
    exp_count = 0

# --------------------------------------- #
#           FUNZIONE PROVVISORIA          #
# Trova il programma nei file se presente #
# --------------------------------------- #


def find_Program(statement):
    if statement in Appoggio.hike_program:
        return str(Appoggio.hike_program[statement][0]) \
            + " " + str(Appoggio.hike_program[statement][1])
    if statement in Appoggio.chain_registry:
        return "HIKE_CHAIN_" \
            + str(Appoggio.chain_registry[statement]) + "_ID"
    raise Exception("\"" + statement
                    + "\" Hike Program/Function not defined")


#################################################
#                   PROGRAM                     #
#################################################
class Program(BaseBox):
    def __init__(self, statement, package_name):
        self.statements = []
        self.statements.append(statement)
        self.package_name = package_name

    def add_statement(self, statement):
        self.statements.insert(0, statement)

    def exec(self, env):
        # ----------------------------------------- #
        # prima passata per "scorrere" le funzioni  #
        # e le variabili, e per l'escuzione         #
        prima_passata = ""
        for statement in self.statements:
            result = statement.exec(env)
            prima_passata += statement.prima_passata(env)
        # ----------------------------------------- #
        # Controllo se le funzioni dichiarate sono  #
        # già esistenti, in basse al NameSpace      #
        # fornito, allo stesso tempo metto i valori #
        # in un dict "dict_registry".               #
        funzioni = ""
        count = 74
        name_space = self.package_name
        dict_registry = {}
        # if os.path.exists(HIKE_REGISTRY):
        #     with open(HIKE_REGISTRY, mode='r') as csv_file:
        #         read = csv.reader(csv_file, delimiter=';')
        #         for row in read:
        #             dict_registry[int(row[0])] = row[1:]
        #             if len(row) > 1:
        #                 if row[1] == name_space:
        #                     if row[2] in Appoggio.variabili_locali:
        #                         raise Exception("Function '" + row[2] +
        #                                         "' in NameSpace '" + name_space+"' already exist. Change file or chain name.")
        #                 count = int(row[0])
        count += 1
        # ----------------------------------------- #
        # Aggiorno il "dict_regisrty" e scrivo le   #
        # chain da aggiungere al file .c            #
        for fun in Appoggio.variabili_locali:
            dict_registry[count] = [name_space, fun]
            if len(dict_registry[count]) > 1:
                Appoggio.chain_registry[fun] = count
            funzioni += "#define " + "HIKE_CHAIN_" + str(count) \
                        + "_ID" + " " + str(count) + "\n"
            count += 1
        # ----------------------------------------- #
        # CONVERTO IN C, Il risultato è in 'output' #
        output = ""
        for statement in self.statements:
            output += statement.to_c(env)
        # ----------------------------------------- #
        # Riscrivo il file regisrty.csv con i       #
        # i valori aggiornati e riempio il dict     #
        # "chain_registry" che mi serivirà per      #
        # repire gli ID delle chain.                #
        # with open(HIKE_REGISTRY, 'w', newline='') as csv_file:
        #     writer = csv.writer(csv_file, delimiter=';')
        #     for row in dict_registry:
        #         if len(dict_registry[row]) > 1:
        #             writer.writerow(
        #                 [row, dict_registry[row][0], dict_registry[row][1]])
        #         else:
        #             writer.writerow([row])
        # ----------------------------------------- #
        # Importo i #define di default e            #
        # incollo (in ordine):    
        # - lista librerie                          #
        # - le funzioni (chain) dichiarate          #
        # - il codice .c calcolato                  #
        output = HEADER_LIST_LIB + funzioni + output
        # ----------------------------------------- #
        return output
        #print("\nVARIABILI: ")
        # for var in env.variables:
        #    print(var, env.variables[var])
        #return result

    def get_statements(self):
        return self.statements


#################################################
#                     BLOCK                     #
#################################################
class Block(BaseBox):
    def __init__(self, statement):
        self.statements = []
        self.statements.append(statement)

    def add_statement(self, statement):
        self.statements.insert(0, statement)

    def get_statements(self):
        return self.statements

    def exec(self, env):
        result = ""
        for statement in self.statements:
            result = statement.exec(env)
        return result

    def to_c(self, env):
        result = ''
        Appoggio.indent_level += 1
        for statement in self.statements:
            stmt = statement.to_c(env)
            result += '\t'*Appoggio.indent_level + stmt
            if result[-1] != '{' and result[-1] != '}' and result[-1] != ';' and len(stmt) > 0:
                result += ';'
            result += '\n'

        Appoggio.indent_level -= 1
        return result

    def prima_passata(self, env):
        result = ""
        for statement in self.statements:
            if statement.prima_passata(env) != "" and statement.prima_passata(env) != ",":
                result += statement.prima_passata(env) + ","
        return result


#################################################
#                 EXPRESSION                    #
#################################################
class Expression(BaseBox):
    def __init__(self, value):
        self.value = value

    def exec(self, env):
        return self.value.exec(env)

    def prima_passata(self, env):
        return ""

    def to_c(self, env):
        # ----------------------------------------- #
        # Se sono all'interno di una condizione     #
        # incremento ogni volta che incotro un Exp  #
        # Questo per eliminare doppie parentesi se  #
        # viene trovata una sola Exp                #
        # Infatti se c'è più di un Expression     #
        # tra quelle trovate le parentesi non     #
        # necessarie.                             #
        # --------------------------------------- #
        if Appoggio.in_condition:
            Appoggio.exp_count += 1
        return "(" + self.value.to_c(env) + ")"


#################################################
#                     NULL                      #
#################################################
class Null(BaseBox):
    def exec(self, env):
        return self

    def prima_passata(self, env):
        return ""

    def to_c(self, env):
        return 'Null'

#################################################
#                    BOOLEAN                    #
#################################################


class Boolean(BaseBox):
    def __init__(self, value):
        self.value = bool(value)

    def exec(self, env):
        return self.value

    def prima_passata(self, env):
        return str(self.value)

    def to_c(self, env):
        if self.value:
            return "1"
        else:
            return "0"

#################################################
#                   INTEGER                     #
#################################################


class Integer():
    def __init__(self, value, base):
        self.value = int(value)
        self.base = base

    def exec(self, env):
        return self.value

    def prima_passata(self, env):
        return str(self.value)

    def to_c(self, env):
        # Per gestire le basi
        if self.base == 16:
            return str(hex(self.value))
        if self.base == 10:
            return str(self.value)


#################################################
#                     FLOAT                     #
#################################################
class Float(BaseBox):
    def __init__(self, value):
        self.value = float(value)

    def exec(self, env):
        return self.value

    def prima_passata(self, env):
        return str(self.value)

    def to_c(self, env):
        return str(self.value)


#################################################
#                    STRING                     #
#################################################
class String(BaseBox):
    def __init__(self, value):
        self.value = str(value)

    def exec(self, env):
        return self.value

    def prima_passata(self, env):
        return str(self.value)

    def to_c(self, env):
        return "\"" + str(self.value) + "\""


#################################################
#                  VARIABLE                     #
#################################################
class Variable(BaseBox):
    def __init__(self, name):
        self.name = str(name)
        self.value = None

    def getname(self):
        return str(self.name)

    def exec(self, env):
        if env.variables.get(self.name, None) is not None:
            self.value = env.variables[self.name]
            return self.value
            raise Exception("Not yet defined " + str(self.name))

    def to_c(self, env):
        # ----------------------------------------- #
        # Se sono all'interno di una funzione       #
        if Appoggio.funzione_corrente != "":
            # Se è una variabile globale.           #
            if self.name in Appoggio.variabili_globali:
                return self.name.upper()
            if Appoggio.funzione_corrente in Appoggio.variabili_locali:
                if self.name in Appoggio.variabili_locali[Appoggio.funzione_corrente]:
                    return self.name
        else:
            return self.name.upper()
        raise Exception("Variable \"" + str(self.name) + "\" not declared")

    def prima_passata(self, env):
        # ----------------------------------------- #
        # Il controllo dell'errore è in .to_c(),    #
        # ----------------------------------------- #
        return str(self.name)


#################################################
#               BINARY OPERATION                #
#################################################
class BinaryOperation():
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def exec(self, env):
        if self.operator == '+':
            return self.left.exec(env).__add__(self.right.exec(env))
        elif self.operator == '-':
            return self.left.exec(env).__sub__(self.right.exec(env))
        elif self.operator == '*':
            return self.left.exec(env).__mul__(self.right.exec(env))
        elif self.operator == '/':
            return self.left.exec(env).__div__(self.right.exec(env))
        elif self.operator == '==':
            return self.left.exec(env).__eq__(self.right.exec(env))
        elif self.operator == '!=':
            result = self.left.exec(env).__eq__(self.right.exec(env))
            result.value = not result.value
            return result
        elif self.operator == '>=':
            return self.left.exec(env).__ge__(self.right.exec(env))
        elif self.operator == '<=':
            return self.left.exec(env).__le__(self.right.exec(env))
        elif self.operator == '>':
            return self.left.exec(env).__gt__(self.right.exec(env))
        elif self.operator == '<':
            return self.left.exec(env).__lt__(self.right.exec(env))
        elif self.operator == 'AND':
            one = self.left.exec(env).equals(Boolean(True))
            two = self.right.exec(env).equals(Boolean(True))
            return Boolean(one.value and two.value)
        elif self.operator == 'OR':
            one = self.left.exec(env).equals(Boolean(True))
            two = self.right.exec(env).equals(Boolean(True))
            return Boolean(one.value or two.value)
        ### BITWISE OPERATION #####
        elif self.operator == '&':
            return int(self.left.exec(env)) & int(self.right.exec(env))
        elif self.operator == '|':
            return int(self.left.exec(env)) | int(self.right.exec(env))
        elif self.operator == '^':
            return int(self.left.exec(env)) ^ int(self.right.exec(env))
        elif self.operator == '<<':
            return int(self.left.exec(env)) << int(self.right.exec(env))
        elif self.operator == '>>':
            return int(self.left.exec(env)) >> int(self.right.exec(env))
        else:
            raise Exception("Shouldn't be possible")

    def to_c(self, env):
        return ' ' + self.left.to_c(env) + ' ' \
            + self.operator + ' ' + self.right.to_c(env) + ' '

    def prima_passata(self, env):
        return ' ' + self.left.prima_passata(env) + ' ' \
            + self.operator + ' ' + self.right.prima_passata(env) + ' '


#################################################
#                     NOT                       #
#################################################
class Not(BaseBox):
    def __init__(self, value):
        self.value = value

    def exec(self, env):
        result = self.value.exec(env)
        if isinstance(result, Boolean):
            return Boolean(not result.value)
        raise LogicError("Cannot 'not' that")

    def to_c(self, env):
        return 'not%s ' % (self.value.to_c(env))

    def prima_passata(self, env):
        return ""


#################################################
#               BIT-WISE NOT                    #
#################################################
class BitWise_Not(BaseBox):
    def __init__(self, value):
        self.value = value

    def exec(self, env):
        result = self.value.exec(env)
        return ~bin(result.value)
        raise LogicError("Cannot 'not' that")

    def to_c(self, env):
        return 'BitWise_Not(%s)' % (self.value.to_c(env))

    def prima_passata(self, env):
        return ""


#################################################
#                 FROM IMPORT                   #
#################################################
class FromImport(BaseBox):
    def __init__(self, to_co, args):
        self.to_co = to_co
        self.args = args

    def exec(self, env):
        self.args.exec(env)
        #raise LogicError("Cannot assign to this")

    def to_c(self, env):
        result = ''
        if self.to_co == "hike":
            for statement in self.args.get_statements():
                result += '\n#define ' + Appoggio.hike_program[statement][0] + " " \
                    + Appoggio.hike_program[statement][1] + '\n'
        return result

    def prima_passata(self, env):
        # Controllo il modulo
        if self.to_co == "net":
            path = ECLAT_DATA
            for statement in self.args.get_statements():
                currentDirectory = os.getcwd()
                os.chdir(path)
                try:    
                    Appoggio.import_module[str(statement)] = __import__("net", str(statement))
                except:
                    raise ModuleNotFoundError()
                os.chdir(currentDirectory)
            return ""
        elif self.to_co == "hike":
            path = HIKE_PROGRAM + "hike/"
            for statement in self.args.get_statements():
                if os.path.exists(path + statement + ".bpf.c"):
                    # ----------------------------------------- #
                    # Per ogni programma hike importato leggo i #
                    # valori dal file eclat_program_list.csv e  #
                    # li salvo IN UN DICT PER COMODITA'.        #
                    with open(HIKE_DATA_LIST, mode='r') as csv_file:
                        string = csv.reader(csv_file, delimiter=';')
                        for row in string:
                            if statement == row[0]:
                                Appoggio.hike_program[row[0]] = [row[1], row[2]]
                else:
                    raise Exception(str(statement + ".bpf.c not found."))
            return ""
        else:
            raise Exception(str(self.to_co + " not found."))
        


#################################################
#                    IMPORT                     #
#################################################
class Import(BaseBox):
    def __init__(self, args):
        self.args = args

    def exec(self, env):
        self.args.exec(env)
        #raise LogicError("Cannot assign to this")

    def to_c(self, env):
        result = ''
        for statement in self.args.get_statements():
            path_array = str(statement).split(".")
            if path_array[0] == "hike":
                path = ECLAT_DATA+ "hike_program"
                if os.path.exists(path):
                    module = "/".join(path_array[1:])
                    if os.path.exists(path + "/" + module + ".c"):
                        result += '\n#define ' + Appoggio.hike_program[module][0] + " " \
                            + Appoggio.hike_program[module][1] + '\n'
                        #result += "#include \"" + path + "/" + module + ".c\"\n"
                    elif os.path.exists(path + "/" + module + ".py"):
                        # ----------------------------------------- #
                        # Per packet nel .c non devo scrivere nulla #
                        pass
                    else:
                        raise Exception(path + "/" + module + ".c not found.")
                else:
                    raise Exception(path + " not found.")
        return result

    def prima_passata(self, env):
        path = ECLAT_DATA
        for statement in self.args.get_statements():
            path_array = str(statement).split(".")
            num = 0
            if path_array[0] == "hike":
                # ----------------------------------------- #
                # Per ogni programma hike importato leggo i #
                # valori dal file eclat_program_list.csv e  #
                # li salvo IN UN DICT PER COMODITA'.        #
                with open(HIKE_DATA_LIST, mode='r') as csv_file:
                    string = csv.reader(csv_file, delimiter=';')
                    for row in string:
                        if path_array[1] == row[0]:
                            Appoggio.hike_program[row[0]] = [row[1], row[2]]
            else:
                for module in path_array:
                    path += module + "/"
                    num += 1
                    # Se esiste una cartella o un file python
                    if os.path.exists(path):
                        continue
                    elif os.path.exists(path[:-1] + ".py"):
                        break
                    else:
                        raise Exception(path + " not found.")
                path_array = path_array[num:]
                module = ".".join(path_array)
                path = path.replace("/", ".")
                Appoggio.import_module[module] = importlib.import_module(
                    path[:-1], module)
        return ""


#################################################
#            VARIABLE DECLARATION               #
#################################################
class VariableDeclaration(BaseBox):
    def __init__(self, name, dimension, value=Null()):
        self.name = name
        self.dimension = dimension
        self.value = value

    def exec(self, env):
        if isinstance(self.name, Variable):
            if type(self.value) is BinaryOperation:
                env.variables[self.name.getname()] = self.value.exec(env)
            elif type(self.value) is Variable:
                env.variables[self.name.getname()] = self.value.exec(env)
            elif type(self.value) is Null:
                env.variables[self.name.getname()] = Null()
            else:
                env.variables[self.name.getname()] = self.value.value
            return self.value.exec(env)
        else:
            raise Exception("Cannot assign to this")

    def to_c(self, env):
        if type(self.value) is Null:
            return ""
            # return "__" + str(self.dimension).lower() + " " + str(self.name.getname())
        else:
            Appoggio.var_packet_read = self.name.getname()
            if type(self.value) is Call and self.value.name[:11] == "Packet.read":
                return self.value.to_c(env)
            return str(self.name.getname()) + " = " + self.value.to_c(env)

    def prima_passata(self, env):
        if not Appoggio.funzione_corrente in Appoggio.variabili_locali:
            Appoggio.variabili_locali[Appoggio.funzione_corrente] = {}
        if type(self.value) is Null:
            Appoggio.variabili_locali[Appoggio.funzione_corrente][self.name.getname()] = [
                self.dimension, "Null()", "VAR"]
        else:
            Appoggio.variabili_locali[Appoggio.funzione_corrente][self.name.getname()] = [
                self.dimension, self.value.prima_passata(env), "VAR"]
        return ""


#################################################
#            FUNCTION DECLARATION               #
#################################################
class FunctionDeclaration(BaseBox):
    def __init__(self, name, args, block):
        self.name = name
        self.args = args
        self.block = block

    def exec(self, env):
        self.block.exec(env)

    def to_c(self, env):
        Appoggio.funzione_corrente = self.name
        # -------------------------------------------- #
        # Scorro il dict delle variabili locali della  #
        # funzione separando in array di appoggio      #
        # argomenti e variabili
        function_dict = Appoggio.variabili_locali[self.name]
        Appoggio.indent_level += 1
        array_arg_appoggio = []
        array_var_appoggio = []
        arg = ""
        var = ""
        for element in function_dict:
            if function_dict[element][2] == "ARG":
                array_arg_appoggio = [element, function_dict[element][0]]
                arg += ", __" + \
                    array_arg_appoggio[1] + ", " + array_arg_appoggio[0]
            elif function_dict[element][2] == "VAR":
                array_var_appoggio = [element, function_dict[element][0]]
                var += Appoggio.indent_level*"\t" + "__" + \
                    str(array_var_appoggio[1]) + " " + \
                    str(array_var_appoggio[0]) + ";\n"
        arg += ") {\n"
        result = "\nHIKE_CHAIN_" + \
            str(len(array_arg_appoggio)+1) + \
            "(" + find_Program(self.name) + arg
        # -------------------------------------------- #
        # Se esistono variabili locali, Le INCOLLO     #
        result += var
        # -------------------------------------------- #
        # Richiamo il body della funzione              #
        Appoggio.indent_level -= 1
        result += self.block.to_c(env)
        Appoggio.indent_level += 1
        # -------------------------------------------- #
        # Controllo se è stato scritto il RETURN       #
        # statement, se NO lo scrivo in automatico     #
        Appoggio.return_presente = False
        for statement in self.block.get_statements():
            stmt = statement.to_c(env).split()
            if len(stmt) > 0 and stmt[0] == "return":
                Appoggio.return_presente = True
        if Appoggio.return_presente:
            result += '\t'*Appoggio.indent_level
        else:
            result += '\n' + '\t'*Appoggio.indent_level + 'return 0;'
        result += "\n}\n"
        Appoggio.indent_level -= 1
        Appoggio.funzione_corrente = ""
        return result

    def prima_passata(self, env):
        # +++++++++++ CONTROLLO ERRORE ++++++++++++ #
        # Controllo se sia già stata dichiarata     #
        # +++++++++++++++++++++++++++++++++++++++++ #

        if self.name in Appoggio.variabili_locali:
            raise Exception("Function \"" + str(self.name) +
                            "\" already exists.")
        Appoggio.funzione_corrente = self.name
        Appoggio.variabili_locali[self.name] = {}
        # ----------------------------------------- #
        # Metto gli argomenti in un dict            #
        arg_number = 0
        if isinstance(self.args, Array):
            for statement in self.args.get_statements():
                var = statement.split()
                if len(var) > 1:
                    Appoggio.variabili_locali[self.name][var[1]] = [
                        var[0], "Null()", "ARG"]
                else:
                    Appoggio.variabili_locali[self.name][var[0]] = [
                        "u64", "Null()", "ARG"]
                    warnings.warn("Dimension of argument '" + str(var[0]) + " in '" + str(self.name) +
                                  "' function not declared. Dimesion u64 set by default.")
                arg_number += 1
        # +++++++++++ CONTROLLO ERRORE ++++++++++++ #
        # Controllo il numero dei parametri         #
        # +++++++++++++++++++++++++++++++++++++++++ #
        if arg_number > 4:
            raise Exception("You can only pass 4 parameters")
        # ----------------------------------------- #
        # Eseguo Block il quale mette le variabili  #
        # locali in un dict                         #
        result = self.block.prima_passata(env)
        Appoggio.funzione_corrente = ""
        return str(self.name)


#################################################
#                 ASSIGNMENT                    #
#################################################
class Assignment(BinaryOperation):
    def exec(self, env):
        if isinstance(self.left, Variable):
            if type(self.right) is BinaryOperation:
                env.variables[self.left.getname()] = self.right.exec(env)
            elif type(self.right) is Variable:
                env.variables[self.left.getname()] = self.right.exec(env)
            else:
                env.variables[self.left.getname()] = self.right.value
            return self.right.exec(env)
        else:
            raise Exception("Cannot assign to this")

    def to_c(self, env):
        # ----------------------------------------- #
        # Se sono dentro o meno a una funzione      #
        # ----------------------------------------- #
        if Appoggio.funzione_corrente != "":
            # Se la funzione è stata dichiarata
            if Appoggio.funzione_corrente in Appoggio.variabili_locali:
                Appoggio.var_packet_read = self.left.getname()
                if type(self.right) is Call and self.right.name[:11] == "Packet.read":
                    return self.right.to_c(env)
                return self.left.getname() + ' = ' + self.right.to_c(env)
        else:
            # ----------------------------------------- #
            # Se è tra le variabili globali già         #
            # già dichiarate, faccio #undef e la        #
            # ridefinisco.                              #
            # Altrimenti la inserisco nel dict con      #
            # associata la stringa tradotta in .c       #
            # ----------------------------------------- #
            if self.left.getname() in Appoggio.variabili_globali:
                if Appoggio.variabili_globali[self.left.getname()] != "Null()":
                    return '#undef ' + self.left.getname().upper() \
                        + "\n#define " + self.left.getname().upper() + ' ' + \
                        str(self.right.to_c(env)) + '\n'
                else:
                    Appoggio.variabili_globali[self.left.getname()] = '\n#define '\
                        + self.left.getname().upper() + ' ' + str(self.right.to_c(env)) + '\n'
                    return Appoggio.variabili_globali[self.left.getname()]

    def prima_passata(self, env):
        # ----------------------------------------- #
        # Aggiorno il valore della variabile        #
        # nel caso in cui non è stata prima         #
        # dichiarata la dimensione, assegno di      #
        # default U64 e lancio un Warning di avviso #
        if Appoggio.funzione_corrente != "":
            if type(self.right) is Call:
                #Appoggio.funzioni_alias[self.left.getname()] = self.right.to_c(env)
                Appoggio.funzioni_alias[self.left.getname(
                )] = self.right.prima_passata(env)
            if Appoggio.funzione_corrente in Appoggio.variabili_locali:
                if self.left.getname() in Appoggio.variabili_locali[Appoggio.funzione_corrente]:
                    dim_value = Appoggio.variabili_locali[Appoggio.funzione_corrente][self.left.getname(
                    )]
                    #dim_value[1] = self.right.to_c(env)
                    dim_value[1] = self.right.prima_passata(env)
                    Appoggio.variabili_locali[Appoggio.funzione_corrente].update(
                        {self.left.getname(): dim_value})
                else:
                    #dim_value = ["u64", self.right.to_c(env), "VAR", "UNDECLARED"]
                    dim_value = ["u64", self.right.prima_passata(env), "VAR"]
                    Appoggio.variabili_locali[Appoggio.funzione_corrente].update(
                        {self.left.getname(): dim_value})
                    warnings.warn("Variable '" + self.left.getname() + "' in '" + Appoggio.funzione_corrente +
                                  "' not declared. Dimesion u64 set by default.")
            else:
                raise Exception(
                    "Function '" + Appoggio.funzione_corrente + "' not found.")
        else:
            Appoggio.variabili_globali[self.left.getname()] = "Null()"
        return str(self.left.getname())


#################################################
#                    CALL                       #
#################################################
class Call(BaseBox):
    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.value = 0

    def exec(self, env):
        result = Null()
        return result

    def prima_passata(self, env):
        # -------------------------------------------#
        # Il controllo dell'errore è fatto in .to_c  #
        # questo perchè non ho ancora a disposizione #
        # tutte le chain scritte nel file .eclat, le #
        # quali sono poi riportate nel dict:         #
        # Appoggio.chain_registry.                   #
        # Quindi il controllo va fatto alla seconda  #
        # passata.                                   #
        # -------------------------------------------#
        return ''

    def to_c(self, env):
        str_arg = ''      # Stringa per gli argomenti
        arg_number = 0    # Numero parametri trovati
        # ----------------------------------------- #
        # Metto gli argomenti in una stringa di     #
        # appoggio (str_arg)                        #
        # ----------------------------------------- #
        array_arg = []
        for statement in self.args.get_statements():
            array_arg.append(statement.to_c(env))
            # ----------------------------------------- #
            # Se è globale ovvero #define occorre       #
            # fare .upper()                             #
            # ----------------------------------------- #
            if statement.to_c(env) in Appoggio.variabili_globali:
                str_arg += ', ' + statement.to_c(env).upper()
            else:
                str_arg += ', ' + statement.to_c(env)
            arg_number += 1
        str_arg += ')'
        # -------------------------------------------#
        # Quando faccio una Call la funzione         #
        # potrebbe essere:                           #
        # - getID, funzione integrata in eCLAT per   #
        #   ottere l'ID del programma HIKE.          #
        # - un alias, ovvero una variabile a cui     #
        #   è stato assegnato un programma eCLAT     #
        #   o una chain.                             #
        # - una chain, contenuta in registry.csv     #
        # - un programma HIKE,                       #
        #   contenuto in eclat_program_list.csv      #
        # - una funzione di PACKET                   #
        # -------------------------------------------#
        string = ""
        # if self.name == "exec_by_name":
        if self.name == "exec_by_id":
            try:
                metodo = getattr(
                    Appoggio.import_module[str(self.name)], str(self.name))
                return metodo(arg_number, str_arg)
            except Exception as e:
                raise Exception(e)
        if self.name == "get_Id" and arg_number == 1:
            if type(self.args.get_statements()[0]) is String:
                string = self.args.get_statements()[0].exec(env)
            else:
                string = self.args.get_statements()[0].getname()
            try:
                metodo = getattr(
                    Appoggio.import_module[str(self.name)], str(self.name))
                return metodo(string, Appoggio.hike_program)
            except Exception as e:
                raise Exception(e)
        elif self.name == "get_Id" and not arg_number == 1:
            raise Exception("The expected number of parameter in 'getId' is: 1" +
                            ", found: " + str(arg_number))
        # ----------------------------------------- #
        #    Controllo se è una funzione PACKET     #
        # Se è una funzione Packet, richiamo la     #
        # classe packet se è stata importata        #
        # correttamente.
        # ----------------------------------------- #
        if self.name[:6] == "Packet":
            try:
                classe = getattr(Appoggio.import_module[str(
                    self.name)[:6]], str(self.name)[:6])
                metodo = getattr(classe, self.name[7:])
                if self.name[7:11] == "read":
                    if Appoggio.var_packet_read != "":
                        str_arg = "&"+Appoggio.var_packet_read + str_arg
                    else:
                        # Non sto assegnando il valore di ritorno
                        str_arg = str_arg[1:]
                return metodo(str_arg)
            except Exception as e:
                raise Exception(e)

        hike_elem_call_ = 'hike_elem_call_'
        # ------------------------------------------- #
        #         Controllo se è un alias             #
        # ------------------------------------------- #
        if self.name in Appoggio.funzioni_alias:
            ##############  PROBLEMA  #################
            # NON POSSO FARE L'ESECUZIONE ESSENDO A   #
            # BASSO LIVELLO QUINDI NON POSSO SAPERE   #
            # QUALE ALIAS SARA'DI CONSEGUENZA NON     #
            # POSSO FARE UN CONTROLLO SUL NUMERO DI   #
            # PARAMETRI PER ESEMPIO NON SO SE L'ALIAS #
            # SARA' UNA CHAIN O UN PROGRAMMA eCLAT    #
            ###########################################
            return hike_elem_call_ + str(arg_number+1) + '(' + self.name + str_arg
        # ------------------------------------------- #
        #         Controllo se è una chain            #
        # ------------------------------------------- #
        if self.name in Appoggio.variabili_locali:
            # +++++++++++ CONTROLLO ERRORE ++++++++++++ #
            # Controllo che il numero di parametri      #
            # passati sia giusto                        #
            array_arg_appoggio = []
            # ------------------------------------------- #
            # Calcolo il numero di argomenti previsti     #
            # dalla chain.                                #
            arg_index = 0
            fun_dict = Appoggio.variabili_locali[self.name]     # Chain chimata
            for element in fun_dict:
                if fun_dict[element][2] == "ARG":
                    # +++++++++++ CONTROLLO ERRORE ++++++++++++ #
                    # Controllo che il tipo dei parametri, sia  #
                    # corretto, ovvero che corrisponda con      #
                    # quello dichiarato nella chain chiamata    #
                    dim_var = Appoggio.variabili_locali[Appoggio.funzione_corrente][array_arg[arg_index]][0]
                    correct_dim_var = fun_dict[element][0]
                    if dim_var != correct_dim_var:
                        raise Exception("In '" + Appoggio.funzione_corrente + "', when '" + self.name +
                                        "' is call, argument '" + element + "' required size '" +
                                        str(correct_dim_var) + "', found: '" + str(dim_var) + "'")
                    array_arg_appoggio.append([element, fun_dict[element][0]])
                    arg_index += 1
            if len(array_arg_appoggio) != arg_number:
                raise Exception("The expected number of parameter in "
                                + self.name + " is: "
                                + str(len(array_arg_appoggio))
                                + ", found: " + str(arg_number))

            return hike_elem_call_ + str(arg_number+1) + '(' + find_Program(self.name) + str_arg
        # ------------------------------------------- #
        #      Controllo se è un hike Program         #
        # ------------------------------------------- #
        if self.name in Appoggio.hike_program:
            # +++++++++++ CONTROLLO ERRORE ++++++++++++ #
            # Controllo che il numero di parametri      #
            # passati sia al più 4                      #
            if arg_number > 4:
                raise Exception("The expected number of parameter in "
                                + self.name + " is max 4, found: " + str(arg_number))
            return hike_elem_call_ + str(arg_number+1) \
                + '(' + Appoggio.hike_program[self.name][0] + str_arg
        raise Exception("Function or Chain '" + self.name + "' not found.")


#################################################
#                    RETURN                     #
#################################################
class Return(BaseBox):
    def __init__(self, value):
        self.value = value

    def exec(self, env):
        return self.value.exec(env)

    def to_c(self, env):
        if self.value.to_c(env) == "Null":
            return "return 0"
        return 'return %s' % (self.value.to_c(env))

    def prima_passata(self, env):
        return ""


#################################################
#                      IF                       #
#################################################
class If(BaseBox):
    def __init__(self, condition, body, else_body=Null()):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def exec(self, env):
        condition = self.condition.exec(env)
        if condition:
            return self.body.exec(env)
        else:
            if type(self.else_body) is not Null:
                return self.else_body.exec(env)
        return Null()

    def to_c(self, env):
        # --------------------------------------- #
        # Questa parte di codice mi serve per     #
        # eliminare le parentesi di troppo.       #
        # Tale inconveniente è dovuto al fatto    #
        # che in Python la condizione può NON     #
        # essere racchiusa tra parentesi.         #
        # Infatti se c'è più di un Expression     #
        # tra quelle trovate le parentesi non     #
        # necessarie.                             #
        # --------------------------------------- #
        Appoggio.in_condition = True
        condition = self.condition.to_c(env)
        # if Appoggio.exp_count > 1:
        #     condition = condition[1:-1]
        if condition[0] != "(" and condition[-1] != ")":
            condition = "(" + condition + ")"
        Appoggio.in_condition = False
        result = 'if ' + condition + ' {\n' \
            + self.body.to_c(env) + Appoggio.indent_level*'\t' + '}'
        if type(self.else_body) is not Null:
            result += self.else_body.to_c(env)
        return result

    def prima_passata(self, env):
        return self.body.prima_passata(env) + "," + self.else_body.prima_passata(env)


#################################################
#                    ELSE                       #
#################################################
class Else(BaseBox):
    def __init__(self, else_body=Null()):
        self.else_body = else_body

    def exec(self, env):
        return self.else_body.exec(env)

    def to_c(self, env):
        result = '\n' + Appoggio.indent_level*'\t' + \
            'else {\n' + \
            self.else_body.to_c(env) + Appoggio.indent_level*'\t' + '}'
        return result

    def prima_passata(self, env):
        return self.else_body.prima_passata(env)


#################################################
#                    ELIF                       #
#################################################
class Elif(BaseBox):
    def __init__(self, condition, body, else_body=Null()):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def exec(self, env):
        condition = self.condition.exec(env)
        if condition:
            return self.body.exec(env)
        else:
            if type(self.else_body) is not Null:
                return self.else_body.exec(env)
        return Null()

    def to_c(self, env):
        result = '\n' + Appoggio.indent_level*'\t' + 'else {\n'
        Appoggio.in_condition = True
        condition = self.condition.to_c(env)
        if condition[0] != "(" and condition[-1] != ")":
            condition = "(" + condition + ")"
        Appoggio.in_condition = False

        Appoggio.indent_level += 1
        result += Appoggio.indent_level*'\t' + 'if ' + condition + ' {\n' \
            + self.body.to_c(env) + Appoggio.indent_level*'\t' + '}'

        if type(self.else_body) is not Null:
            result += self.else_body.to_c(env)

        Appoggio.indent_level -= 1
        result += '\n' + Appoggio.indent_level*'\t' + '}'
        return result

    def prima_passata(self, env):
        return self.body.prima_passata(env) + "," + self.else_body.prima_passata(env)


#################################################
#                    WHILE                      #
#################################################
class While(BaseBox):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def exec(self, env):
        i = 0
        while True:
            if not self.condition.exec(env):
                break
            i += 1
            self.body.exec(env)
        return Null()

    def to_c(self, env):
        # --------------------------------------- #
        # Questa parte di codice mi serve per     #
        # eliminare le parentesi di troppo.       #
        # Tale inconveniente è dovuto al fatto    #
        # che in Python la condizione può NON     #
        # essere racchiusa tra parentesi.         #
        # Infatti se c'è più di un Expression     #
        # tra quelle trovate le parentesi non     #
        # necessarie.                             #
        Appoggio.in_condition = True
        condition = self.condition.to_c(env)
        if Appoggio.exp_count > 1:
            condition = condition[1:-1]
        Appoggio.in_condition = False
        # --------------------------------------- #
        result = 'while (' + condition \
            + ') {\n' + self.body.to_c(env) \
            + Appoggio.indent_level*'\t' + '}'
        return result

    def prima_passata(self, env):
        return self.body.prima_passata(env)


class InnerArray(BaseBox):
    def __init__(self, statements=None):
        self.statements = []
        self.values = []
        if statements:
            self.statements = statements

    def push(self, statement):
        self.statements.insert(0, statement)

    def append(self, statement):
        self.statements.append(statement)

    def extend(self, statements):
        self.statements.extend(statements)

    def get_statements(self):
        return self.statements


class Array(BaseBox):
    def map(self, fun, ls):
        nls = []
        for l in ls:
            nls.append(fun(l))
        return nls

    def __init__(self, inner):
        self.statements = inner.get_statements()
        self.values = []

    def get_statements(self):
        return self.statements

    def push(self, statement):
        self.statements.insert(0, statement)

    def append(self, statement):
        self.statements.append(statement)

    def index(self, i):
        if type(i) is Integer:
            return self.values[i.value]
        if type(i) is Float:
            raise LogicError("Cannot index with that value")

    def add(self, right):
        if type(right) is Array:
            result = Array(InnerArray())
            result.values.extend(self.values)
            result.values.extend(right.values)
            return result
        raise LogicError("Cannot add that to array")

    def exec(self, env):
        if len(self.values) == 0:
            for statement in self.statements:
                # self.values.append(statement.exec(env))
                self.values.append(statement)
        return self

    def to_c(self, env):
        result = '['
        #result += ",".join(self.map(lambda x: x.to_c(env), self.statements))
        result += ",".join(self.map(lambda x: x, self.statements))
        result += ']'
        return result

    def to_string(self):
        return '[%s]' % (", ".join(self.map(lambda x: x.to_string(), self.values)))

    def prima_passata(self, env):
        return ""
