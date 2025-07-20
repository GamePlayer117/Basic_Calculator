#Hello, reader(s)! This here is a command-line calculator coded with python. Its name is 
#'Basic Calculator', and as its name says, it supports the 4 basic arithmetic operations : 
#addition, subtraction, multiplication, and division. It also comes with a few special 
#commands to do some cool stuff.

#==The first step here would be to import anything that we will use later on.==

#Here, we will import the isnan, isinf, and copysign functions from the math module
#and the sleep function from the time module.
from math import isnan, isinf, copysign
from time import sleep

#==The next step would be defining the variables that we will use later in the program.==

#The 'max_decimals' variable here is used to set the
#maximum amount of decimal places a decimal can have.
max_decimals = 3

#These 2 variables here are lists that are used for history saving.
#They will be cleared automatically once the program ends.
results = list()
equations = list()

#This variable (or constant actually) here is a dictionary that is used to be displayed in
#the program. It contains the names of the commands and their respective descriptions.
COMMANDS = {'done': 'Ends calculator usage. '
                    'Type it at any prompt to use.',
            'show calculation history': 'Shows the history of calculations. '
                                        'Type it at any prompt to use.',
            'use previous result': 'Uses the previous calculation result as a '
                                    'number for the current calculation operation. '
                                    'Type it at any number prompt to use.',
            'use result from equation #n': 'Uses the result from a past equation , referenced by '
                                            'its entry number (n) in the calculation history, '
                                            'as a number for the current calculation operation. '
                                            'Type it at any number prompt to use.',
            'clear calculation history': 'Clears the history of calculations. '
                                            'Type it at any prompt to use.',
            'set max decimal places to : n': 'Sets the maximum amount of decimal places '
                                                'a decimal can have. With n as a whole number, '
                                                'lowest is 1 and highest is 5. The default '
                                                'amount at the very start is 3. '
                                                'Type it at any prompt to use.',
            'show help guide': 'Shows some help guides if you are having some trouble. '
                                'Type it at any prompt to use.',
            'show commands list': 'Shows the list of all usable commands. '
                                    'Type it at any prompt to use.'}

#This variable (or constant) is a list that contains
#help guides to be displayed to the user.
HELP_GUIDES = ["Make sure to type numbers correctly (don't type '1 4' (with space)"
                ", but '14' (without space)).",
                "Make sure to type commands correctly (don't type 'doone', but type 'done' "
                "(casing and extra spaces/tabs are ignored here)).",
                "You should type only one number or command per prompt (don't type 'done, "
                "show commands list' at once, or '14 15' (this one counts as a mistyped number)).",
                "If you want to include thousand separators or enter decimal numbers, "
                "use ',' as the thousand separator (like '1,000') "
                "and '.' as the decimal point (like '0.5').",
                "Don't type negative numbers with brackets (don't type (-1)), "
                "they will automatically get brackets when they're displayed to you."]

#The 'commands_list' variable here is used to store the dictionary keys (the commands themselves)
#of the 'COMMANDS' dictionary into a list. For the commands that need variables to be filled, we
#will modify the them to have only the command part intact. No more changes will be done to the
#list after this point, so we will assign the list to a variable with the same name but in all
#uppercase letters to show that it is a constant and this constant will be the one used instead.
commands_list = list(COMMANDS.keys())
commands_list[3] = 'use result from equation #'
commands_list[5] = 'set max decimal places to :'
COMMANDS_LIST = commands_list

#==The step after that one would be defining the functions that will be used later in the program.==

#==The first 6 functions defined here are the helper functions.
#They help with program effiency and user experience.==

#The 'confirm_number' function is used to check whether one or all values are valid numbers.
def confirm_number(*values_to_test):
    for value in values_to_test:
        if '_' in str(value):
            return False
        try:
            float(value)
        except ValueError:
            return False
    return True

#The 'confirm_representable' function is used to check whether a value is representable.
def confirm_representable(value_to_test):
    if isnan(value_to_test):
        return False, 'is unrepresentable as a number!'
    elif isinf(value_to_test):
        if copysign(1, value_to_test) == -1:
            return False, 'is too small to be represented!'
        else:
            return False, 'is too large to be represented!'
    else:
        return True, 'is representable!'

#The 'confirm_valid_thousand_format' function is used to check whether the thousand format is valid
def confirm_valid_thousand_format(*values_to_test):
    for value in values_to_test:
        value = str(value).strip()
        if ',' not in value:
            continue
        if '.' in value:
            value = value.split('.')[0]
        comparer_value = value.replace(',', '')
        if value != format(int(comparer_value), ','):
            return False
    return True

