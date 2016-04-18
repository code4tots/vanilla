import os

from . import err
from . import lexer
from . import parser


def load(roots, uris):
  modules = dict()
  stack = list(uris)
  roots = list(roots)
  if '.' not in roots:
    roots.append('.')
  loader = Loader(roots)
  seen = set([uri])
  while stack:
    uri = stack.pop()
    source = lexer.Source(uri, loader.load(uri))
    _, _, incs, _, _, _ = module = parser.parse(source)
    modules[uri] = module
    for inc in incs:
      if inc not in seen:
        seen.add(inc)
        stack.append(inc)
  return 'program', modules


# TODO: In the future, include from e.g. repositories on github.
class Loader(object):

  def __init__(self, roots):
    self.roots = list(roots)

  def load(self, uri):
    for root in self.roots:
      path = os.path.join(root, uri)
      if os.path.exists(path):
        with open(path) as f:
          return f.read()
    else:
      raise err.Err('Could not find %r (%r)' % (uri, path))

