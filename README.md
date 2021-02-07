
# LISP INTERPRETOR USING PYTHON 

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Working](#working)
## General info
> 
A simple and quick way to know about the working of an interpretor using python.

LISP is an family of High level programming languages.Scheme is one of them.
Scheme is made up of 5 keywords and 8 syntactic forms.

Interpretor works in two steps :
- PARSING 
- EXECUTION
<hr>

## Technologies
Project is created with:
* PYTHON 3.8

## Working
1.**Parsing**\  
    - *tokenize*  
  takes input and adds space around parenthesis to break down the instruction   
        for interpretion  
    -*read_from_tokens*  
       checks for EOF errors and also helps to process tokens  
    -*atom*  
  helps to classify tokens  
    -*parse*  
  runs the above functions   
  
2.**Execution**  
    -*eval*  
  Evaluates the instructions and performs the corresponding operation  
    -*schemestr*  
  for formatting the output  
    convert python object into a scheme readable object  
    -*repl*\
  Read-Evaluate-Print-Loop  
## Environment  
>
### standard_Env 
contains all the in-built functions of scheme , thus provides the environment
### Env
An environment dictionary containing the value for variable

<hr>

Thank you for reading 