#The 'format_number' function is used to format the looks of one or more numbers.
def format_number(*numbers_to_format):
    formatted_numbers = list()
    for number in numbers_to_format:
        format_value = ',.' + str(max_decimals) + 'f'
        formatted_number = format(float(number), format_value).rstrip('0').rstrip('.')
        if formatted_number.startswith('-'):
            formatted_number = '(' + formatted_number + ')'
        formatted_numbers.append(formatted_number)
    return formatted_numbers

#The 'replace_character' function is used to replace a specific
#character with a new one on one or more string values.
def replace_character(*values_to_format, old_character, new_character):
    formatted_values = list()
    for value in values_to_format:
        formatted_value = value.replace(old_character, new_character)
        formatted_values.append(formatted_value)
    return formatted_values

#The 'yes_no_question' function is used to create a question with just yes or no as the answer
def yes_no_question(question, response_if_yes, response_if_no, prefix_on_yes='', prefix_on_no='', default_answer='no'):
    answer = input(question).lower().strip()
    if answer == 'yes':
        if prefix_on_yes != '':
            response_if_yes = prefix_on_yes + ' ' + response_if_yes
        return 'yes', response_if_yes
    elif answer == 'no':
        if prefix_on_no != '':
            response_if_no = prefix_on_no + ' ' + response_if_no
        return 'no', response_if_no
    else:
        if default_answer == 'yes':
            return 'yes', 'Taken as a "yes". ' + response_if_yes
        else:
            return 'no', 'Taken as a "no". ' + response_if_no

#==The next 4 functions are the arithmetic functions. They each
#perform one of the 4 basic arithmetic operations mentioned above.==

#The 'addition' function performs addition with 2 numbers.
def addition(first_addend, second_addend):
    number_test = confirm_number(first_addend, second_addend)
    if number_test == True:
        total = float(first_addend) + float(second_addend)
        return total
    else:
        return 'Error! Mistyped or non-number, or mistyped command entered! Try again!'

#The 'subtraction' function performs subtraction with 2 numbers.
def subtraction(minuend, subtrahend):
    number_test = confirm_number(minuend, subtrahend)
    if number_test == True:
        difference = float(minuend) - float(subtrahend)
        return difference
    else:
        return 'Error! Mistyped or non-number, or mistyped command entered! Try again!'

#The 'multiplication' function performs multiplication with 2 numbers.
def multiplication(multiplicand, multiplier):
    number_test = confirm_number(multiplicand, multiplier)
    if number_test == True:
        product = float(multiplicand) * float(multiplier)
        return product
    else:
        return 'Error! Mistyped or non-number, or mistyped command entered! Try again!'

#The 'division' function performs division with 2 numbers.
def division(dividend, divisor):
    number_test = confirm_number(dividend, divisor)
    if number_test == True:
        try:
            quotient = float(dividend) / float(divisor)
        except ZeroDivisionError:
            return "Error! Can't divide by zero! Try again!"
        else:
            return quotient
    else:
        return 'Error! Mistyped or non-number, or mistyped command entered! Try again!'

#==The next 8 functions are the command functions. They are used to 
#do the mechanics of the special commands in the 'commands' dictionary 
#as their descriptions state.==

#The 'done' function does the mechanics of the 'done' command.
def done():
    question_1 = 'End calculator usage? This action is irreversible (Yes/No).'
    response_1 = 'Thank you for using this basic calculator!'
    response_2 = 'Enjoy using this basic calculator then.'
    prefix = 'Alright.'
    answer_1, response_a = yes_no_question(question_1, response_1, response_2, prefix_on_no=prefix)
    if answer_1 == 'yes':
        if not len(equations) == 0:
            question_2 = 'Show final calculation history? ' + str(len(equations)) + ' equation(s) exist (Yes/No).'
            answer_2, response_b = yes_no_question(question_2, response_1, response_1, prefix_on_no=prefix, default_answer='yes')
            if answer_2 == 'yes':
                if 'Taken as a "yes". ' in response_b:
                    print('Taken as a "yes".')
                    response_b = response_b.replace('Taken as a "yes". ', '')
                show_calculation_history()
            print(response_b)
        else:
            print(response_a)
        return 'break'
    else:
        print(response_a)
        return 'continue'

#The 'show_commands_list' function does the mechanics of the 'show commands list' command.
def show_commands_list():
    print('Commands list:')
    for command, info in COMMANDS.items():
        print('-', command + ':\n', info)

