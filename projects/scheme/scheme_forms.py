from scheme_eval_apply import *
from scheme_utils import *
from scheme_classes import *
from scheme_builtins import *

#################
# Special Forms #
#################

# Each of the following do_xxx_form functions takes the cdr of a special form as
# its first argument---a Scheme list representing a special form without the
# initial identifying symbol (if, lambda, quote, ...). Its second argument is
# the environment in which the form is to be evaluated.

def do_define_form(expressions, env):
    """Evaluate a define form.
    >>> env = create_global_frame()
    >>> do_define_form(read_line("(x 2)"), env) # evaluating (define x 2)
    'x'
    >>> scheme_eval("x", env)
    2
    >>> do_define_form(read_line("(x (+ 2 8))"), env) # evaluating (define x (+ 2 8))
    'x'
    >>> scheme_eval("x", env)
    10
    >>> # problem 10
    >>> env = create_global_frame()
    >>> do_define_form(read_line("((f x) (+ x 2))"), env) # evaluating (define (f x) (+ x 8))
    'f'
    >>> scheme_eval(read_line("(f 3)"), env)
    5
    """
    validate_form(expressions, 2) # Checks that expressions is a list of length at least 2
    signature = expressions.first
    if scheme_symbolp(signature):
        # assigning a name to a value e.g. (define x (+ 1 2))
        validate_form(expressions, 2, 2) # Checks that expressions is a list of length exactly 2
        # BEGIN PROBLEM 4
        value=scheme_eval(expressions.rest.first,env)
        env.define(signature,value)
        return signature
        # END PROBLEM 4
    elif isinstance(signature, Pair) and scheme_symbolp(signature.first):
        # defining a named procedure e.g. (define (f x y) (+ x y))
        # signature is (f x y) the rest is ((+ x y),nil)
        # we are making a procedure
        # BEGIN PROBLEM 10
        # 1. Using the given variables signature and expressions, find the defined function's name (symbol), formals, and body.
        formals=signature.rest
        signature=signature.first
        body=expressions.rest
        # 2. Create a LambdaProcedure instance using the formals and body. (You could call do_lambda_form to do this.)
        lam=do_lambda_form(Pair(formals,body),env)
        # 3. Bind the symbol to this new LambdaProcedure instance.
        env.define(signature,lam)
        # 4. Return the symbol that was bound.
        return signature
        # END PROBLEM 10
    else:
        bad_signature = signature.first if isinstance(signature, Pair) else signature
        raise SchemeError('non-symbol: {0}'.format(bad_signature))

def do_quote_form(expressions, env):
    """Evaluate a quote form.

    >>> env = create_global_frame()
    >>> do_quote_form(read_line("((+ x 2))"), env) # evaluating (quote (+ x 2))
    Pair('+', Pair('x', Pair(2, nil)))
    """
    validate_form(expressions, 1, 1)
    # BEGIN PROBLEM 5
    # structure Pair(A,nil)
    return expressions.first
    # END PROBLEM 5

def do_begin_form(expressions, env):
    """Evaluate a begin form.

    >>> env = create_global_frame()
    >>> x = do_begin_form(read_line("((print 2) 3)"), env) # evaluating (begin (print 2) 3)
    2
    >>> x
    3
    """
    validate_form(expressions, 1)
    return eval_all(expressions, env)

def do_lambda_form(expressions, env):
    """Evaluate a lambda form.

    >>> env = create_global_frame()
    >>> do_lambda_form(read_line("((x) (+ x 2))"), env) # evaluating (lambda (x) (+ x 2))
    LambdaProcedure(Pair('x', nil), Pair(Pair('+', Pair('x', Pair(2, nil))), nil), <Global Frame>)
    """
    validate_form(expressions, 2)
    formals = expressions.first
    validate_formals(formals)
    # BEGIN PROBLEM 7
    return LambdaProcedure(formals,expressions.rest,env)
    # END PROBLEM 7

