# TODO: Clean up.
from . import lexer
from . import parser


source = lexer.Source('<test>', r"""

var x = 5

fn main[] {
  print[x]
  print[x._add_[6]]
  var y = 'hi'
  var z
  print[y._add_[' there']]
}

""")

result = parser.parse(source)

assert repr(result) == """('module', (var, 'var')@2, [], [('fn', (fn, 'fn')@13, 'main', [], None, ('block', ({, '{')@23, [('expr', ('mcall', ([, '[')@32, ('id', (ID, 'print')@27, 'print'), '_call_', ('args', ([, '[')@32, [('id', (ID, 'x')@33, 'x')], None))), ('expr', ('mcall', ([, '[')@43, ('id', (ID, 'print')@38, 'print'), '_call_', ('args', ([, '[')@43, [('mcall', (., '.')@45, ('id', (ID, 'x')@44, 'x'), '_add_', ('args', ([, '[')@51, [('num', (NUM, '6')@52, '6')], None))], None))), ('var', (var, 'var')@58, 'y', ('str', (STR, "'hi'")@66, "'hi'")), ('var', (var, 'var')@73, 'z', None), ('expr', ('mcall', ([, '[')@86, ('id', (ID, 'print')@81, 'print'), '_call_', ('args', ([, '[')@86, [('mcall', (., '.')@88, ('id', (ID, 'y')@87, 'y'), '_add_', ('args', ([, '[')@94, [('str', (STR, "' there'")@95, "' there'")], None))], None)))]))], [], [('var', (var, 'var')@2, 'x', ('num', (NUM, '5')@10, '5'))])""", result


