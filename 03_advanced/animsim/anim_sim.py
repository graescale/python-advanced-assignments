#*******************************************************************************
# content = Simulates hovering motion.
#
# version      = 0.4.1
# date         = 2021-12-19
# how to       => anim_sim = animSim()
#
# dependencies = Maya
#
# to dos = Restructure workflow, simplify code
# author = Grae Revell <grae.revell@gmail.com>
#*******************************************************************************

import numpy as np
import scipy.signal

import pymel.core as pm
import maya.cmds as cmds

#*******************************************************************************
# VARIABLES

ROTATION_LAYER = 'auto_rotation_layer'
TRANSLATION_LAYER = 'auto_translation_layer'


class Flyer:
    def __init__(self, name):
        self.name = name
        self.start_frame = ''
        self.end_frame = ''
        self.key_frames = []
        self.pos_axis_1 = []
        self.pos_axis_2 = []
        self.start_pos_axis_1 = 0
        self.start_pos_axis_2 = 0
        self.accel_axis_1 = []
        self.accel_axis_2 = []
        self.rot_axis_1 = []
        self.rot_axis_2 = []
        self.rot_axis_1_dict = {}
        self.rot_axis_2_dict = {}
        self.rot_layer_name = ROTATION_LAYER
        self.trans_layer_name = TRANSLATION_LAYER
        self.smoothness = 0
        self.parent_state = None
        self.parent_value = ''


#*******************************************************************************
# COLLECT  

    def get_scene_data(self):
        print('|get_scene_data|')
        self.start_frame = int(cmds.playbackOptions(min=True,q=True))
        self.end_frame = int(cmds.playbackOptions(max=True,q=True))


    def get_anim_data(self, attributes, autoRoll):
        """ Return dictionary of lists of keyframe values for given attributes.
        
        Args:
            attributes (list): The requested transfromation attributes
        
        Returns:
            dictionary: animation data lists
        """

        print('|get_anim_data|')
        self.create_world_space_buffer(autoRoll)
        # Make a list of the key_frames to be used later in both modes.
        self.key_frames = cmds.keyframe(self.name + '_buffer_raw',
                                        attribute=['translate', 'rotate'],
                                        query=True,
                                        timeChange=True)

        # Make a dictionary containing lists of keyframe values for each attribute.
        anim_data = {}
        for attr in attributes:
            anim_data[attr] = cmds.keyframe(self.name + '_buffer_raw',
                                            attribute='.' + attr,
                                            query=True,
                                            valueChange=True)  
        return anim_data
    

    def create_world_space_buffer(self, autoRoll):
        print('|create_world_space_buffer|')
        # Create  a buffer node.
        buffer_raw = self.name + '_buffer_raw'

        pm.createNode('transform', n = buffer_raw, ss = True)
        # Change the rotation order to zxy to prevent gimbal lock.

        cmds.setAttr(buffer_raw + '.rotateOrder', 2)
        if self.parent_state:           
            cmds.parent( buffer_raw, self.parent_value )
        else:
            print('No parent set.')

        # Constrain buffer to object, bake it, delete constraint.
        cmds.parentConstraint(self.name, buffer_raw, name='buffer_constraint')
        time_range = (self.start_frame, self.end_frame)
        if autoRoll == True:
            # Automatically add pre / post roll from the smoothness value
            time_range = (self.start_frame - self.smoothness, self.end_frame + self.smoothness)
        cmds.bakeResults(buffer_raw + '.translate', buffer_raw + '.rotate', t=time_range, sb=1)
        cmds.delete('buffer_constraint')


