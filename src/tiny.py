# Tiny succinct objects
# (c) Tim Menzies, 2021 MIT License, https://opensource.org/licenses/MIT.

class o:
  "Containers with get/set methods."
  def __init__(i, **d): i.__dict__.update(**d)
  def __repr__(i): return str(
      {k: (v.__name__ + "()" if callable(v) else v)
       for k, v in sorted(i.__dict__.items()) if k[0] != "_"})

def _method(i, f):
  "Methods are lambda bodies with an added pointer to a container."
  return lambda *l, **d: f(i, *l, **d)

def of(i, **methods):
  "Add methods to a simple containers."
  for k, f in methods.items():
    i.__dict__[k] = _method(i, f)
  return i


if __name__ == "__main__":
  def Fred(a=2):
    def a(x): return x + 10
    def lt(i, j): return i.a < j.a
    def say(i): return f"{i.a} ==> {i.b}"
    return of(o(a=10, b=20), say=say, less=lt)
  f = Fred(200)
  print(f.less(Fred()), f.say())
