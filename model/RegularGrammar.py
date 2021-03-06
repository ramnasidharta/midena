from model.FormalGrammar import FormalGrammar
from model.GrammarTypeValidator import RGValidator, CFGValidator


class RegularGrammar(FormalGrammar):

    def __init__(self, symbols, sigma, prods, s, name="Regular_Grammar"):
        super().__init__(symbols, sigma, prods, s, name, RGValidator())
        self.type = 3


if __name__ == "__main__":
    # alphabet: {0,1} and starts with 0
    s = ("S", ["0A", "0"])
    a = ("A", ["0A", "1A", "0", "1"])
    productions = [s, a]
    rg = RegularGrammar(symbols="SA01", sigma="01", prods=productions, s='S')

    # not Regular Grammars
    print("N: non terminals, T: terminals, X: something")
    s = ("S", ["0A", "0"])
    a = ("A", ["0A", "10", "0", "1"])  # N -> TT
    b = ("A", ["0A", "1B", "0", "1"])  # N -> TX
    c = ("A", ["0A", "B1", "0", "1"])  # N -> XT
    d = ("A", ["0A", "AA", "0", "1"])  # N -> NN
    e = ("A", ["0A", "BA", "0", "1"])  # N -> XN
    prods1 = [s, a]
    prods2 = [s, b]
    prods3 = [s, c]
    prods4 = [s, d]
    prods5 = [s, e]

    try:
        rg = RegularGrammar(symbols="SA01", sigma="01", prods=prods1, s='S')
    except ValueError:
        print("[ERROR] Production N -> TT")

    try:
        rg = RegularGrammar(symbols="SA01", sigma="01", prods=prods2, s='S')
    except ValueError:
        print("[ERROR] Production N -> TX")

    try:
        rg = RegularGrammar(symbols="SA01", sigma="01", prods=prods3, s='S')
    except ValueError:
        print("[ERROR] Production N -> XT")

    try:
        rg = RegularGrammar(symbols="SA01", sigma="01", prods=prods4, s='S')
    except ValueError:
        print("[ERROR] Production N -> NN")

    try:
        rg = RegularGrammar(symbols="SA01", sigma="01", prods=prods5, s='S')
    except ValueError:
        print("[ERROR] Production N -> XN")
