# TODO:
#   Should mismatched brackets work?
#   Catch bracketing errors earlier on
#   Possible division of 0 / sqrt of negatives / bad use of logs etc would crash system, sending lots of error messages
#   Symbols that haven't been defined
#   fullEvaluate("e^6pi + e^7") doesn't work because of order of operations
#   Sort out negativeness

import re
import math

class Function(object):
    '''
    A simple class to represent mathematical functions.
    '''

    def __init__(self, symbol, applyFunction):
        '''
        Functions have two attributes:
            Symbol is a string representation of the function.
            ApplyFunction is a function that actually carries out the function
        '''        
        self.symbol = symbol
        self.applyFunction = applyFunction

class Symbol(object):
    '''
    A simple class to represent mathematical symbols.
    '''

    def __init__(self, symbol, value):
        '''
        Functions have two attributes:
            Symbol is a string representation of the symbol.
            Value is a float that approximately represents the value of the symbol.
        '''        
        self.symbol = symbol
        self.value = value

def basicEvaluate(exp):
    '''
    Evaluates an expression with only the simple brackets and no extra symbols or functions, for testing.
    '''
    return evaluateExpression(exp, ["("], [")"], [], [])

def fullEvaluate(exp):
    '''
    Takes an expression as a string, and returns an equivalent float.
    '''
    
    exp = prepareExpression(exp)

    # Sets up necessary brackets, functions and symbols.
    openBrackets = ["(", "[", "{"]
    closeBrackets = [")", "]", "}"]
    
    sqrt = Function("sqrt", math.sqrt)
    cos = Function("cos", math.cos)
    sin = Function("sin", math.sin)
    tan = Function("tan", math.tan)
    functions = [sqrt, cos, sin, tan]

    pi = Symbol("pi", math.pi)
    e = Symbol("e", math.e)
    symbols = [pi, e]
    
    return evaluateExpression(exp, openBrackets, closeBrackets, functions, symbols)

def prepareExpression(exp):
    '''
    Prepares an expression for the evaluateExpression function by making the format easier and less ambiguous.
    '''

    # Puts a multiply symbol between two characters
    def addMultiply(s):
        s = s.group()
        return s[0] + "*" + s[1]
    
    # Remove spaces
    exp = exp.replace(" ", "")

    # Add some * symbols for implicit multiplication
    exp = exp.replace(")(", ")*(")      
    exp = re.sub(r"[0-9][a-wyzA-Z(]", addMultiply, exp) # Exclude x, as x is used for multiplying

    return exp
    

def evaluateExpression(exp, openBrackets, closeBrackets, functions, symbols):
    '''
    This function takes a mathematical expression as a string, and returns the equivalent floating point number.
    It also takes a list of openBrackets, closeBrackets, functions and symbols that may be used in the expression.
    '''

    # The program attempts the following simplifications in order:
        # Check if the expression is now a valid float or symbol
        # Remove excess brackets
        # Process +/- signs outside of brackets
        # Process functions at the start of expressions
        # Process times/divide signs outside of brackets
        # Process ^ powers

    # Check if the expression is now a valid float
    if validFloat(exp):
        return float(exp)

    # Check if the expression is now a valid symbol
    sym = validSymbol(exp, symbols)
    if sym != None:
        return sym.value

    # Remove excess brackets
    if removableBrackets(exp, openBrackets, closeBrackets):
        return evaluateExpression(exp[1:-1], openBrackets, closeBrackets, functions, symbols)

    # Process +/- signs outside of brackets
    plusMinusSplit, operators = splitOutsideBrackets(exp, openBrackets, closeBrackets, ["+", "-"])
    if len(plusMinusSplit) != 1:
        add = lambda x, y: x + y
        minus = lambda x, y: x - y
        return applyOperators(plusMinusSplit, operators, openBrackets, closeBrackets, functions, symbols, ["+", "-"], [add, minus], 0)

    # Process functions at the start of expressions
    startingFunction = startsWithFunction(exp, functions)
    if startingFunction != None:
        return applyFunction(exp, startingFunction, openBrackets, closeBrackets, functions, symbols)

    # Process times/divide signs outside of brackets
    timesDivideSplit, operators = splitOutsideBrackets(exp, openBrackets, closeBrackets, ["*","x", "/"])
    if len(timesDivideSplit) != 1:
        times = lambda x, y: x * y
        divide = lambda x, y: x / y
        return applyOperators(timesDivideSplit, operators, openBrackets, closeBrackets, functions, symbols, ["*", "x", "/"], [times, times, divide], 1)

    # Process ^ powers
    powerSplit, operators = splitOutsideBrackets(exp, openBrackets, closeBrackets, ["^"])
    if len(powerSplit) != 1:
        return applyOperators(powerSplit, operators, openBrackets, closeBrackets, functions, symbols, ["^"], [pow], 1)

    raise

def validFloat(exp):
    '''
    Checks if an expression is now just a number, by converting it and seeing if it fails.
    '''

    try:
        float(exp)
        return True
    except ValueError:
        return False
        