#The 'show_calculation_history' function does the
#mechanics of the 'show calculation history' command.
def show_calculation_history():
    entry_number = 0
    if not len(equations) == 0:
        print('Calculation history:')
        for equation in equations:
            entry_number += 1
            print(str(entry_number) + '.', equation)
    else:
        print('Calculation history is empty!')

#The 'clear_calculation_history' function does the
#mechanics of the 'clear calculation history' command.
def clear_calculation_history():
    if not len(results) == 0 and not len(equations) == 0:
        question_1 = 'Clear history? This action is irreversible (Yes/No).'
        response_1 = 'Calculation history cleared.'
        response_2 = 'Calculation history uncleared.'
        answer, response = yes_no_question(question_1, response_1, response_2)
        if answer == 'yes':
            results.clear()
            equations.clear()
        print(response)
    else:
        print('Calculation history is already empty!')

#The 'set_max_decimals' function does the mechanics of the 'set max decimal places to : n' command.
def set_max_decimals(user_input):
    global max_decimals
    specified_number = user_input.split(':', 1)[1]
    try:
        new_max_decimals = int(format_number(specified_number)[0])
    except ValueError:
        print('Max decimal places must be a correctly typed whole number!')
    else:
        if new_max_decimals >= 1 and new_max_decimals <= 5:
            if new_max_decimals != max_decimals:
                max_decimals = new_max_decimals
                print('Max decimal places set to ' + str(max_decimals) + '. '
                        + 'Now, all decimals in calculations past this point will have at most '
                        + str(max_decimals) + ' decimal places when displayed. '
                        + 'All decimals in calculations before this point are unaffected.')
            else:
                print('Max decimal places is already set to', max_decimals)
        else:
            print('Max decimal places must be in a range of 1-5!')

#The 'show_help_guide' function does the mechanics of the 'show help guides' command.
def show_help_guides():
    print('Help:')
    for help_line in HELP_GUIDES:
        print('-', help_line)

#The 'use_previous_result' function does the mechanics of the 'use previous result' command.
def use_previous_result():
    if not len(results) == 0:
        previous_result = results[-1]
        return previous_result
    else:
        return 'No previous results exist!'

#The 'use_specific_past_result' function does the
#mechanics of the 'use result from equation #n' command.
def use_specific_past_result(user_input):
    if not len(equations) == 0:
        specified_number = user_input.split('#', 1)[1]
        try:
            index_num = int(format_number(specified_number)[0]) 
        except ValueError:
            return 'Equation entry number must be a correctly typed whole number!'
        else:
            if index_num <= len(equations) and index_num > 0:
                chosen_equation = equations[index_num - 1]
                equation_result = chosen_equation.split('=')[1]
                return equation_result
            else:
                return 'Equation entry number out of bounds!'
    else:
        return 'No equations exist!'

#==The next 3 functions are the last ones to be defined. They are the
#dispatcher functions that call a specific function based on a condition.==

#The 'calculate' function does the main calculating job. 
#Its worker functions are the 4 arithmetic functions.
def calculate(operand1, operator, operand2):
    operator = operator.strip()
    if operator == '+':
        calculation_result = addition(operand1, operand2)
    elif operator == '-':
        calculation_result = subtraction(operand1, operand2)
    elif operator == '×' or operator == '*':
        calculation_result = multiplication(operand1, operand2)
    elif operator == '÷' or operator == '/':
        calculation_result = division(operand1, operand2)
    else:
        calculation_result = 'Error! Invalid arithmetic operator, or mistyped or invalid command entered! Try again!'
    return calculation_result

#The 'check_commands' function checks if a command was entered and then
#calls the function that handles the mechanics of that command.
#Its worker functions are the first 6 command functions defined.
def check_commands(user_input):
    user_input = ' '.join(user_input.lower().split())
    if user_input == COMMANDS_LIST[0]:
        loop_code = done()
        return loop_code    
    elif user_input == COMMANDS_LIST[1]:
        show_calculation_history()
        return 'continue'
    elif user_input == COMMANDS_LIST[4]:
        clear_calculation_history()
        return 'continue'
    elif user_input.startswith(COMMANDS_LIST[5]):
        set_max_decimals(user_input)
        return 'continue'
    elif user_input == COMMANDS_LIST[6]:
        show_help_guide()
        return 'continue'
    elif user_input == COMMANDS_LIST[7]:
        show_commands_list()
        return 'continue'

