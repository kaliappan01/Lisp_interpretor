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
"""

def read_from_tokens(tokens: list) -> Exp:
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token: str) -> Atom:
    "Numbers become numbers; every other token is a symbol."
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)
"""
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

global_env = standard_Env()

def eval(x : str ,env = global_env)-> Exp:
    """
    evaluates an expression
    """
    if isinstance(x, Symbol):
        return env[x]
    elif isinstance(x, Number):
        return x
    elif x[0]=="if":
        (_, test, conseq, alt) = x
        exp = ( conseq if test else alt)
        return eval(exp, env)
    elif x[0]=='define':
        (_, var, exp) = x
        env[var] = eval(exp, eval)
    else:
        proc = eval( x[0], env )
        args = [eval(arg, env) for arg in x[1:]]
        return proc(*args)


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

repl()
