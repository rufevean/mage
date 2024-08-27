
import pytest
from magelang.parser import Parser
from magelang.scanner import Scanner
from magelang.passes.check_undefined import check_undefined
from magelang.util import pipe

def parse_grammar(content: str):
    """Helper function to parse grammar content."""
    scanner = Scanner(content, filename="<test>")
    parser = Parser(scanner)
    return parser.parse_grammar()

def test_check_undefined_no_error():
    """Test that check_undefined does not raise an error for valid grammar."""
    valid_grammar = """
    pub start = expr
    expr = 'foo'
    """
    grammar = parse_grammar(valid_grammar)
    
    # Optional: Uncomment for debugging purposes
    # print("Parsed Grammar Rules:", grammar.rules)  
    
    try:
        # Applying check_undefined to the valid grammar should not raise an error
        grammar = pipe(grammar, check_undefined)
    except ValueError:
        pytest.fail("check_undefined raised ValueError unexpectedly")

def test_check_undefined_with_error():
    """Test that check_undefined raises an error for grammar with undefined rules."""
    invalid_grammar = """
    pub start = expr
    expr = foo # 'foo' is not defined
    """
    grammar = parse_grammar(invalid_grammar)
    
    # Optional: Uncomment for debugging purposes
    # print("Parsed Grammar Rules:", grammar.rules)  
    
    # Using pytest.raises to check for ValueError with specific message
    with pytest.raises(ValueError, match="Undefined rule referenced: foo"):
        grammar = pipe(grammar, check_undefined)

