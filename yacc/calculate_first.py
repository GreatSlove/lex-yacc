import time
import pandas as pd

class State:
    def __init__(self, items):
        self.items = items

class Token:
    def __init__(self, value):
        self.value = value

class Symbol:
    NONTERMINAL = 'nonterminal'
    TERMINAL = 'terminal'
    EPSILON = 'epsilon'
    EOF = 'eof'

    def __init__(self, symbol_type, value=None):
        self.symbol_type = symbol_type
        self.value = value

    @staticmethod
    def non_terminal(value):
        return Symbol(Symbol.NONTERMINAL, value)
    
    @staticmethod
    def terminal(value):
        return Symbol(Symbol.TERMINAL, value)
    
    @staticmethod
    def epsilon():
        return Symbol(Symbol.EPSILON)
    
    @staticmethod
    def eof():
        return Symbol(Symbol.EOF)
    
    def __eq__(self, other):
        return self.symbol_type == other.symbol_type and self.value == other.value
    
    def __hash__(self):
        return hash((self.symbol_type, self.value))
    
    def __repr__(self):
        if self.symbol_type == Symbol.EPSILON:
            return 'ε'
        elif self.symbol_type == Symbol.EOF:
            return '$'
        return self.value
    
    def __str__(self):
        return self.__repr__()
    
class Rule:
    def __init__(self, symbol, production):
        self.symbol = symbol
        self.production = production

    def __eq__(self, other):
        return self.symbol == other.symbol and self.production == other.production
    
    def __hash__(self):
        return hash((self.symbol, tuple(self.production)))
    
    def __repr__(self):
        return f'{self.symbol} -> {" ".join(map(str, self.production))}'

class Grammar:
    def __init__(self, start_symbol, rules):
        self.start_symbol = start_symbol
        self.rules = rules
        self.symbols = set([self.start_symbol] + [rule.symbol for rule in self.rules] + [symbol for rule in self.rules for symbol in rule.production])
    
    def non_terminals(self):
        return [symbol for symbol in self.symbols if symbol.symbol_type == Symbol.NONTERMINAL]
    
    def terminals(self):
        return [symbol for symbol in self.symbols if symbol.symbol_type == Symbol.TERMINAL]

first_single_cache = {}

def first_single(grammar, X):
    if X in first_single_cache:
        return first_single_cache[X]
    first_single_cache[X] = set()
    old_result = None
    result = set()
    while old_result != result:
        old_result = result.copy()
        if X.symbol_type == Symbol.TERMINAL:
            result.add(X)
        elif X.symbol_type == Symbol.EPSILON:
            result.add(Symbol.epsilon())
        elif X.symbol_type == Symbol.NONTERMINAL:
            for rule in grammar.rules:
                if rule.symbol == X:
                    has_epsilon = True
                    for Y in rule.production:
                        if has_epsilon:
                            Y_first = first(grammar, Y)
                            result.update(Y_first)
                            if Symbol.epsilon() not in Y_first:
                                has_epsilon = False
                    if has_epsilon:
                        result.add(Symbol.epsilon())
        elif X.symbol_type == Symbol.EOF:
            result.add(Symbol.eof())
    first_single_cache[X] = result
    return result


def first(grammar, α):
    if isinstance(α, Symbol):
        α = [α]
    result = set()
    for X in α:
        X_first = first_single(grammar, X)
        result.update(X_first)
        if Symbol.epsilon() not in X_first:
            break
    return result