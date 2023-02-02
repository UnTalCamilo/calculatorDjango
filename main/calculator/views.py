from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView

# Create your views here.
class IndexView(TemplateView):
    template_name = "calculator/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = [
            ["C", "CE", "^", "/"],
            ['7', '8','9', "*"],
            ['4', '5', '6', "-"],
            ['1', '2', '3', "+"],
            ['0', ".", "="],
        ]
        return context






class SimpleView(TemplateView):
    template_name = "calculator/simple_cal.html"

    def get(self, request, *args, **kwargs):
        result = 0
        try:
            number1 = float(request.GET['first_number'])
            number2 = float(request.GET['second_number'])
            operator = request.GET['operator']
            
            if operator == '+':
                result = number1 + number2
            elif operator == '-':
                result = number1 - number2
            elif operator == '*':
                result = number1 * number2
            elif operator == '/':
                result = number1 / number2
        except:
            result = "Error"
        
        print(result)
        return render(request, self.template_name, {
            "result" : str(result) 
        })
    




# logic for calculator

def calculate(request):
    body = request.body.decode("utf-8")
    try:
        infixStr = infix(body)
        prefixStr = prefix(infixStr)
        result = arithmetic_expression_evaluation(prefixStr)
        print(result)
        return JsonResponse({ "result" : result})
    except:
        return JsonResponse({ "result" : "Error"})
        
def infix(string):
    cad = ""
    cont = 0
    while cont < len(string):
        if string[cont] in ("+", "-", "*", "/", "^"):
            if string[cont] == "-":
                if cont > 0 and string[cont-1] in ("*","/"):
                    try:
                        float(string[cont+1])
                        cad += f"{string[cont]}{string[cont+1]}"
                        cont += 2
                    except:
                        print("a")
                elif len(cad) == 0:
                    cad += f"{string[cont]}{string[cont+1]}"
                    cont += 2
            if cont < len(string):
                cad += f" {string[cont]} "
        else :
            cad += string[cont]
        cont += 1
    return cad

def prefix(string):
    cad = []
    infix_rev = string.split(" ")
    infix_rev = infix_rev[::-1]
    operators = []
    for i in infix_rev:
        if i in ("+","-","*","/","^"):
            if len(operators) == 0:
                operators.append(i)
            elif get_priority(operators[-1]) == 1 and get_priority(i) == 1:
                cad.append(operators.pop())
                operators.append(i)
            elif get_priority(operators[-1]) >= get_priority(i):
                operators.append(i)
            else:
                while len(operators) > 0 and get_priority(operators[-1]) <= get_priority(i):
                    cad.append(operators.pop())
                operators.append(i)
        else :
            cad.append(i)
            

    while len(operators) > 0:
        cad.append(operators.pop())
    
    return cad

def arithmetic_expression_evaluation(array):
    numbers = []
    for i in array:
        try:
            numbers.append(float(i))
        except:
            if i == "+":
                numbers.append(numbers.pop() + numbers.pop())
            elif i == "-":
                numbers.append(numbers.pop() - numbers.pop())
            elif i == "*":
                numbers.append(numbers.pop() * numbers.pop())
            elif i == "/":
                numbers.append(numbers.pop() / numbers.pop())
            elif i == "^":
                numbers.append(numbers.pop() ** numbers.pop())
            elif i == "%":
                numbers.append(numbers.pop() % numbers.pop())
    return numbers.pop()


def get_priority(data):
    if data in ("+,-"):
        return 3
    elif data in ("*,/"):
        return 2
    elif data in ("^"):
        return 1
    