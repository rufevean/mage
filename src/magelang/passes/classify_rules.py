
from magelang.ast import Grammar, Rule
from magelang.parser import Parser
from magelang.scanner import Scanner 

grammar_rules_list = []

def read_file(filename: str) -> str:
    with open(filename, "r") as file:
        return file.read() 

def parse_test() -> Grammar:
    scanner = Scanner(read_file("gp.mage")) 
    token = scanner.scan() 
    parser = Parser(scanner)
    grammar = parser.parse_grammar()
    grammar_rules_list.append(grammar.rules)
    return grammar 

def format_rule(rule: Rule) -> str:
     return f"Rule Name: {rule.name}, Expression: {rule.expr}"

parse_test()

print("Parsed Grammar Rules:")

for rule_list in grammar_rules_list:
    for rule in rule_list:
        print(format_rule(rule))