#The 'determine_number' function determines which number will be used for
#calculation depending on user input, whether to use user inputted numbers or a past
#calculation result. Its worker functions are the last 2 command functions defined.
def determine_number(*user_inputs):
    determined_numbers = list()
    for user_input in user_inputs:
        user_input = ' '.join(user_input.lower().split())
        if user_input == COMMANDS_LIST[2]:
            determined_number = use_previous_result()
        elif user_input.startswith(COMMANDS_LIST[3]):
            determined_number = use_specific_past_result(user_input)
        else:
            determined_number = user_input
        determined_numbers.append(determined_number)
    return determined_numbers

#==The final step before the main loop is
#to print some instructions towards the user.==

print('Welcome. Enter two numbers and an arithmetic operator to get calculation results.\n')
print('Type these commands at any prompt : "done" (to exit the calculator), "help" '
        '(if you are having trouble), "show commands list" (to view '
        'the list of all usable commands).\n(Note: Command word(s) must be typed exactly and '
        'only one command or number should be typed per prompt!)\n')
print('Performable operations and usable operators: addition(+), subtraction(-), '
        'multiplication(× or *), and division(÷ or /).\n')

#==Now its finally time to go into the main loop after all the preparations are done.==

#The loop was made to an infinite loop with an exit-at-any-prompt system so the user can
#use the calculator for as long as he/she wants and stop whenever he/she wants to.
while True:
    #This part here is the input collection part. 
    #It collects 2 numbers and an arithmetic operator.
    first_number = input('Enter the first number:')
    commands_check = check_commands(first_number)
    if commands_check == 'break':
        break
    elif commands_check == 'continue':
        continue

    operator = input('Enter the arithmetic operator:')
    commands_check = check_commands(operator)
    if commands_check == 'break':
        break
    elif commands_check == 'continue':
        continue
    
    second_number = input('Enter the second number:')    
    commands_check = check_commands(second_number)
    if commands_check == 'break':
        break
    elif commands_check == 'continue':
        continue

    #After 2 numbers and an operator are collected, we'll print a message that shows
    #that the calculator is calculating the result.
    print('Calculating...')

    #User inputted brackets are meant to be invalid here, so we will check for any user inputted
    #brackets before doing any calculation. The sleep function will be used here to give a short
    #delay before displaying the error message if there were user inputted brackets, otherwise
    #It will display immediately after the 'Calculating...' message is printed. The others outputs
    #already have delays because they have to go through a lot before getting displayed.
    if '(' in first_number or ')' in first_number or '(' in second_number or ')' in second_number:
        sleep(1.5)
        print('Error! Mistyped or non-number, or mistyped command entered! Try again!')
        continue

    #This next part here is where the calculation happens. It determines what numbers will be used
    #for calculation and does either calculating the result or giving out an error message.
    first_number, second_number = determine_number(first_number, second_number)

    past_result_error_codes = ['No previous results exist!', 'Equation entry number must be a correctly typed whole number!', 
                                'Equation entry number out of bounds!', 'No equations exist!']
    
    if first_number not in past_result_error_codes and second_number not in past_result_error_codes:
        first_number, second_number = replace_character(first_number, second_number, old_character='(', new_character='')
        first_number, second_number = replace_character(first_number, second_number, old_character=')', new_character='')
        if ',' in first_number or ',' in second_number:
            valid_thousand_format_test = confirm_valid_thousand_format(first_number, second_number)
            if valid_thousand_format_test == True:
                first_number, second_number = replace_character(first_number, second_number, old_character=',', new_character='')
                result = calculate(first_number, operator, second_number)
            else:
                result = 'Error! Mistyped or non-number, or mistyped command entered! Try again!'
        else:
            result = calculate(first_number, operator, second_number)
    else:
        number_position = 1
        for error_code in [first_number, second_number]:
            if error_code in past_result_error_codes:
                if number_position == 1:
                    position = 'first number'
                else:
                    position = 'second number'
                result = 'Error at the ' + position + '! ' + error_code + ' Try again!'
                break
            number_position += 1

    #This final part here is to decide how the 'calculation result' will be displayed
    #and whether to save stuff into the history lists we've seen earlier.
    number_test = confirm_number(result)
    if number_test == True:
        representable_test, warning_message = confirm_representable(result)
        if representable_test == True:
            first_number, second_number, result = format_number(first_number, second_number, result)
            print('Result:', result)
            results.append(result)
            operator = operator.strip()
            if operator == '*':
                operator = '×'
            elif operator == '/':
                operator = '÷'
            equation = first_number + ' ' + operator + ' ' + second_number + ' = ' + result
            equations.append(equation)
        else:
            print('Result', warning_message)
    else:
        print(result)