#*******************************************************************************
# HELPERS (MODULES?)


    def get_derivative(self, anim_data, degree, filter_data, window, order=3):
        """ Returns a list containing n degree derivative of supplied list.
        
        Args:
            anim_data (list): The data to get derivatives from.
            degree (int): The number of derivatives to calculate.
            filter_data (bool): Option to smooth the data after deriving.
            window (int): The filter window size.
            order (int): The filter polynomial order. Default 3

        Returns:
            list: The n degree derivative of anim_data
         """

        print('|get_derivative|')
        # Initialize data
        data_to_derive = anim_data
        deriv_result = []
        count = 1
        while count <= degree:
            deriv_result = np.diff(data_to_derive)        
            deriv_result = np.insert(deriv_result,0,0)
            data_to_derive = deriv_result
            count = count + 1
        if filter_data == True:
            deriv_result = scipy.signal.savgol_filter(deriv_result, window, order)            
        return deriv_result


    def get_integral(self, anim_data, degree):
        """ Returns a list containing the n degree integral of the supplied list.
        
        Args:
            anim_data (list): The data to get derivatives from.
            degree (int): The number of derivatives to calculate.

        Returns:
            list: The n degree integral of anim_data
        """

        print('|get_integral|')
        # velocity(t) - velocity(t - 1) = acceleration(t)
        # velocity(t) = acceleration(t) + velocity(t -1)
        data_to_integrate = anim_data      
        count = 1
        while count <= degree:
            #print('Getting integral of degree: '+ str(count))
            # Initialize integral_result.
            integral_result = []
            # Append the first value in data_to_integrate to integral_result's first element     
            integral_result.append(data_to_integrate[0])
            for idx, i in enumerate(data_to_integrate):
                if idx > 0:
                    integral_result.append(data_to_integrate[idx] + integral_result[idx - 1])
            count = count + 1
            data_to_integrate = integral_result
        return integral_result 


    def smooth_data(self, data, window, order):
        """ Smooths list of numbers using Savitzky–Golay filter.
        
        Args:
            data (list): The numbers to smooth.
            window (int): The smoothing window size.
            order (int): The polynomial order to use in the smoothing method.
        Returns:
            list: Smoothed data.
        """

        print('|smoothData|')
        return scipy.signal.savgol_filter(data, window, order) 

 
    def create_anim_layer(self, layer_name):
        """ Creates an animation layer
        
        Args:
            layer_name (str): The name of layer to be created

        """
        print('|create_anim_layer|')
        # Make an animation layer if it doesn't already exist.
        if not cmds.animLayer(layer_name, query=True, exists=True):
           cmds.animLayer(layer_name)
        # Add self to that animation layer.
        cmds.select(self.name)
        cmds.animLayer(layer_name, edit=True, addSelectedObjects=True)


#*******************************************************************************
# PROCESS
        

    def derive_rotation(self, axis_1, axis_2, scale, window, autoRoll, polyOrder=3 ):
        """ Derives object's rotation from its translation.
        
        Args:
            axis_1 (str): 1st translation axis
            axis_2 (str): 2nd translation axis
            scale (int): Value multiplier
            window (int): The filter window size. Default is 31
            order (int): The filter polynomial order. Default is 3

        Returns:
            None

        """

        print('|derive_rotation|')
        self.get_scene_data()
        raw_anim_data = self.get_anim_data(['translate' + axis_1, 'translate' + axis_2], autoRoll)

        # Loop to replace next block
        #axes = [axis_1, axis_2]
        #for axis in axes:
        #    raw_position + axis = raw_anim_data['translate' + axis]
        #    self.pos + axis = self.smoothData(self.raw_pos_axis_1, window, polyOrder)   

        # Should replace lines below with loop
        self.raw_pos_axis_1 = raw_anim_data['translate' + axis_1]
        self.raw_pos_axis_2 = raw_anim_data['translate' + axis_2]
        self.pos_axis_1 = self.smoothData(self.raw_pos_axis_1, window, polyOrder)
        self.pos_axis_2 = self.smoothData(self.raw_pos_axis_2, window, polyOrder)
        self.accel_axis_1 = self.get_derivative(self.pos_axis_1, 2, True, window)
        self.accel_axis_2 = self.get_derivative(self.pos_axis_2, 2, True, window)      
        self.copy_to_rotation(scale, axis_1, axis_2)
        cmds.delete(self.name + '_buffer_raw')


    def integrate_translation(self, axis_1, axis_2, scale, autoRoll):
        """ Derives object's translation from its rotation.
        
        Args:
            axis_1 (str): 1st rotation axis
            axis_2 (str): 2nd rotation axis
            scale (str): Value multiplier
        
        Returns:
            None
        """

        print('|integrate_translation|') 
        self.get_scene_data()
        raw_anim_data = self.get_anim_data(['rotate' + axis_1, 'rotate' + axis_2, 'translate' + axis_1, 'translate' + axis_2], autoRoll)
        self.rot_axis_1 = raw_anim_data['rotate' + axis_1]
        self.rot_axis_2 = raw_anim_data['rotate' + axis_2]   

        # Get the local starting position
        self.start_pos_axis_1 = cmds.getAttr( self.name + '.translate' + axis_1, time=self.start_frame - autoRoll )
        self.start_pos_axis_2 = cmds.getAttr( self.name + '.translate' + axis_2, time=self.start_frame - autoRoll )

        # Swap axes because the integral of the rotation in axis_1 is the translation in axis_2
        self.pos_axis_2 = self.get_integral(self.rot_axis_1, 2)
        self.pos_axis_1 = self.get_integral(self.rot_axis_2, 2)

        self.copy_to_translation(scale, axis_1, axis_2)
        cmds.delete(self.name + '_buffer_raw')

