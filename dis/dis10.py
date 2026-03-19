class Pair:
    "A Scheme list is a Pair in which rest is a Pair or nil."
    def __init__(self, first, rest):
        self.first = first
        self.rest = rest

""" >>> Pair('+', Pair(Pair('*', Pair(3, Pair(4, nil))), Pair(5, nil)))
    (+ (* 3 4) 5)
    >>> Pair('+', Pair(1, Pair(Pair('*', Pair(2, Pair(3, nil))), nil)))
    (+ 1 (* 2 3))
    >>> Pair('and', Pair(Pair('<', Pair(1, Pair(0, nil))), Pair(Pair('/', Pair(1, Pair(0, nil))), nil)))
    (and (< 1 0) (/ 1 0))
    >>> 
"""
def print_evals(expr):
        """Print the expressions that are evaluated while evaluating expr.

        expr: a Scheme expression containing only (, ), +, *, and numbers.

        >>> nested_expr = Pair('+', Pair(Pair('*', Pair(3, Pair(4, nil))), Pair(5, nil)))
        >>> print_evals(nested_expr)
        (+ (* 3 4) 5)
        +
        (* 3 4)
        *
        3
        4
        5
        >>> print_evals(Pair('*', Pair(6, Pair(7, Pair(nested_expr, Pair(8, nil))))))
        (* 6 7 (+ (* 3 4) 5) 8)
        *
        6
        7
        (+ (* 3 4) 5)
        +
        (* 3 4)
        *
        3
        4
        5
        8
        """
        if not isinstance(expr, Pair):
            print(expr)
        else:
            print(expr)
            while expr is not nil:
                print_evals(expr.first)
                expr = expr.rest