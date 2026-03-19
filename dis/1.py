def inverse_cascade(n):
    """
    >>> inverse_cascade(1234)
    1
    12
    123
    1234
    123
    12
    1
    """
    grow(n)
    print(n)
    shrink(n)
    return None
def f_then_g(f,g,n):
    if n:
        f(n)
        g(n)
grow=lambda n: f_then_g(grow,print,n//10)
shrink=lambda n: f_then_g(print,shrink,n//10)

def recursion(n):
    if n<=1:
        return n
    else:
        return recursion(n-1)+recursion(n-2)

def index(keys,values,match):
          """Return a dictionary from keys k to a list of values v for which
          match(k,y) is a true value.
          >>> index([7,9,11],range(30,50),lambda k,v: v%k==0)
          {7:[35,42,49],9:[36,45],11: [33,44]}
          """
          return {k: [v for v in values if match (k,v)] for k in keys}
