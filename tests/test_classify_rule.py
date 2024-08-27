
import pytest
from magelang.parser import Parser
from magelang.scanner import Scanner
from magelang.passes.classify_rules import format_rule

def parse_grammar(content: str):
    """Helper function to parse grammar content."""
    scanner = Scanner(content, filename="<test>")
    parser = Parser(scanner)
    return parser.parse_grammar()

def test_rule_type_classification():
    """Test that rules are classified correctly based on their type."""
    test_grammar = """
    pub expr = [a-z]+
    pub start = expr
    """
    
    # Parse the grammar
    grammar = parse_grammar(test_grammar)
    
    # Expected types for rules
    expected_types = ["Token Rule", "Parse Rule"]

    # Extract the actual types of the rules
    actual_types = [format_rule(rule, grammar).split(", Type: ")[1] for rule in grammar.rules]

    # Assert that the actual types match the expected types with custom error messages
    for expected, actual, rule in zip(expected_types, actual_types, grammar.rules):
        assert actual == expected, f"Rule '{rule.name}' expected to be '{expected}', but got '{actual}'."


""" 
 NEED TO ADD MORE TEST CASES
"""
