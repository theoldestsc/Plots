# 1) Проверить количество скобок (и правильность их порядка)
# 2) Проверить правильность введенных операторов
# 3) Проверить кейсы по типу coscos (но можно *cos)
# 4) Убрать математические операторы с начала и конца строки
# 5) Найти самую глубокую точку
#
#
# equation =  '50+70*(20+60)+sin(x+2)+tg(2*x)'
#

#TODO: Не пересчитывать при каждой итерации остальное уравнение,
# 1) Если в блоке нет X - посчитать
# 2) Заменить в строке
# 3) Проанализировать математические функции вне скобок, выполнить действия по приоритету


from queue import LifoQueue
import re, math, numpy
# import matplotlib.pyplot as plt


# If you add any, don't forget to also add them to prioritized operators and lambdas
FUNCTIONS = ['acos',
             'asin',
             'atan',
             'sqrt',
             'sin',
             'cos',
             'tg',
             'log'
             ]
OPERATORS = ['*', '^', '/', '+', '-']


def areBracketsClosed(equation):
    brackets = LifoQueue()
    for symbol in equation:
        if symbol == '(':
            brackets.put('(')
        if symbol == ')':
            brackets.get()
        if symbol == '[':
            brackets.put('[')
        if symbol == ']':
            brackets.get()

    if brackets.qsize() != 0:
        return False
    else:
        return True


def isEquationCorrect(equation):
    numbers = [str(x) for x in range(0,10)]
    functions = [str(x)+'(' for x in FUNCTIONS]
    allowedSymbols = functions + OPERATORS + ['x', '(', ')', '.','[',']'] + numbers

    while True:
        for symbol in allowedSymbols:
                equation = equation.replace(symbol, '')
                continue

        # If some garbage left in the equation, then we should return False
        if len(equation) != 0:
            return False
        else:
            return True



def noDuplicatesInEquation(equation):
    strOperators = ''.join(OPERATORS)
    regexOperators = re.compile((r'''[{0}][{1}]'''.format(strOperators, strOperators)))
    if regexOperators.search(equation):
        return False

    for firstFunction in FUNCTIONS:
        for secondFunction in FUNCTIONS:
            regexOperators = re.compile(r'''({0}{1})|({0}[{2}])'''.format(firstFunction, secondFunction, strOperators))
            if regexOperators.search(equation):
                return False

    return True


def isEquationEndAndStartClean(equation):
    for operator in OPERATORS:
        if equation.startswith(operator) and operator != '-':
            return False
        if equation.endswith(operator):
            return False

    return True


def checkEquation(equation):
    if not areBracketsClosed(equation):
        return False, "Brackets are't closed"
    if not isEquationCorrect(equation):
        return False, "Equation is't correct"
    if not noDuplicatesInEquation(equation):
        return False, "There is duplicates in equation(Maybe sinsin,coscos etc...)"
    if not isEquationEndAndStartClean(equation):
        return False, "Your Equation start or end with operator"

    return True, "Okay"


def findMaxDepth(equation):
    brackets = []
    maxDepth = 0
    maxDepthIndex = 0
    closeBracketIndex = len(equation)
    foundMax = False

    for i in range(len(equation)):
        if equation[i] == '(':
            brackets.append('(')
            if (len(brackets) > maxDepth):
                maxDepth = len(brackets)
                maxDepthIndex = i
                foundMax = True

        if equation[i] == ')':
            if foundMax == True:
                closeBracketIndex = i

            brackets.pop()
            foundMax = False

    return maxDepthIndex, closeBracketIndex


def getOperatorValue(expression):
    result = {
        '*' : (lambda left, right : left * right),
        '/': (lambda left, right: left / right),
        '+': (lambda left, right: left + right),
        '-': (lambda left, right: left - right),
        '^': (lambda left, right: left ** right),
    }

    for operator in OPERATORS:
        if expression.find(operator) != -1:
            #regexOperator = re.compile(r'''(-)?\d+([.]\d+)?(e-\d+)?(\{0})(-)?\d+([.]\d+)?(e-\d+)?'''.format(operator))
            #numbers = regexOperator.search(expression).group().split(operator,1)
            #print(numbers[::-1])
            i_1End = 0
            for symbol in expression:
                if symbol == operator and i_1End != 0:
                    break
                else:
                    i_1End+=1
            try:
                #return result[operator](float(numbers[0]), float(numbers[1])),""
                return  result[operator](float(expression[:i_1End]),
                                         float(expression[len(expression)-(len(expression)-i_1End-1)
                                                          :len(expression)])),""
            except ZeroDivisionError:
                return 0,"Вы делите на 0, чего делать нельзя"
            except OverflowError:
                return 0,"Слишком большое значение"



