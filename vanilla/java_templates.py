ARG_SIG = 'int lineno, String fs, VvvObject... args'
PASS_SIG = 'lineno, fs, args'

PROGRAM = r"""
import java.util.ArrayList;

public class VanillaProgram {

  public static class Entry {
    int lineno;
    String fs;
    VvvObject owner;
    String msg;
    public Entry(int lineno, String fs, VvvObject owner, String msg) {
      this.lineno = lineno;
      this.fs = fs;
      this.owner = owner;
      this.msg = msg;
    }
    public String toString() {
      if (owner == null)
        return msg + " called on line " + lineno + " of " + fs;
      else
        return
            owner.getClassName() + msg +
            " called on line " + lineno + " of " + fs;
    }
  }

  public static class Err extends RuntimeException {
    ArrayList<Entry> trace = new ArrayList<Entry>();
    public Err(String message, Entry... entries) {
      super(message);
      for (Entry e: entries) {
        trace.add(e);
      }
    }
    public void add(Entry e) {
      trace.add(e);
    }
    public void add(int lineno, String fs, VvvObject owner, String msg) {
      trace.add(new Entry(lineno, fs, owner, msg));
    }

    public String dump() {
      StringBuilder sb = new StringBuilder();
      for (Entry e: trace) {
        sb.append(e.toString());
      }
      return sb.toString();
    }
  }

  public static class VvvObject {

    public String getClassName() {
      return getClass().getName().substring(3);
    }

    // 'getattr/setattr' method stubs
{attr_stubs}
    // Vanilla method stubs
{method_stubs}
  }

  public static class VvvFunction extends VvvObject {
    public abstract VvvObject vvm_call_({sig});
  }

{clss}
{fns}
}

""".replace('{sig}', ARG_SIG)

ATTR_STUB = r"""

  public VvvObject getattr{name}({sig}) {
    throw new Err(
        getClassName() + " does not have attribute '{name}'",
        new Entry(lineno, fs, this, "getattr#{name}"));
  }

  public VvvObject setattr{name}({sig}) {
    throw new Err(
        getClassName() + " does not have attribute '{name}'",
        new Entry(lineno, fs, this, "setattr#{name}"));
  }

""".replace('{sig}', ARG_SIG)


ATTR = r"""

  public VvvObject attr{name};

  public VvvObject getattr{name}({sig}) {
    try {
      try {
        checkArgs(args, 0);
        return attr{name}
      }
      catch (final RuntimeException e) {
        if (e instanceof Err)
          throw e;
        else
          throw new Err(e.toString());
      }
    }
    catch (final Err e) {
      e.add(lineno, fs, this, "getattr#{name}");
      throw e;
    }
  }

  public VvvObject setattr{name}({sig}) {
    try {
      try {
        checkArgs(args, 1);
        return attr{name} = args[0];
      }
      catch (final RuntimeException e) {
        if (e instanceof Err)
          throw e;
        else
          throw new Err(e.toString());
      }
    }
    catch (final Err e) {
      e.add(lineno, fs, this, "setattr#{name}");
      throw e;
    }
  }


"""
