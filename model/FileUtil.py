import json
from model.FiniteAutomata import FiniteAutomata


def import_FA(path):
    data = json.load(open(path, 'r'))
    initial = data["initial"]
    accepting = data["accepting"]
    file_table = data["table"]
    sigma = []
    table = {}

    for state in file_table:
        if state not in table:
            table[state] = {}
        for symbol, transitions in file_table[state].items():
            if symbol not in sigma:
                sigma.append(symbol)
            if symbol not in table[state]:
                table[state][symbol] = []
            for i in transitions:
                table[state][symbol].append(i)
    fa = FiniteAutomata(sigma, table, initial, accepting)
    fa.name = data["name"]
    fa.regex_str = data["regex_str"]
    fa.grammar_str = data["rg_str"]
    return fa


def export_FA(fa, path):
    fa_json = {}
    fa_json["name"] = fa.name
    fa_json["sigma"] = fa.sigma
    fa_json["table"] = fa.table
    fa_json["initial"] = fa.initial
    fa_json["accepting"] = fa.accepting
    fa_json["rg_str"] = fa.grammar_str
    fa_json["regex_str"] = fa.regex_str

    with open(path, 'w') as outfile:
        json.dump(fa_json, outfile)
