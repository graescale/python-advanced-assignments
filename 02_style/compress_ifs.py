# STYLE ***************************************************************************
# content = assignment (Python Advanced)
#
# deliver = .zip file with only .py, jpg or links
#           Use clear folder and module names.
#
# date    = 2021-03-07
# email   = alexanderrichtertd@gmail.com
#**********************************************************************************


# COMMENT --------------------------------------------------
# Not optimal
def set_color(ctrlList, color):

    color_overrides = {1:4, 2:13, 3:25, 4:17, 5:17, 6:15, 7:6, 8:16}

    for ctrlName in ctrlList:
       mc.setAttr(ctrlName + 'Shape.overrideColor', color_overrides[color])



# EXAMPLE
# set_color(['circle','circle1'], 8)
