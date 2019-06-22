from abc import ABC, abstractmethod

from model.GrammarTypeValidator import RGValidator


class FormalGrammar(ABC):

    def __init__(self, symbols, sigma, prods, root, name="Grammar",
            grammarValidator=RGValidator):
        if not (symbols and sigma and prods and root):
            raise ValueError("Parameters must not be null.")

        self.symbols = symbols
        self.sigma = sigma
        self.productions = prods
        self.root = root
        self.name = name

        if not grammarValidator.validProductions(self):
            raise ValueError("Invalid grammar type.")

    def updateProductions(self, prods):
        self.productions = prods

    def derivate(self, iform, n):
        pass

    def apply_productions(self, w):
        pass

    def productionsDictionary(self):
        pdict = {}
        for prod in self.productions:
            pdict[prod[0]] = prod[1]
        return pdict

    def __str__(self):
        grammarStr = ""
        for p in self.productions:
            grammarStr += p[0] + " -> "
            for b in p[1]:
                beta = "".join(b)
                grammarStr += beta + " | "
            grammarStr = grammarStr[:-2] + '\n'  # add \n removing extra "| "
        return grammarStr.strip()