def getFunctionValue(expression):
    result = {
        'cos' : (lambda number : math.cos(number)),
        'sin' : (lambda number : math.sin(number)),
        'tg' : (lambda number : math.tan(number)),
        'acos':(lambda number : math.acos(number)),
        'asin': (lambda number: math.asin(number)),
        'atan': (lambda number: math.atan(number)),
        'sqrt': (lambda number: math.sqrt(number)),

        'log':(lambda number,base:math.log(number,base))
    }

    for function in FUNCTIONS:
        if expression.find(function) != -1:
            if function!='log':
                try:
                    return result[function](float(expression[len(function) : len(expression)])),""
                except ValueError:
                    return 0,"Ваш диапазон не удовлетворяет ОДЗ функции "
            else:
                try:
                    indexfirst = expression.find('[').__index__()
                    indexsecond = expression.find(']').__index__()
                    return result[function](float(expression[len(function): indexfirst]),
                float(expression[indexfirst+1:indexsecond])),""
                except ValueError:
                    return 0,"Ваш диапазон не удовлетворяет ОДЗ функции "


def calculateOperator(block):
    for function in FUNCTIONS:
            regexFunction = re.compile(r'''{0}(-)?\d+([.]\d+)(\[\d+([.]\d+)?\])?'''.format(function, ''.join(OPERATORS)))
            reFindFunc = regexFunction.search(block)
            if reFindFunc != None:
                value, error = getFunctionValue(regexFunction.search(block).group())
                if error=="":
                    return block.replace(reFindFunc.group(),
                                 str(value)),""
                else:
                    return block.replace(reFindFunc.group(),
                                         str(value)), error

    operators = {'+' : 3,
                 '-' : 3,
                 '*' : 2,
                 '/' : 2,
                 '^' : 1}

    maxPriority = 10
    symbol = ''

    if block.find('+-') != -1:
        block = block.replace('+-', '-')
    if block.find('--') != -1:
        block = block.replace('--','+')

    for i in range(len(block)):
        for operator in operators.keys():
            if block[i] == operator:
                if maxPriority >= operators[block[i]] and i!=0:
                    symbol = block[i]
                    maxPriority = operators[symbol]

    regexOperator = re.compile(r'''(-)?\d+([.]\d+)?(e-\d+)?\{0}(-)?\d+([.]\d+)?(e-\d+)?'''.format(symbol))
    regexOperatorFound = regexOperator.search(block)
    if regexOperatorFound!=None:
        value,error = getOperatorValue(regexOperator.search(block).group())
        return block.replace(regexOperatorFound.group(),
                                str(value)),error
    else:
        error = "Значения, которые вы хотите посчитать, слишком малы"
        return block.replace("",
                             ""), error




def calculateBlock(equation, maxDepthIndex, closeBracketIndex):
    block = equation[maxDepthIndex : closeBracketIndex+1]
    while True:
        if not type(block) == float:
            try:
                return float(block.strip('()')),""
            except ValueError:
                value, error = calculateOperator(block)
                if error=="":
                    block = block.replace(equation[maxDepthIndex : closeBracketIndex+1], str(value))
                    maxDepthIndex, closeBracketIndex = findMaxDepth(block)
                    if block[0] == '(' and block[len(block)-1] == ')':
                        equation = block.strip('()')
                    if equation.find('(') == -1:
                        equation = block
                else:
                    return str(block),error
                    #maxDepthIndex, closeBracketIndex = findMaxDepth(block)



def calculate(equation):
    while True:
        try:

            maxDepthIndex, closeBracketIndex = findMaxDepth(equation)
            blockToChange = equation[maxDepthIndex : closeBracketIndex+1]
            newBlock,error = calculateBlock(equation, maxDepthIndex, closeBracketIndex)
            equation = equation.replace(blockToChange, str(newBlock))
            if error!="":
                return 0,error+ " " + str(newBlock)
            return float(equation),""
        except ValueError:
            continue

def formatString(equation):
    equation = re.sub('pi', f'{math.pi}', equation)
    equation = re.sub('e', f'{math.e}', equation)


    return equation

def mainMathParse(equation, xrange=0, xrange2=5,step = 0.1):
    equation = formatString(equation)

    correct, value = checkEquation(equation)

    error = ""
    if correct:
        points = []
        if(xrange2>0 and xrange > 0):
            num_values = step*100*(xrange2-xrange)
        else:
            num_values = step * 100 * (math.fabs(xrange2) + math.fabs(xrange))
        for i in numpy.linspace(xrange, xrange2, int(num_values)):
            # print(points,i)
            x = equation.replace('x', str(i))
            value,error = calculate(x)
            # print(value , i)
            if error == "":
                points.append(value)
            else:
                return [],error
        return points, error
    else:
        return [1, 2, 3, 4, 5], value

#print(mainMathParse("2^x",-20,0))
#print(mainMathParse("sin(x)+2*x+3*6+cos(x)",-5,5))
# print(mainMathParse("(2*x+(3*6*x^2))+sin(x)"))
# print(log(x*e)[x])
print(mainMathParse("sin(x)+2*atan(x^2+4*x+sin(6*x^2-sin(x)^3))",-1,1,0.1))