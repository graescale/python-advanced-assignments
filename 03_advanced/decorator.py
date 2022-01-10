#*********************************************************************
# content   = decorator example
# date      = 2021-11-03
#
# seminar   = Scripting for Artists {Advanced}
#
# license   = MIT
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************


import time
from datetime import datetime


#*********************************************************************
# DECORATOR
def print_process(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        
        print('\n**********')
        print('Function Name: {}'.format(func.__name__))
        print('START')

        func(args)                  # main_function

        result_time = (datetime.now() - start_time).total_seconds()
        hours, remainder = divmod(result_time, 3600)
        minutes, seconds = divmod(remainder, 60)

        print('END')
        print('ELAPSED TIME: {:02}:{:02}:{:02}'.format(int(hours),
                                int(minutes),
                                int(seconds)))                       
        print('\n**********')
    return wrapper

def confirm_process(func):
    def wrapper():
        print('\n**********')
        print('Hold up. Are you sure you want to continue?')
        
        decision = input('y/n\n')
        if decision == 'y':
            print('OK, you\'re the boss.')
            func()
        else:
            print('You didn\'t press \'y\' so we are cancelling.')
    return(wrapper)


#*********************************************************************
# FUNC
@print_process
def short_sleeping(test):
    time.sleep(1)
    print(*test)

@print_process
def mid_sleeping():
    time.sleep(2)

@print_process
def long_sleeping():
    time.sleep(4)

@confirm_process
def foo():
    print('deleting everything')

short_sleeping('dads')

foo()

#******************************************************************************************************************************************
# 0 - CONNECT decorator to all functions
#     print START and END before and after
#
# START
# main_function
# END


#*********************************************************************
# 1 - print processing time of all sleeping func
#
# END - 00:00:00


#*********************************************************************
# 2 - PRINT also the name of the function
#
# START - long_sleeping


#*********************************************************************
# 3 - create your personal decorator and function
