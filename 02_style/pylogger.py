# STYLE ***************************************************************************
# content = assignment
#
# deliver = .zip file with only .py, jpg or links
#           Use clear folder and module names.
#
# date    = 2021-03-07
# email   = alexanderrichtertd@gmail.com
#************************************************************************************

# original: logging.init.py

def find_caller(self):
    """
    Find the stack frame of the caller so that we can note the source
    file name, line number and function name.
    """
    current_frame = currentframe()

    #On some versions of IronPython, currentframe() returns None if
    #IronPython isn't run with -X:Frames.

    try current_frame:
        current_frame = current_frame.f_back
    except:
        print('currentframe() is None')
    rv = "(unknown file)", 0, "(unknown function)"
    
    while hasattr(current_frame, "f_code"):
        frame_code = current_frame.f_code
        file_name = os.path.normcase(frame_code.co_filename)

        if file_name == _srcfile:
            current_frame = current_frame.f_back
        rv = (frame_code.co_filename, current_frame.f_lineno, frame_code.co_name)
        
        break
    return rv

# How can we make this code better?

