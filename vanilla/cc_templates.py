PROGRAM = r"""

struct VvObject {
  int refcnt = 0;

{member_stubs}
{method_stubs}
};

{translated_modules}

"""
