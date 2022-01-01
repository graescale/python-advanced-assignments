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


#*********************************************************************
# DECORATOR
def print_process(func):
    def wrapper(*args, **kwargs):
        func(arg)                  # main_function
    return wrapper


#*********************************************************************
# FUNC
@print_process
def short_sleeping(test):
    time.sleep(.1)
    print(test)

def mid_sleeping():
    time.sleep(2)

def long_sleeping():
    time.sleep(4)

short_sleeping("dads")

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
