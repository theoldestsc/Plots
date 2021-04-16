# 1) Проверить количество скобок (и правильность их порядка)
# 2) Проверить правильность введенных операторов
# 3) Проверить кейсы по типу coscos (но можно *cos)
# 4) Убрать математические операторы с начала и конца строки
# 5) Найти самую глубокую точку
#
#
# equation =  '50+70*(20+60)+sin(x+2)+tg(2*x)'
#2/x*tg(sin(x)*log(x)[e])

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
             'sin',
             'cos',
             'tg',
             'sqrt',
             'log'
             ]
OPERATORS = ['*', '^', '/', '+', '-']

def logFunctionIsCorrect(equation):
    pattern = re.compile(r'''log\((-)?\d+([.]\d+)?\)\[(-)?\d+([.]\d+)?\]''')
    isThereLog = re.findall("log",equation)
    if isThereLog != None:
        size = len(isThereLog)
        result = pattern.findall(equation)
        size_r = len(result)
        if size_r == size:
            return True
        else:
            return False
    else:
        return True


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
    if len(equation) == 0:
        return False, "Your equation is empty"
    if not logFunctionIsCorrect(equation):
        return False, "Log function incorrect, try log(number)[base]"
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
            i_1End = 0
            for symbol in expression:
                if symbol == operator and i_1End != 0:
                    if (expression[i_1End - 1] != 'e'):
                        break
                    else:
                        i_1End += 1
                else:
                    i_1End += 1
            try:
                # return result[operator](float(numbers[0]), float(numbers[1])),""
                number_1 = float(expression[:i_1End])
                number_2 =  float(expression[len(expression) - (len(expression) - i_1End - 1)
                                                  :len(expression)])
                returned_value = result[operator](number_1,number_2)
                if number_1 < 0 and returned_value > 0:
                    returned_value = "+"+str(returned_value)
                return returned_value, ""
            except ZeroDivisionError:
                return numpy.nan, ""#,"Вы делите на 0, чего делать нельзя"
            except OverflowError:
                return numpy.nan,"Слишком большое значение"



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
                    return numpy.nan,"" #,"Ваш диапазон не удовлетворяет ОДЗ функции "
            else:
                try:
                    indexfirst = expression.find('[').__index__()
                    indexsecond = expression.find(']').__index__()
                    return result[function](float(expression[len(function): indexfirst]),
                float(expression[indexfirst+1:indexsecond])),""
                except ValueError:
                    return numpy.nan,"" #,"Ваш диапазон не удовлетворяет ОДЗ функции "


def calculateOperator(block):
    for function in FUNCTIONS:
            regexFunction = re.compile(r'''{0}(-)?\d+([.]\d+)(\[\d+([.]\d+)?\])?'''.format(function, ''.join(OPERATORS)))
            reFindFunc = regexFunction.search(block)
            if reFindFunc != None:
                value, error = getFunctionValue(regexFunction.search(block).group())
                if value == numpy.nan:
                    return numpy.nan,error
                elif error=="":
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

    #if block.find('+-') != -1:
     #   block = block.replace('+-', '-')
    #if block.find('--') != -1:
     #   block = block.replace('--','+')

    i=0
    while i < len(block):
        if block[i] == 'e':
            i+=2
        if block[i].isdigit() != True:
            for operator in operators.keys():
                if block[i] == operator:
                    if maxPriority >= operators[block[i]] and i!=0:
                        symbol = block[i]
                        maxPriority = operators[symbol]
                        i+=1
            i+=1
        else:
            i+=1

   # regexOperator = re.compile(r'''(-)?\d+([.]\d+)?(e-\d+)?[*/\-+^](-)?\d+([.]\d+)?(e-\d+)?''')
    regexOperator = re.compile(r'''(-)?\d+([.]\d+)?(e-\d+)?\{0}(-)?\d+([.]\d+)?(e-\d+)?'''.format(symbol))
    regexOperatorFound = regexOperator.search(block)
    if regexOperatorFound!=None: # HERE ############################ Не тот приоритет считает
        value,error = getOperatorValue(regexOperator.search(block).group())
        if value == numpy.nan:
            return numpy.nan
        return block.replace(regexOperatorFound.group(),
                                str(value)),error
    else:
        # error = "Значения, которые вы хотите посчитать, слишком малы"
        return block.replace("",
                             ""), ""




def calculateBlock(equation, maxDepthIndex, closeBracketIndex):
    block = equation[maxDepthIndex : closeBracketIndex+1]
    while True:
        if block.find('+-') != -1:
            block = block.replace('+-', '-')
        elif block.find('--') != -1:
            block = block.replace('--', '+')
        elif block.find('*+') != -1:
            block = block.replace('*+', '*')
        elif block.find('/+') != -1:
            block = block.replace('/+', '/')
        if not type(block) == float:
            try:
                return float(block.strip('()')),""
            except ValueError:
                value, error = calculateOperator(block)
                if value.find("nan")!=-1:
                    return numpy.nan,"Выколатая точка"
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
            if newBlock == numpy.nan:
                return numpy.nan,""
            equation = equation.replace(blockToChange, str(newBlock))
            if error!="":
                return numpy.nan,error+ " " + str(newBlock)
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
        x_points = []
        if(xrange2>0 and xrange > 0):
            num_values = step*100*(xrange2-xrange)
        else:
            if xrange < 0 and xrange2 <0:
                num_values = step * 100 * (math.fabs(xrange) - math.fabs(xrange2))
            else:
                num_values = step * 100 * (math.fabs(xrange2) + math.fabs(xrange))# проблема с шагом
        for i in numpy.linspace(xrange, xrange2, int(num_values)):
            x = equation.replace('x', str(i))
            value,error = calculate(x)
            if error=="":
                x_points.append(i)
                points.append(value)
            else:
                continue
                #return [],error
        return points, x_points, "" #error
    else:
        return [1, 2, 3, 4, 5],[1, 2, 3, 4, 5], value

# print(mainMathParse("2^x",-20,0))
# print(mainMathParse("sin(x)+2*x+3*6+cos(x)",-10,10,0.1))
# print(mainMathParse("(2*x+(3*6*x^2))+sin(x)",-10,10,0.1))
# print(mainMathParse("log(x*e)[x]",-10,10,0.1))
# print(mainMathParse("2/x*tg(sin(x))", -10,10,0.1)) # проблема с шагом
# print(mainMathParse("sin(x)/cos(2*x)*asin(x)",-10,10,0.1))
# print(mainMathParse("3^(x/(1-x^2))"),-1,1,0.1)
# print(mainMathParse("sin(x)+2*atan(x^2+4*x+sin(6*x^2-sin(x)^3))",-1,1,0.1))
# print(mainMathParse("sin(x)+2*atan(x^2+4*x+sin(6*x^2-sin(x)^3))",-1,1,0.1))
# print(mainMathParse("log(x^2+4x+16+sin(x))[e]",-4,-3,0.1))
# print(mainMathParse("sin(x^2+4*x+16)*tg(x)*sin(x)",-10,10,0.1))
# print(mainMathParse("sin(x)+2*atan(x^2+4*x+sin(6*x^2-sin(x)^3))",-0.11009174311926628,1,0.1))



#print(mainMathParse("sqrt(log(8.21321)[2]*2*sin(x)*cos(2*x+3/8*tg(x/2))+2*x)/log(4)[2]*2*log(4)[e]"))
#print(mainMathParse("log(8)[e]"))