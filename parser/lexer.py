from rply import LexerGenerator
import re
import csv


def getLexer():
    """
    Return a Lexer objects and a token list
    """
    TOKEN_MAP_FILE = "syntax/python9-tokens.csv"
    lg = LexerGenerator()
    tokens = []
    with open(TOKEN_MAP_FILE, mode='r') as csv_file:
        str = csv.reader(csv_file, delimiter=';')
        for row in str:
            lg.add(row[0], eval(row[1]))
            tokens.append(row[0])
    tokens.append('$end')
    lg.ignore('[ \t\r\f\v]+')
    return lg.build(), tokens
