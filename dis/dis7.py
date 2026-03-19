def draw(hand, positions):
    """Remove and return the items at positions from hand.

    >>> hand = ['A', 'K', 'Q', 'J', 10, 9]
    >>> draw(hand, [2, 1, 4])
    ['K', 'Q', 10]
    >>> hand
    ['A', 'J', 9]
    """
    # 利用p列表中的位序提取hand中的元素，同时保留元素的相对位序
    # 提取 list(hand(p) for p in positions) 这时候提取出来的元素失去了原来的相对位置
    # 更新设计 使用迭代器，依次弹出hand中的每一个元素，如果该元素的位序在positions中那么就纳入列表 此为良算法
    return list(reversed( [hand.pop(i) for i in sorted(positions,reverse=True)]))

LOWERCASE_LETTERS = 'abcdefghijklmnopqrstuvwxyz'

class CapsLock:
    def __init__(self):
        self.pressed = 0

    def press(self):
        self.pressed += 1

class Button:
    """A button on a keyboard.

    >>> f = lambda c: print(c, end='')  # The end='' argument avoids going to a new line
    >>> k, e, y = Button('k', f), Button('e', f), Button('y', f)
    >>> s = e.press().press().press()
    eee
    >>> caps = Button.caps_lock
    >>> t = [x.press() for x in [k, e, y, caps, e, e, k, caps, e, y, e, caps, y, e, e]]
    keyEEKeyeYEE
    >>> u = Button('a', print).press().press().press()
    A
    A
    A
    """
    caps_lock = CapsLock() # Capslock的一个实例对象，通过访问他的实例属性pressed来判断当前输入的字母是否需要大写输出

    def __init__(self, letter, output):
        """ 
        i=botton('c',print) 一次输入的实例例子
        """
        assert letter in LOWERCASE_LETTERS # 限定输入只能是26个字母
        self.letter = letter
        self.output = output
        self.pressed = 0 

    def press(self):
        """Call output on letter (maybe uppercased), then return the button that was pressed."""
        self.pressed += 1
        if(self.caps_lock.pressed%2!=0):
            self.output(self.letter.upper())
        else:
            self.output(self.letter)
        return self  # 返回 Button 实例
    

class Keyboard:
    """A keyboard.

        >>> Button.caps_lock.pressed = 0  # Reset the caps_lock key
        >>> bored = Keyboard()
        >>> bored.type('hello')
        >>> bored.typed
        ['h', 'e', 'l', 'l', 'o']
        >>> bored.keys['l'].pressed
        2
        >>> Button.caps_lock.press()
        >>> bored.type('hello')
        >>> bored.typed
        ['h', 'e', 'l', 'l', 'o', 'H', 'E', 'L', 'L', 'O']
        >>> bored.keys['l'].pressed
        4
    """
    def __init__(self):
        self.typed = []
        self.keys ={key : Button(key,lambda c: None) for key in LOWERCASE_LETTERS}  # Try a dictionary comprehension!

    def type(self, word):
        """Press the button for each letter in word."""
        assert all([w in LOWERCASE_LETTERS for w in word]), 'word must be all lowercase'
        for __ in word:
            self.keys[__].press()  # 按下对应的字母
            if(self.keys[__].caps_lock.pressed%2!=0):
                self.typed+=[__.upper()]  # 记录每次按下的字母
            else:
                self.typed+=[__]  # 记录每次按下的字母





class Eye:
    """An eye.

    >>> Eye().draw()
    '0'
    >>> print(Eye(False).draw(), Eye(True).draw())
    0 -
    """
    def __init__(self, closed=False):
        self.closed = closed

    def draw(self):
        if self.closed:
            return '-'
        else:
            return '0'

class Bear:
    """A bear.

    >>> Bear().print()
    ? 0o0?
    """
    def __init__(self):
        self.nose_and_mouth = 'o'

    def next_eye(self):
        return Eye()

    def print(self):
        left, right = self.next_eye(), self.next_eye()
        print('? ' + left.draw() + self.nose_and_mouth + right.draw() + '?')

class SleepyBear(Bear):
    """A bear with closed eyes.

    >>> SleepyBear().print()
    ? -o-?
    """
    def next_eye(self):
        __=Eye()
        __.closed=True
        return __

class WinkingBear(Bear):
    """A bear whose left eye is different from its right eye.

    >>> WinkingBear().print()
    ? -o0?
    """
    def __init__(self):
        super().__init__()
        self.times=0
    def next_eye(self):
        if(self.times%2==0):
            __=Eye()
            __.closed=True
        else:
            __=Eye()
        self.times+=1
        return __