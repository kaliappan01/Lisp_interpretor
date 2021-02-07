#Lets do it
#Now

import math
import operator as op

#declaration of literals
Symbol = str              # A Scheme Symbol is implemented as a Python str
Number = (int, float)     # A Scheme Number is implemented as a Python int or float
Atom   = (Symbol, Number) # A Scheme Atom is a Symbol or Number
List   = list             # A Scheme List is implemented as a Python list
Exp    = (Atom, List)     # A Scheme expression is an Atom or List
Env    = dict             # A Scheme environment (defined below) 
                          # is a mapping of {variable: value}

def tokenize(chars : str) -> list:
    """
        takes input and adds space around parenthesis to break down the instruction 
        for interpretion
    """
    #adding space
    chars = chars.replace('(',' ( ')
    chars = chars.replace(')',' ) ')

    #breaking down the instruction into list of literals
    return chars.split()

def read_from_tokens(tokens : list) -> Exp:
    if len(tokens)==0:
        raise SyntaxError("unexpected EOF")
    token = tokens.pop(0)
    if token == '(':
        #creating list 
        L = []
        while tokens[0]!=')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)  #removing the ')' closing bracket
        return L
    elif token == ')':
        raise SyntaxError("unexpected EOF")
    else :
        return atom(token)


def atom(token :str)->Atom:
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)

def parse(program:str)->Exp:
    d = read_from_tokens(tokenize(program))
    return d


def standard_Env()->Env:
    """
    used to run the inbuilt functions and operations
    """
    l_env = Env()
    l_env.update(vars(math)) 

    l_env.update(
        {'+':op.add, '-':op.sub , '*':op.mul, '/':op.truediv,
        '<':op.lt ,'>':op.gt ,'<=':op.le, '>=':op.ge, '=':op.eq,
        'abs' : abs,
        'apply': lambda proc,args :proc(*args),
        'append' : op.add,
        'begin' :lambda *x: x[-1],
        'car' : lambda x: x[0],
        'cdr' : lambda x: x[1:],
        'cons' : lambda x,y: [x] + y,
        'eq?' : op.is_,
        'expt' : pow,
        'equal?' : op.eq,
        'list' : lambda *x: List(x),
        'list?' : lambda x: isinstance(x,List),
        'map': map,
        'max' : max,
        'min' : min,
        'not' : op.not_,
        'null?' : lambda x:x==[],
        'number?' : lambda x: isinstance(x,Number),
                'print ' : print,
        'procedure' : callable,
        'symbol?' : lambda x: isinstance(x,Symbol),
        'round'  : round
        
        })
    return l_env


def repl(prompt = "lisp>"):
    """
    Read-Evaluate-Print-Loop
    """
    while True:
        val = eval(parse(input(prompt)))
        if val is not None:
            print(schemestr(val))

def schemestr(exp):
    """
    for formatting the output
    convert python object into a scheme readable object
    """
    if isinstance(exp,List):
        return '(' + " ".join(map(schemestr,exp))+')'
    else:
        return str(exp)

class Env(dict):
    """
    An environment dictionary containing the value fo variable
    """
    def __init__(self, params = (),args = (),outer = None):
        self.update(zip(params,args))
        self.outer = outer
    def find(self,var):
        
       # find the innermost environment available
        return self if (var in self) else self.outer.find(var)

class Procedure(object):
    """
    An user-defined scheme procedure
    """
    def  __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env
    def __call__(self,*args):
        return eval(self.body, Env(self.params, args, self.env ))
global_env = standard_Env()

def eval(x ,env = global_env):
    """
    Evaluates an expression
    """
    if isinstance(x, Symbol):
        #variable reference 
        return env.find(x)[x]
    elif not isinstance(x, List):
        #constant
        return x
    op,*args = x
    if op == "quote":
        return args[0]
    elif op == "if": 
        (test, conseq, alt) = args
        exp = ( conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif op=='define':
        #definition
        (symbol, exp) = args
        env[symbol] = eval(exp, env)
    elif op=="set!":
        #assignment
        (symbol, exp) = args
        env.find(symbol)[symbol] = eval(exp, env)
    elif op == "lambda":
        #procedure
        (params, body) = args
        return Procedure(params, body, env)
    else:
        #procedure call
        proc = eval( op, env )
        args = [eval(arg, env) for arg in args]
        return proc(*args)

repl()
