
from magelang.ast import Grammar, Rule, RefExpr, SeqExpr, ChoiceExpr, ListExpr, RepeatExpr, LookaheadExpr,CharSetExpr
from magelang.parser import Parser
from magelang.scanner import Scanner 


def check_rule(grammar: Grammar, expr) -> bool:
    assert isinstance(expr, (RefExpr, SeqExpr, ChoiceExpr, ListExpr, RepeatExpr, LookaheadExpr, CharSetExpr)), \
        f"Unexpected expression type: {type(expr)}"
    
    if isinstance(expr, RefExpr):
        rule = grammar.lookup(expr.name)
        assert rule is not None, f"Rule '{expr.name}' not found in grammar"
        
        if rule.is_public:
            return True
        if rule.is_extern:
            return False
        if rule.expr is not None:
            return check_rule(grammar, rule.expr)
        
        raise RuntimeError(f"Rule '{expr.name}' has no associated expression")

    elif isinstance(expr, (SeqExpr, ChoiceExpr)):
        if not expr.elements:
            raise ValueError("SeqExpr and ChoiceExpr must have at least one element")
        return any(check_rule(grammar, element) for element in expr.elements)

    elif isinstance(expr, ListExpr):
        if expr.element is None:
            raise ValueError("ListExpr must have a non-None element")
        return check_rule(grammar, expr.element) or (expr.separator is not None and check_rule(grammar, expr.separator))

    elif isinstance(expr, (RepeatExpr, LookaheadExpr)):
        if expr.expr is None:
            raise ValueError("RepeatExpr and LookaheadExpr must have a non-None expression")
        return check_rule(grammar, expr.expr)

    elif isinstance(expr, CharSetExpr):
        """ Added this because of an error i encountered while running the test """ 
        return False

    return False


"""
Helper functions for the classify_rules pass. 
                - rufevean 2024 
"""
def is_parse_rule(grammar: Grammar, rule: Rule) -> bool:

    return check_rule(grammar, rule.expr)

def format_rule(rule: Rule, grammar: Grammar) -> str:

    rule_type = "Parse Rule" if is_parse_rule(grammar, rule) else "Token Rule"
    return f"Rule Name: {rule.name}, Type: {rule_type}"

def parse_test(input_string: str) -> Grammar:

    scanner = Scanner(input_string) 
    parser = Parser(scanner)
    return parser.parse_grammar()
