# ADVANCED ***************************************************************************
# content = assignment
#
# deliver = .zip file with only .py, jpg or links
#           Use clear folder and module names.
#
# date    = 2021-11-07
# email   = alexanderrichtertd@gmail.com
#************************************************************************************

"""
CUBE CLASS

1. CREATE an abstract class "Cube"
   with a variabale name and the functions: translate(x, y, z), rotate(x, y, z), scale(x, y, z) and color(R, G, B)
   All functions print out and store the data in the cube (translate, rotate, scale and color)

2. CREATE 3 cube objects with different names (use __init__(name)).

3. ADD the function print_status() which prints all the variables in a spreadsheet.

4. ADD the function update_transform(ttype, value).
   ttype can be "translate", "rotate" and "scale" while value is a list of 3 floats: e.g. [1.2, 2.4 ,3.7]
   This function should trigger either the translate, rotate or scale function.

   BONUS: Can you do it without ifs?

5. CREATE a parent class "Object" which has a name, translate, rotate and scale.
   Use Object as the parent for your cube class.
   Update the cube class to not repeat the content of Object.

NOTE: Upload only the final result.


"""