def do_if_form(expressions, env):
    """Evaluate an if form.

    >>> env = create_global_frame()
    >>> do_if_form(read_line("(#t (print 2) (print 3))"), env) # evaluating (if #t (print 2) (print 3))
    2
    >>> do_if_form(read_line("(#f (print 2) (print 3))"), env) # evaluating (if #f (print 2) (print 3))
    3
    """
    validate_form(expressions, 2, 3)
    if is_scheme_true(scheme_eval(expressions.first, env)):
        return scheme_eval(expressions.rest.first, env)
    elif len(expressions) == 3: # 必须是三段式遇到#f才能执行错误结果
        return scheme_eval(expressions.rest.rest.first, env)

def do_and_form(expressions, env):
    """Evaluate a (short-circuited) and form.

    >>> env = create_global_frame()
    >>> do_and_form(read_line("(#f (print 1))"), env) # evaluating (and #f (print 1))
    False
    >>> # evaluating (and (print 1) (print 2) (print 4) 3 #f)
    >>> do_and_form(read_line("((print 1) (print 2) (print 3) (print 4) 3 #f)"), env)
    1
    2
    3
    4
    False
    """
    # BEGIN PROBLEM 12
    if expressions is nil:
        return True
    cur=scheme_eval(expressions.first, env)
    while(is_scheme_true(cur)):
        if expressions.rest is nil:
            return cur
        expressions=expressions.rest
        cur=scheme_eval(expressions.first, env)
    return False
    # END PROBLEM 12

def do_or_form(expressions, env):
    """Evaluate a (short-circuited) or form.

    >>> env = create_global_frame()
    >>> do_or_form(read_line("(10 (print 1))"), env) # evaluating (or 10 (print 1))
    10
    >>> do_or_form(read_line("(#f 2 3 #t #f)"), env) # evaluating (or #f 2 3 #t #f)
    2
    >>> # evaluating (or (begin (print 1) #f) (begin (print 2) #f) 6 (begin (print 3) 7))
    >>> do_or_form(read_line("((begin (print 1) #f) (begin (print 2) #f) 6 (begin (print 3) 7))"), env)
    1
    2
    6
    """
    # BEGIN PROBLEM 12
    if expressions is nil:
        return False
    cur=scheme_eval(expressions.first, env)
    while(is_scheme_false(cur)):
        if expressions.rest is nil:
            return False
        expressions=expressions.rest
        cur=scheme_eval(expressions.first, env)
    return cur
    # END PROBLEM 12

def do_cond_form(expressions, env):
    """Evaluate a cond form.

    >>> do_cond_form(read_line("((#f (print 2)) (#t 3))"), create_global_frame())
    3
    """
    while expressions is not nil:
        clause = expressions.first
        validate_form(clause, 1)
        if clause.first == 'else':
            test = True
            if expressions.rest != nil:
                raise SchemeError('else must be last')
        else:
            test = scheme_eval(clause.first, env)
        if is_scheme_true(test):
            # BEGIN PROBLEM 13
            if clause.rest is not nil:
                return eval_all(clause.rest,env)
            return test
            # END PROBLEM 13
        expressions = expressions.rest

def do_let_form(expressions, env):
    """Evaluate a let form.

    >>> env = create_global_frame()
    >>> do_let_form(read_line("(((x 2) (y 3)) (+ x y))"), env)
    5
    """
    validate_form(expressions, 2)
    let_env = make_let_frame(expressions.first, env)
    return eval_all(expressions.rest, let_env)


