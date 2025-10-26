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

            if is_add or is_change: 
                if len(args[INPUT]) != 2:
                    print("Syntax: give me name and phone")
                    return
                is_user_exists = args[INPUT][USERNAME] in args[DATABASE] 


            if is_add:
                if is_user_exists: 
                    print("Contact already exists")
                    return

            if is_change:
                if not is_user_exists:
                    print("Contact doesn't exist")
                    return

            return func(*args)
        except ValueError:
            print("Give me name and phone please.")
        except KeyError:
            print('Contact not found')
        except IndexError:
            print('Index error')
        except Exception as err_msg:
            print(err_msg)
    return inner

def modify_database(args):
    name, phone = args[INPUT] 
    args[DATABASE][name] = phone

@input_error
def add_contact(*args):
    modify_database(args)
    print("Contact added")

@input_error
def change_contact(*args):
    modify_database(args)
    print("Contact changed")
    
@input_error
def show_phone(*args):
    print(args[DATABASE][args[INPUT][USERNAME]])
        
@input_error
def show_all(*args):
    for name, phone in args[DATABASE].items():
        print(f'{name}: {phone}')

def exit_(*args):
    print("Good bye!")
    sys.exit()

def invalid_cmd(*args):
    print("Invalid command")
    return

def parse_input(user_input):
    cmd, *args = user_input.split()
    return cmd.casefold(), *args

def hello(*args):
    print('How can I help you?')


def main():
    contacts = {'test255': 255} #database
    
    # bot's functions dict
    run = {'add': add_contact, 'change': change_contact,
            'phone':show_phone, 'all': show_all, 'exit': exit_,
            'error': invalid_cmd, 'close': exit_, 'hello': hello
    }

    while True:

        # waits for input, parses command and arguments, and runs function
        cmd, *args = parse_input(input("Hello Friend! #: "))
        if cmd in run:
            run[cmd](args, contacts)
        else:
            invalid_cmd()

if __name__ == '__main__':
    main()