#*******************************************************************************
# APPLY


    def copy_to_rotation(self, scale, axis_1, axis_2):
        """ Copies acceleration values to the object's rotation on a separate layer.
        
        Args:
            scale (int): Value multiplier
            axis_1 (str): 1st translation axis
            axis_2 (str): 2nd translation axis
        
        Returns:
            None
        """

        print('|copy_to_rotation|')
        self.create_anim_layer(self.rot_layer_name)
        cmds.animLayer(self.rot_layer_name, edit=True, sel=True, prf=True)

        self.rot_axis_1 = self.accel_axis_2
        self.rot_axis_2 = self.accel_axis_1

        # Zip key_frames and rotation values lists into tuples and then into a dictionary
        self.rot_axis_1_dict = dict(zip(self.key_frames, self.rot_axis_1))
        self.rot_axis_2_dict = dict(zip(self.key_frames, self.rot_axis_2))
        for key in self.rot_axis_1_dict:
            cmds.setKeyframe(self.name, time=key, at='rotate' + axis_1, value=(self.rot_axis_1_dict[key] * scale) )
            cmds.setKeyframe(self.name, time=key, at='rotate' + axis_2, value=(self.rot_axis_2_dict[key] * -scale) )
  

    def copy_to_translation(self, scale, axis_1, axis_2):
        """ Copies generated values to the object's translation on a separate layer.
        
        Args:
            scale (int): Value multiplier
            axis_1 (str): 1st rotation axis
            axis_2 (str): 1st rotation axis
        
        Returns:
            None
        """

        print('|copy_to_translation|')
        self.create_anim_layer(self.trans_layer_name)
        cmds.animLayer(self.trans_layer_name, edit=True, sel=True, prf=True)

        # Zip key_frames and position values lists into tuples and then into a dictionary
        self.pos_axis_1_dict = dict(zip(self.key_frames, self.pos_axis_1))
        self.pos_axis_2_dict = dict(zip(self.key_frames, self.pos_axis_2))

        for key in self.pos_axis_1_dict:
            cmds.setKeyframe(self.name, animLayer=self.trans_layer_name, time=key, at='translate' + axis_1, value=(self.pos_axis_1_dict[key] / -scale + self.start_pos_axis_1) )
            cmds.setKeyframe(self.name, animLayer=self.trans_layer_name, time=key, at='translate' + axis_2, value=(self.pos_axis_2_dict[key] / scale + self.start_pos_axis_2) )



#*******************************************************************************
# UI


