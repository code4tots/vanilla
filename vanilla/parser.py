from . import err
from . import lexer


def parse(source):
  return Parser(source).parse_module()


class Parser(object):

  def __init__(self, source):
    self.source = source
    self.tokens = lexer.lex(source)
    self.i = 0

  def peek(self):
    return self.tokens[self.i]

  def gettok(self):
    self.i += 1
    return self.tokens[self.i-1]

  def at(self, type_):
    return self.peek().type == type_

  def consume(self, type_):
    if self.at(type_):
      return self.gettok()

  def expect(self, type_):
    if self.at(type_):
      return self.gettok()
    else:
      raise err.Err(
          'Expected token of type %r but found %r' % (
              type_, self.peek()),
          self.peek())

  ##############

  def parse_module(self):
    token = self.peek()
    incs = []
    fns = []
    clss = []
    decls = []
    while not self.at('EOF'):
      if self.consume('include'):
        incs.append(self.expect('ID').value)
      elif self.at('fn'):
        fns.append(self.parse_fn())
      elif self.at('class'):
        clss.append(self.parse_class())
      elif self.at('var'):
        decls.append(self.parse_var())
      else:
        raise err.Err('Expected top level', token)
    return 'module', token, incs, fns, clss, decls

  def parse_fn(self):
    token = self.expect('fn')
    name = None
    if not self.at('['):
      name = self.expect('ID').value
    self.expect('[')
    argnames = []
    varargname = None
    while not self.consume(']'):
      if self.consume('*'):
        varargname = self.expect('ID').value
        self.expect(']')
        break
      else:
        argnames.append(self.expect('ID').value)
        self.consume(',')
    body = self.parse_block()
    return 'fn', token, name, argnames, varargname, body

  def parse_class(self):
    token = self.expect('class')
    name = self.expect('ID').value
    base = 'Object'
    if self.consume('<'):
      base = self.expect('ID').value
    self.expect('{')
    members = []
    methods = []
    while not self.consume('}'):
      if self.at('var'):
        members.append(self.parse_var())
      elif self.at('fn'):
        methods.append(self.parse_fn())
      else:
        raise err.Err('Expected member or method', token)
    return 'class', token, name, base, members, methods

  def parse_var(self):
    token = self.expect('var')
    name = self.expect('ID').value
    expr = None
    if self.consume('='):
      expr = self.parse_expr()
    return 'var', token, name, expr

  def parse_block(self):
    token = self.expect('{')
    stmts = []
    while not self.consume('}'):
      stmts.append(self.parse_stmt())
    return 'block', token, stmts

  def parse_stmt(self):
    token = self.peek()
    if self.consume('break'):
      return 'break', token
    elif self.consume('continue'):
      return 'continue', token
    elif self.consume('while'):
      cond = self.parse_expr()
      body = self.parse_block()
      return 'while', token, cond, body
    elif self.at('if'):
      return self.parse_if()
    elif self.at('var'):
      return self.parse_var()
    elif self.at('{'):
      return self.parse_block()
    else:
      return 'expr', self.parse_expr()

  def parse_if(self):
    token = self.expect('if')
    cond = self.parse_expr()
    body = self.parse_block()
    other = None
    if self.consume('else'):
      if self.at('if'):
        other = self.parse_if()
      else:
        other = self.parse_block()
    return 'if', token, cond, body, other

  def parse_expr(self):
    return self.parse_postfix_expr()

  def parse_postfix_expr(self):
    e = self.parse_primary_expr()
    while True:
      token = self.peek()
      if self.at('['):
        args = self.parse_args()
        e = ('mcall', token, e, '_call_', args)
      elif self.consume('.'):
        name = self.expect('ID').value
        if self.at('['):
          args = self.parse_args()
          e = ('mcall', token, e, name, args)
        elif self.consume('='):
          val = self.parse_expr()
          e = ('setattr', token, e, name, val)
        else:
          e = ('getattr', token, e, name)
      else:
        break
    return e

  def parse_primary_expr(self):
    token = self.peek()
    if self.at('('):
      e = self.parse_expr()
      self.expect(')')
      return e
    elif self.at('NUM'):
      return 'num', token, self.expect('NUM').value
    elif self.at('STR'):
      return 'str', token, self.expect('STR').value
    elif self.consume('self'):
      return 'self', token
    elif self.at('ID'):
      name = self.expect('ID').value
      if self.consume('='):
        expr = self.parse_expr()
        return 'assign', token, name, expr
      else:
        return 'id', token, name
    elif self.at('fn'):
      return self.parse_fn()
    else:
      raise err.Err('Expected expression', token)

  def parse_args(self):
    token = self.expect('[')
    args = []
    vararg = None
    while not self.consume(']'):
      if self.consume('*'):
        vararg = self.parse_expr()
        self.expect(']')
        break
      else:
        args.append(self.parse_expr())
        self.consume(',')
    return 'args', token, args, vararg

