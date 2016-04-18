from . import cc_templates as templates
from . import parser
from . import err


def translate(program):
  assert program[0] == 'program'
  _, modules = program

  method_names = get_all_method_names(program)
  attribute_names = get_all_attribute_names(program)
  translated_modules = ''.join(map(translate_module, modules))

  return templates.PROGRAM.format(
      translated_modules=translated_modules)


class NameCollector(parser.Visitor):

  def __init__(self):
    self.method_names = set()
    self.attr_names = set()
    self.fn_names = dict()

  def visit_class(self, node):
    assert node[0] == 'class', node[0]
    _, _, _, _, members, methods = node

    mems = dict()
    for member in members:
      _, token, name, _ = member
      if name in mems:
        raise err.Err('Duplicate attribute', mems[name], token)
      mems[name] = token
      self.attr_names.add(name)

    meths = dict()
    for method in methods:
      _, token, name, _, _, _ = method
      if name in meths:
        raise err.Err('Duplicate method', meths[name], token)
      meths[name] = token
      self.method_names.add(name)

  def visit_fn(self, node):
    assert node[0] == 'fn', node[0]
    _, token, name, _, _, _ = node
    if name in self.fn_names:
      raise err.Err('Duplicate functions', self.fn_names[name], token)
    self.fn_names[name] = token




