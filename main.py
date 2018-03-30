from my_parser_eval import SyntaxNetProcess
from my_parser_eval import _write_input
from my_parser_eval import _read_output
from my_parser_eval import pretty_print

tagger = SyntaxNetProcess("brain_tagger")
parser = SyntaxNetProcess("brain_parser")

_write_input("Bob brought the pizza to Alice")
tagger.eval()
print "TAGGER OUTPUT=================="
print _read_output()

_write_input(_read_output())
parser.eval()
print "PARSER OUTPUT=================="
print _read_output()

print "Print as tree:"
pretty_print()
