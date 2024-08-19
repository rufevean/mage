
from magelang.scanner import Scanner
from magelang.parser import Parser 
from magelang.passes.classify_rules import format_rule


def parse_grammar(content: str):
    scanner = Scanner(content, filename="<test>")
    parser = Parser(scanner)
    return parser.parse_grammar()
    
  
test_grammar = """
pub expr = [a-z]+
pub start = expr
"""

for rule in parse_grammar(test_grammar).rules:
    print(format_rule(rule, parse_grammar(test_grammar))) 

()