def make_let_frame(bindings, env):
    """Create a child frame of Frame ENV that contains the definitions given in
    BINDINGS. The Scheme list BINDINGS must have the form of a proper bindings
    list in a let expression: each item must be a list containing a symbol
    and a Scheme expression."""
    if not scheme_listp(bindings):
        raise SchemeError('bad bindings list in let form')
    names = vals = nil
    # BEGIN PROBLEM 14 
    """关键问题 1 bindings中存在不规范赋值情况 1 多变量赋值       在最后完整提取出来参数列表后调用validate_formals函数来验证
                                          2 单一变量赋多个值  一开始存储表达式的时候就对表达式进行validate_form 长度规范
               2 评估表达式的时候我们调用的是scheme_eval函数 我们需要向其传入env环境 但是此时env环境的参数列表中没有我们最新定义的参数 我们需要新建一个子帧额外包含我们定义的参数环境来评估我们的表达式
       关键要点 1 因为let赋值先后存在覆盖问题 我们构建的链表必须和bindings中参数出现顺序是一致的
    
    if bindings is not nil: # 本次let进行了赋值操作 bindings不为空
        aim=bindings.first # 本组评估对象 aim的结构为 参数 表达式 
        next=bindings.rest
        #关键要点 1 为保证顺序 我们采取尾插法构建链表,并进行初始化链表
        name=names=Pair(aim.first,nil)
        if aim.rest is nil: # 不允许空赋值
            raise SchemeError
        validate_form(aim,2,2) # 关键问题 2 确保表达式最终只提供一个值 避免多重赋值
        val=vals=Pair(aim.rest.first,nil)
        while True:
            if next is nil: # 提取结束
                break
            else:
                aim=next.first
                name.rest=Pair(aim.first,nil)
                if aim.rest is nil: # 不允许空赋值
                    raise SchemeError
                validate_form(aim,2,2)
                val.rest=Pair(aim.rest.first,nil)
                if next.rest is nil:
                    break
                else:
                    next=next.rest
        #关键问题 1 1 检验参数列表是否合规
        validate_formals(names)
        #关键问题 2 子帧评估表达式
        name=names.rest
        none=nones=Pair(None,nil)
        while name is not nil:
            none.rest=Pair(None,nil)
            name=name.rest
        env_tem=env.make_child_frame(names,nones)
        name=names
        val=vals
        while(val is not nil):
            val.first=scheme_eval(val.first,env)
            env_tem.define(name.first,val.first)
            name=name.rest
            val=val.rest
        return env_tem"""
    names = []
    vals = []
    seen = set()
    curr = bindings
    while curr is not nil:
        binding = curr.first
        validate_form(binding, 2, 2)
        var = binding.first
        if var in seen:
            raise SchemeError
        if not scheme_symbolp(var):
            raise SchemeError('non-symbol: {0}'.format(var))
        seen.add(var)
        names.append(var)
        expr = binding.rest.first
        val = scheme_eval(expr, env)  # 用外层环境求值
        vals.append(val)
        curr = curr.rest
     # 构造链表
    def list_to_scheme_list(lst):
        result = nil
        for item in reversed(lst):
            result = Pair(item, result)
        return result
    return env.make_child_frame(list_to_scheme_list(names), list_to_scheme_list(vals))
    # END PROBLEM 14
def do_quasiquote_form(expressions, env):
    """Evaluate a quasiquote form with parameters EXPRESSIONS in
    Frame ENV."""
    def quasiquote_item(val, env, level):
        """Evaluate Scheme expression VAL that is nested at depth LEVEL in
        a quasiquote form in Frame ENV."""
        if not scheme_pairp(val):
            return val
        if val.first == 'unquote':
            level -= 1
            if level == 0:
                expressions = val.rest
                validate_form(expressions, 1, 1)
                return scheme_eval(expressions.first, env)
        elif val.first == 'quasiquote':
            level += 1

        return val.map(lambda elem: quasiquote_item(elem, env, level))

    validate_form(expressions, 1, 1)
    return quasiquote_item(expressions.first, env, 1)

def do_unquote(expressions, env):
    raise SchemeError('unquote outside of quasiquote')


#################
# Dynamic Scope #
#################

def do_mu_form(expressions, env):
    """Evaluate a mu form."""
    validate_form(expressions, 2)
    formals = expressions.first
    validate_formals(formals)
    # BEGIN PROBLEM 11
    return MuProcedure(formals,expressions.rest)
    # END PROBLEM 11



SPECIAL_FORMS = {
    'and': do_and_form,
    'begin': do_begin_form,
    'cond': do_cond_form,
    'define': do_define_form,
    'if': do_if_form,
    'lambda': do_lambda_form,
    'let': do_let_form,
    'or': do_or_form,
    'quote': do_quote_form,
    'quasiquote': do_quasiquote_form,
    'unquote': do_unquote,
    'mu': do_mu_form,
}