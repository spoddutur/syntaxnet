from my_parser_eval import SyntaxNetProcess
from my_parser_eval import _write_input
from my_parser_eval import _read_output
from my_parser_eval import pretty_print
import sys

if (len(sys.argv) > 2):
	print("Please only call me with one parameter")
	sys.exit()

sentence = sys.argv [1]
print(sentence)
print "====================="

tagger = SyntaxNetProcess("brain_tagger")
parser = SyntaxNetProcess("brain_parser")

_write_input(sentence)
tagger.eval()
print "TAGGER OUTPUT=================="
print _read_output()

_write_input(_read_output())
parser.eval()
print "PARSER OUTPUT=================="
print _read_output()

print "Print as tree:"
pretty_print()