class AnimSim():
    
    
    def __init__(self):
    
        # class var
        self.widgets = {}
        self.planeMenu = None
        self.scale = None
        self.smoothness  = None
        self.autoPrePost = 1
        # call on the build UI method
        self.build_UI()
        self.flyer = None
        
    
    def build_UI(self):
        
        windowID = 'AnimSim_UI'
        
        if cmds.window( windowID, exists=True ):
            cmds.deleteUI( windowID )
        
        # Layouts
        self.widgets['window'] = cmds.window( windowID, title='Anim Sim', width=400, height=300)
        self.widgets['mainLayout'] = cmds.columnLayout(adjustableColumn=True) 
        
        # Initialization Frame
        self.widgets['frameLayout1'] = cmds.frameLayout(label='Initialization')
        self.widgets['rowColumnLayout1'] = cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[ (1,200), (2,200)], columnOffset=[ 1,'right', 3], columnSpacing=[ (1,10), (2,10) ])
        cmds.text(label='Select an object and click \"Initialize"')
        cmds.separator(style='none')
        self.widgets['intitButton'] = cmds.button( label='Initialize', command=self.initialize_callback)
        self.widgets['targetTextField'] = cmds.textField( text='none', editable=False)
        cmds.text(label='Parent Options')
        cmds.text(label = '')
        cmds.radioCollection()
        self.widgets['globalRadioButton'] = cmds.radioButton(label='Global')
        self.widgets['parentRadioButton'] = cmds.radioButton(label='Parent')
        self.widgets['parentButton'] = cmds.button(label='Set Parent', command=self.parent_callback)
        self.widgets['parentTextField'] = cmds.textField(text='none', editable=False)
        cmds.setParent('..')
        cmds.setParent('..')
        
        # Parameters Frame
        self.widgets['frameLayout2'] = cmds.frameLayout(label='Parameters')
        self.widgets['rowColumnLayout2'] = cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[ (1,120), (2,150) ], columnOffset=[ 1,'right', 3], columnSpacing=[ (1,10), (2,10) ])
        cmds.text(label='Motion Plane:')  
        self.planeMenu = cmds.optionMenu()
        cmds.menuItem(label='XZ')
        cmds.menuItem(label='XY')
        cmds.menuItem(label='ZY')
        cmds.text(label='Scale:')
        self.scale = cmds.intField(value=150)
        cmds.text(label='Smoothness (odd #):')
        self.smoothness = cmds.intField(value=11, maxValue=99, minValue=3)
        cmds.setParent('..')
        cmds.setParent( ..')
        
        # Build Frame
        self.widgets['frameLayout3'] = cmds.frameLayout(label='Build')
        self.widgets['cmds.rowColumnLayout3'] = cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[ (1,200), (2,200) ], columnSpacing=[ (1,10), (2,10) ])
        self.autoPrePost = cmds.checkBox(label='Auto Pre / Post Roll', value=1)
        cmds.text(label = '')
        self.widgets['rotButton'] = cmds.button(label='Rotation', command=self.derive_rotation_callback)
        self.widgets['transButton'] = cmds.button(label='Translation', command=self.integrate_translation_callback)
        cmds.setParent('..')
        cmds.setParent('..')
    
        cmds.showWindow(self.widgets["window"])
        
    def parent_callback(self, *args):
        print('|parent_callback|')
        if len(cmds.ls(sl=True)) == 1:
            parent_value = cmds.ls(sl=True)[0]
            cmds.textField(self.widgets['parentTextField'], edit=True, text=parent_value)
            print('parent_value is %s' % (parent_value))
            self.flyer.parent_value = parent_value
        else:
            print("Please select a single object")


    def initialize_callback(self, *args):
        print('|initialize_callback|')
        if len(cmds.ls(sl=True)) == 1:
            #print "selection length is: %s" % ( len( cmds.ls( sl=True ) ) )
            targetValue = cmds.ls( sl=True )[0]
            cmds.textField(self.widgets['targetTextField'], edit=True, text=targetValue)
            self.flyer = Flyer(targetValue) 
        else:
            print("Please select a single object")

    
    def derive_rotation_callback(self, *args):
        print('|derive_rotation_callback|')
        # Get values from Parameter fields
        plane = cmds.optionMenu(self.planeMenu, query=True, value=True)
        scale = cmds.intField(self.scale, query=True, value=True)
        smoothness = cmds.intField(self.smoothness, query=True, value=True)
        autoRoll = cmds.checkBox(self.autoPrePost, query=True, value=True)
        
        if (smoothness % 2) == 0:
            print('smoothness value must be an odd number')
        else:
            self.flyer.parent_state = cmds.radioButton(self.widgets['parentRadioButton'], query=True, select=True)
            self.flyer.smoothness = smoothness
            self.flyer.derive_rotation(plane[0], plane[1], scale, smoothness, autoRoll, 3)

    
    def integrate_translation_callback(self, *pArgs):
        print('|integrate_translation_callback|')
        plane = cmds.optionMenu(self.planeMenu, query=True, value=True)
        scale = cmds.intField(self.scale, query=True, value=True)
        autoRoll = cmds.checkBox(self.autoPrePost, query=True, value=True)
        self.flyer.parent_state = cmds.radioButton(self.widgets['parentRadioButton'], query=True, select=True)
        self.flyer.integrate_translation(plane[0], plane[1], scale, autoRoll)