def validSymbol(exp, symbols):
    '''
    Checks if an expression is now a predefined symbol
    It takes an expression as a string, and returns a symbol (or None).
    '''

    # Check against each symbol to see if the expression is one of them.
    for sym in symbols:
        if sym.symbol == exp:
            return sym

    # If the symbol isn't found, return None
    return None

def removableBrackets(exp, openBrackets, closeBrackets):
    '''
    This function takes an expression and a list of possible open and close brackets and returns a boolean stating whether there are removable brackets.
    '''
    
    if not (exp[0] in openBrackets and exp[-1] in closeBrackets):
        # There isn't a bracket at the beginning or at the end, so it can't be surrounded.
        return False

    # bracketCount counts the net (open brackets are + and close brackets are -) number of brackets encountered so far.
    bracketCount = 1
    
    for character in exp[1:-1]:
        
        if character in openBrackets:
            bracketCount += 1
            
        elif character in closeBrackets:
            bracketCount -= 1
            if bracketCount == 0:
                # You are out of all the brackets, so it isn't surrounded.
                return False

    # The expression never got out of all the brackets, so it is surrounded.
    return True

def splitOutsideBrackets(exp, openBrackets, closeBrackets, splittingOperators):
    '''
    This function takes a mathematical expression as a string and a list of opening brackets, closing brackets and operators to be split by.
    It splits the expression into a list of strings split by any of these operators out of all brackets.
    It returns two lists: the split expressions and the operators joining them.
    '''

    # operands is a list of the split expressions.
    operands = []

    # operators is a list of the operators the expression is split by.
    operators = []

    # lastExpression collects the expression since a relevant operator was last found.
    lastExpression = ""

    # bracketCount counts the net (open brackets are positive and close brackets are negative) number of brackets encountered so far.
    bracketCount = 0

    for symbol in exp:
        if symbol in openBrackets:
            bracketCount += 1

        elif symbol in closeBrackets:
            bracketCount -= 1

        # A new if is used (rather than elif) as the else should happen in the first two cases.
        if bracketCount == 0 and symbol in splittingOperators:
            # A plus/minus has been found, so split the expression.
            operands.append(lastExpression)
            operators.append(symbol)
            lastExpression = ""

        else:
            # Add the symbol to the end of lastExpression and keep going.
            lastExpression += symbol

    # Add the final operand to the list.
    operands.append(lastExpression)
    
    return operands, operators

def startsWithFunction(exp, functions):
    '''
    Checks whether the expression starts with any of the functions.
    '''
    
    # Check each function to see if it starts with that
    for fun in functions:
        if exp.startswith(fun.symbol):
            return fun

    # If it doesn't start with a function
    return None
    

def applyOperators(operands, operators, openBrackets, closeBrackets, functions, symbols, operatorSymbols, operatorFunctions, identity):
    '''
    This function takes a list of operands and operators, all information needed for evaluating (openBrackets, closeBrackets, functions and symbols)
    and a list of operatorSymbols to apply and their corresponding operatorFunctions. It returns a float made from evaluating them.
    '''

    # Check for an empty starting string (a leading minus)
    if operands[0] == "":
        answer = identity
    else: 
        # Evaluate the first operand and set this to the answer.
        answer = evaluateExpression(operands[0], openBrackets, closeBrackets, functions, symbols)

    # Pair the remaining operands and operators.
    for exp, sym in zip(operands[1:], operators):
        # Evaluate the next operand
        new = evaluateExpression(exp, openBrackets, closeBrackets, functions, symbols)

        # Apply the function at the same position in operatorFunctions as the symbol is in operatorSymbols
        answer = operatorFunctions[operatorSymbols.index(sym)](answer, new)

    return answer

def applyFunction(exp, function, openBrackets, closeBrackets, functions, symbols):
    '''
    This function takes an expression as a string, a function that the expression starts with and all the other information needed for evaluating
    and returns the float equivalent to the expression.
    '''

    # Remove the first bit of exp, as this is the function name.
    remainingExpression = exp[len(function.symbol):]

    # If the function argument is surrounded by brackets, apply the function to these brackets only.
    if remainingExpression[0] in openBrackets:

        # bracketCount counts the brackets so far, to make sure you are in the outer layer of brackets.
        bracketCount = 0

        # functionalAppliedTo accumulates the expression
        functionAppliedTo = ""

        # Go through each symbol, changing bracketCount appropriately.
        for symbolCount in range(len(remainingExpression)):
            
            symbol = remainingExpression[symbolCount]
            functionAppliedTo += symbol
            
            if symbol in openBrackets:
                bracketCount += 1
                
            elif symbol in closeBrackets:
                bracketCount -= 1

                # If the bracket you just exited, is the outer layer, then you need to evaluate.
                if bracketCount == 0:
                    # newExp evaluates the function to make a simpler expression
                    newExp = str(function.applyFunction(evaluateExpression(functionAppliedTo, openBrackets, closeBrackets, functions, symbols))) + \
                             remainingExpression[symbolCount + 1:]

                    # Now evaluate newExp, and return that.
                    return evaluateExpression(newExp, openBrackets, closeBrackets, functions, symbols)
                
    else:
        # If not surrounded by brackets, the function is applied to the rest of the expression.
        return function.applyFunction(evaluateExpression(remainingExpression, openBrackets, closeBrackets, functions, symbols))