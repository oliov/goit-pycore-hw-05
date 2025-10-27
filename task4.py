import sys
from functools import wraps

INPUT = 0
USERNAME = 0
DATABASE = 1


def input_error(func):
    @wraps(func)
    def inner(*args):
        try:
            # saves current function name to adapt checks
            func_name = func.__name__
            is_add = func_name is add_contact.__name__
            is_change = func_name is change_contact.__name__
            is_parser = func_name is parse_input.__name__
            if is_parser:
                if len(args[INPUT]) == 0:
                    return 'error'

            if is_add or is_change: 
                if len(args[INPUT]) != 2:
                    return "Syntax: give me name and phone"
                is_user_exists = args[INPUT][USERNAME] in args[DATABASE] 

            if is_add:
                if is_user_exists: 
                    return "Contact already exists"

            if is_change:
                if not is_user_exists:
                    return "Contact doesn't exist"

            return func(*args)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return 'Contact not found'
        except IndexError:
            return 'Index error'
        except Exception as err_msg:
            return err_msg
    return inner

def modify_database(args):
    name, phone = args[INPUT] 
    args[DATABASE][name] = phone

@input_error
def add_contact(*args):
    modify_database(args)
    return "Contact added"

@input_error
def change_contact(*args):
    modify_database(args)
    return "Contact changed"
    
@input_error
def show_phone(*args):
    return args[DATABASE][args[INPUT][USERNAME]]
        
@input_error
def show_all(*args):
    for name, phone in args[DATABASE].items():
        return f'{name}: {phone}'

def invalid_cmd(*args):
    return "Invalid command"

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    return cmd.casefold(), *args

def hello(*args):
    return 'How can I help you?'

def main():
    contacts = {'test255': 255} #database
    
    # bot's functions dict
    run = {'add': add_contact, 'change': change_contact,
            'phone':show_phone, 'all': show_all,
            'error': invalid_cmd, 'hello': hello
    }

    while True:

        # waits for input, parses command and arguments, and runs function
        cmd, *args = parse_input(input("Hello Friend! #: "))

        if cmd == 'close' or cmd == 'exit':
            print("Good bye!")
            break

        if cmd in run:
            print(run[cmd](args, contacts))

        else:
            print(invalid_cmd())

if __name__ == '__main__':
    main()