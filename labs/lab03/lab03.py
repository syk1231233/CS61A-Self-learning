SOURCE_FILE = __file__


def double_eights(n):
    """Returns whether or not n has two digits in row that
    are the number 8.

    >>> double_eights(1288)
    True
    >>> double_eights(880)
    True
    >>> double_eights(538835)
    True
    >>> double_eights(284682)
    False
    >>> double_eights(588138)
    True
    >>> double_eights(78)
    False
    >>> # ban iteration
    >>> from construct_check import check
    >>> check(SOURCE_FILE, 'double_eights', ['While', 'For'])
    True
    """
    "*** YOUR CODE HERE ***"
    state=False
    if state:
        return True
    elif n<10:
        return False
    else:
        if n%10==8 and (n//10)%10==8:
            state=True
            return True
        else:
            return double_eights(n//10)


def gcd(a, b):
    """Returns the greatest common divisor of a and b.
    Should be implemented using recursion.

    >>> gcd(34, 19)
    1
    >>> gcd(39, 91)
    13
    >>> gcd(20, 30)
    10
    >>> gcd(40, 40)
    40
    """
    "*** YOUR CODE HERE ***"
    if a==b:
        return a
    elif a<b:
        if b%a==0:
            return a
        else:
            return gcd(a,b%a)
    else:
        if a%b==0:
            return b
        else:
            return gcd(b,a%b)


def pascal(row, column):
    """Returns the value of the item in Pascal's Triangle
    whose position is specified by row and column.
    >>> pascal(0, 0)    # The top left (the point of the triangle)
    1
    >>> pascal(0, 5)	# Empty entry; outside of Pascal's Triangle
    0
    >>> pascal(3, 2)	# Row 3 (1 3 3 1), Column 2
    3
    >>> pascal(4, 2)     # Row 4 (1 4 6 4 1), Column 2
    6
    """
    "*** YOUR CODE HERE ***"
    if column==0 :
        return 1
    elif row<column:
        return 0
    elif row==0 and column==0:
        return 1
    else:
        return pascal(row-1,column-1)+pascal(row-1,column)


def paths(m, n):
    """Return the number of paths from one corner of an
    M by N grid to the opposite corner.

    >>> paths(2, 2)
    2
    >>> paths(5, 7)
    210
    >>> paths(117, 1)
    1
    >>> paths(1, 157)
    1
    """
    "*** YOUR CODE HERE ***"
    if m==1:
        return 1
    elif n==1:
        return 1
    else:
        return paths(m-1,n)+paths(m,n-1)
