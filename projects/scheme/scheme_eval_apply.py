import sys

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms

##############
# Eval/Apply #
##############

def scheme_eval(expr, env, _=None): # Optional third argument is ignored
    # expr is the Pair env is the environment
    """Evaluate Scheme expression EXPR in Frame ENV.
    
    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms
    if scheme_symbolp(expr):            # the type of input is str which can be found in scheme
        return env.lookup(expr)         # find the value of name( str-> real value )
    elif self_evaluating(expr):
        return expr

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr))) # forwardly raise(引起) a Error-> it is a check
    first, rest = expr.first, expr.rest
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS:   # if a given combination is spcilal form
        return scheme_forms.SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 3
        """1.Evaluate the operator (which should evaluate to a Procedure instance  see scheme_classes.py for Procedure definitions).
           2.Evaluate all of the operands and collect the results (the argument values) in a Scheme list.
           3.Return the result of calling scheme_apply on this Procedure and these argument values.
        """
        proc = scheme_eval(first, env)
        args = rest.map(lambda operand:scheme_eval(operand,env))
        return scheme_apply(proc, args, env)
              
        
        # END PROBLEM 3

def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    validate_procedure(procedure)
    if not isinstance(env, Frame):    # check the environment weather is env to avoid apply wrong feature
       assert False, "Not a Frame: {}".format(env)
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        """ Problem
            1. We do not konw how many arguement must be passed into the Built_in_Procedure
            2. We do not konw wether the procedure need the agrument env 
            3. 
            Solve:
            1. 
        """
        arg=[]
        cur=args
        # translate args from Pair into a list
        while(isinstance(cur,Pair)):
            arg+=[cur.first]
            cur=cur.rest
        f=procedure.py_func
        if procedure.need_env:
            arg+=[env]
        # END PROBLEM 2
        try:
            # BEGIN PROBLEM 2
            return f( *arg )
            # END PROBLEM 2
        except TypeError as err:
            raise SchemeError('incorrect number of arguments: {0}'.format(procedure))
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        env=procedure.env.make_child_frame(procedure.formals,args)
        return eval_all(procedure.body,env)
        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        env=env.make_child_frame(procedure.formals,args)
        return eval_all(procedure.body,env)
        # END PROBLEM 11
    else:
        assert False, "Unexpected procedure: {}".format(procedure)

def eval_all(expressions, env):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    Frame ENV (the current environment) and return the value of the last.

    >>> eval_all(read_line("(1)"), create_global_frame())
    1
    >>> eval_all(read_line("(1 2)"), create_global_frame())
    2
    >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
    1
    >>> x
    2
    >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
    2
    """
    # BEGIN PROBLEM 6
    if expressions is nil:
        return None
    else:
        first,rest=expressions.first,expressions.rest
        while(rest is not nil):
            first=scheme_eval(first,env)
            first,rest=rest.first,rest.rest
        return scheme_eval(first,env)
    # END PROBLEM 6


################################
# Extra Credit: Tail Recursion #
################################

class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env

def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not an Unevaluated."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val

def optimize_tail_calls(unoptimized_scheme_eval):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # BEGIN OPTIONAL PROBLEM 1
        "*** YOUR CODE HERE ***"
        # END OPTIONAL PROBLEM 1
    return optimized_eval














################################################################
# Uncomment the following line to apply tail call optimization #
################################################################

# scheme_eval = optimize_tail_calls(scheme_eval)
