"""
Vv* : Class name
vm* : method
va* : attribute name
vv* : value name (variables and functions)
"""

def translate(program):
  return translate_program(program)

def translate_program(program):
  assert program[0] == 'program', program[0]
  _, modules = program
  return ''.join(map(translate_module, modules))

def translate_module(module):
  assert module[0] == 'module', module[0]
  _, token, _, fns, clss, decls = module
  tfns = ''.join(map(translate_fn, fns))
  tclss = ''.join(map(translate_class, clss))
  tdecls = ''.join(map(translate_global_vars, decls))
  return ''.join(map(indent, (tfns, tclss, tdecls)))

def translate_fn(fn):
  assert fn[0] == 'fn', fn[0]
  _, token, name, _, _, _ = fn
  return r"vv{name} = {content};".format(
      name=name,
      content=translate_fn_content(fn))

def translate_fn_content(fn):
  assert fn[0] == 'fn', fn[0]
  _, token, name, argnames, varargname, body = fn
  return r"""new VvFunction() {{
  public VvObject vm_call_({sig}){body}
}}""".format(body=translate_statement(body))


def indent(text):
  return text.replace('\n', '\n  ')
