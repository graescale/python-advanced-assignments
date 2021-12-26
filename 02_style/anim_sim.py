#*******************************************************************************
# content = Creates animation layers to simulate the self-balancing motion.
#
# version = 0.4.1
# date = 2021-12-19
# how to = animSim()
# dependencies = Maya
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
        self.startFrame = ''
        self.endFrame = ''
        self.keyFrames = []
        self.posAxis1 = []
        self.posAxis2 = []
        self.startPosAxis1 = 0
        self.startPosAxis2 = 0
        self.accelAxis1 = []
        self.accelAxis2 = []
        self.rotAxis1 = []
        self.rotAxis2 = []
        self.rotAxis1_dict = {}
        self.rotAxis2_dict = {}
        self.rotLayerName = ROTATION_LAYER
        self.transLayerName = TRANSLATION_LAYER
        self.smoothness = 0
        self.parentState = None
        self.parentValue = ''

#*******************************************************************************
# COLLECT  

    def get_scene_data(self):
        """Gather the current object's start and end frames.
        
        :return: None
        """
        print('|get_scene_data|')
        self.startFrame = int(cmds.playbackOptions(min=True,q=True))
        self.endFrame = int(cmds.playbackOptions(max=True,q=True))


    def get_anim_data(self, attr_list, autoRoll):
        """Return dictionary of lists of keyframe values for desired attributes.
        
        :param attr_list: The requested transfromation attributes
        :type attr_list: list
        :return: animation data lists
        :rtype: dictionary
        """
        print('|get_anim_data|')
        self.create_world_space_buffer(autoRoll)
        # Make a list of the keyframes to be used later in both modes.
        self.keyFrames = cmds.keyframe(self.name + '_buffer_raw', attribute=['translate', 'rotate'], query=True, timeChange=True)
        # Make a dictionary containing lists of keyframe values for each attribute.
        anim_data = {}
        for attr in attr_list:
            anim_data[attr] = cmds.keyframe(self.name + '_buffer_raw', at='.' + attr, query=True, valueChange=True)  
        return anim_data
    

    def create_world_space_buffer(self, autoRoll):
        
        """Create world space node with object's animated transforms.
        
        :param object: The object containing animated transforms.
        :type object: maya object
        :return: None
        """
        print('|create_world_space_buffer|')
        # Create  a buffer node.
        buffer_raw = self.name + '_buffer_raw'
        pm.createNode('transform', n = buffer_raw, ss = True)
        # Change the rotation order to zxy to prevent gimbal lock.
        cmds.setAttr(buffer_raw + '.rotateOrder', 2)
        if self.parentState:           
            # Parent buffer to parentValue.
            #print( 'parent is %s' % ( self.parentValue ) )
            cmds.parent( buffer_raw, self.parentValue )
        else:
            print( 'No parent set.' )
        # Constrain buffer to object, bake it, delete constraint.
        cmds.parentConstraint(self.name, buffer_raw, name='buffer_constraint')
        time_range = (self.startFrame, self.endFrame)
        if autoRoll == True:
            # Automatically add pre / post roll from the smoothness value
            time_range = (self.startFrame - self.smoothness, self.endFrame + self.smoothness)
        cmds.bakeResults(buffer_raw + '.translate', buffer_raw + '.rotate', t=time_range, sb=1)
        cmds.delete('buffer_constraint')


#*******************************************************************************
# HELPERS (MODULES?)


    def get_derivative(self, anim_data, degree, filter_data, window, order=3):
        """Return a list containing the n degree derivative of the supplied list.
        
        :param anim_data: The data to get derivatives from.
        :type anim_data: list
        :param degree: The number of derivatives to calculate.
        :type degree: int
        :param filter_data: Option to smooth the data after deriving.
        :type filter_data: bool
        :param window: The filter window size.
        :type window: int
        :param order: The filter polynomial order. Default 3
        :type order: int
        :return: The n degree derivative of anim_data
        :rtype: list
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
        """Return a list containing the n degree integral of the supplied list.
        
        :param anim_data: The data to get derivatives from.
        :type anim_data: list
        :param degree: The number of derivatives to calculate.
        :type degree: int
        :return: The n degree integral of anim_data
        :rtype: list
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
        """Smooth list of numbers using Savitzky–Golay filter.
        
        :param data: The numbers to smooth.
        :type data: list
        :param window: The smoothing window size.
        :type window: int
        :param order: The polynomial order to use in the smoothing method.
        :type order: int
        :return: The smoothed data.
        :rtype: list
        """
        print('|smoothData|')
        return scipy.signal.savgol_filter(data, window, order) 

 
    def create_anim_layer(self, layerName):
        """Create an animation layer
        
        param layerName: The name of layer to be created
        type layerName: str
        return: None
        """
        print('|create_anim_layer|')
        # Make an animation layer if it doesn't already exist.
        if not cmds.animLayer(layerName, query=True, exists=True):
           cmds.animLayer(layerName)
        # Add self to that animation layer.
        cmds.select(self.name)
        cmds.animLayer(layerName, edit=True, addSelectedObjects=True)


#*******************************************************************************
# PROCESS
        

    def derive_rotation(self, axis1, axis2, scale, window, autoRoll, polyOrder=3 ):
        """Derive object's rotation from its translation.
        
        :param axis1: 1st translation axis
        :type axis1: str
        :param axis2: 1st translation axis
        :type axis2: str
        :param scale: Value multiplier
        :type scale: int
        :param window: The filter window size. Default is 31
        :type window: int
        :param order: The filter polynomial order. Default is 3
        :type order: int
        :return: None
        """
        print('|derive_rotation|')
        self.get_scene_data()
        raw_anim_data = self.get_anim_data(['translate' + axis1, 'translate' + axis2], autoRoll)
        # Should replace lines below with loop
        self.rawPosAxis1 = raw_anim_data['translate' + axis1]
        self.rawPosAxis2 = raw_anim_data['translate' + axis2]
        self.posAxis1 = self.smoothData(self.rawPosAxis1, window, polyOrder)
        self.posAxis2 = self.smoothData(self.rawPosAxis2, window, polyOrder)
        self.accelAxis1 = self.get_derivative(self.posAxis1, 2, True, window)
        self.accelAxis2 = self.get_derivative(self.posAxis2, 2, True, window)      
        self.copy_to_rotation(scale, axis1, axis2)
        cmds.delete(self.name + '_buffer_raw')


    def integrate_translation(self, axis1, axis2, scale, autoRoll):
        """Derive object's translation from its rotation.
        
        :param axis1: 1st rotation axis
        :type axis1: str
        :param axis2: 1st rotation axis
        :type axis2: str
        :param scale: Value multiplier
        :type scale: int
        :return: None
        """
        print('|integrate_translation|') 
        self.get_scene_data()
        raw_anim_data = self.get_anim_data(['rotate' + axis1, 'rotate' + axis2, 'translate' + axis1, 'translate' + axis2], autoRoll)
        self.rotAxis1 = raw_anim_data['rotate' + axis1]
        self.rotAxis2 = raw_anim_data['rotate' + axis2]       
        # Get the local starting position
        self.startPosAxis1 = cmds.getAttr( self.name + '.translate' + axis1, time=self.startFrame - autoRoll )
        self.startPosAxis2 = cmds.getAttr( self.name + '.translate' + axis2, time=self.startFrame - autoRoll )
        #print( 'startPosAxis1 is %s' % ( self.startPosAxis1 ) )
        #print( 'startPosAxis2 is %s' % ( self.startPosAxis2 ) )
        # Swap axes because the integral of the rotation in axis1 is the translation in axis2
        self.posAxis2 = self.get_integral(self.rotAxis1, 2)
        self.posAxis1 = self.get_integral(self.rotAxis2, 2)
        # Get axis1 translation value at startFrame
        #print( 'posAxis1 is %s' % ( self.posAxis1 ) )
        #self.posAxis1 = [x - self.startPosAxis1 for x in self.posAxis1]
        #print( 'posAxis1\'s fist element after adding startPosAxis1 is %s' % ( self.posAxis1[0] ) )
        #self.posAxis2 = [x - self.startPosAxis1 for x in self.posAxis2]
        self.copy_to_translation(scale, axis1, axis2)
        cmds.delete(self.name + '_buffer_raw')

#*******************************************************************************
# APPLY


    def copy_to_rotation(self, scale, axis1, axis2):
        """Copy acceleration values to the object's rotation on a separate layer.
        
        :param scale: Value multiplier
        :type scale: int
        :param axis1: 1st translation axis
        :type axis1: str
        :param axis2: 1st translation axis
        :type axis2: str
        :return: None
        """
        print('|copy_to_rotation|')
        self.create_anim_layer(self.rotLayerName)
        cmds.animLayer(self.rotLayerName, edit=True, sel=True, prf=True)
        self.rotAxis1 = self.accelAxis2
        self.rotAxis2 = self.accelAxis1
        # Zip keyFrames and roation values lists into tuples and then into a dictionary
        self.rotAxis1_dict = dict(zip(self.keyFrames, self.rotAxis1))
        self.rotAxis2_dict = dict(zip(self.keyFrames, self.rotAxis2))
        for key in self.rotAxis1_dict:
            cmds.setKeyframe(self.name, time = key, at = 'rotate' + axis1, value = (self.rotAxis1_dict[key] * scale) )
            cmds.setKeyframe(self.name, time = key, at = 'rotate' + axis2, value = (self.rotAxis2_dict[key] * -scale) )
  

    def copy_to_translation(self, scale, axis1, axis2):
        """Copy generated values to the object's translation on a separate layer.
        
        :param scale: Value multiplier
        :type scale: int
        :param axis1: 1st rotation axis
        :type axis1: str
        :param axis2: 1st rotation axis
        :type axis2: str
        :return: None
        """
        print('|copy_to_translation|')
        self.create_anim_layer(self.transLayerName)
        cmds.animLayer(self.transLayerName, edit=True, sel=True, prf=True)
        # Zip keyFrames and position values lists into tuples and then into a dictionary
        self.posAxis1_dict = dict(zip(self.keyFrames, self.posAxis1))
        self.posAxis2_dict = dict(zip(self.keyFrames, self.posAxis2))
        # Apply scaling & subtract initial position values
        #self.posAxis1 = [ (self.posAxis1_dict[x] / -scale) - self.startPosAxis1 for x in self.posAxis1_dict]
        #self.posAxis2 = [ (self.posAxis1_dict[x] / scale) - self.startPosAxis2 for x in self.posAxis2_dict]
        for key in self.posAxis1_dict:
            cmds.setKeyframe(self.name, animLayer = self.transLayerName, time = key, at = 'translate' + axis1, value = (self.posAxis1_dict[key] / -scale + self.startPosAxis1) )
            cmds.setKeyframe(self.name, animLayer = self.transLayerName, time = key, at = 'translate' + axis2, value = (self.posAxis2_dict[key] / scale + self.startPosAxis2) )
        #print( 'posAxis1_dict key 990 is %s' % ( self.posAxis1_dict[990] / -scale ) )


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
        self.widgets['window'] = cmds.window( windowID, title='Anim Sim', w=400, h=300)
        self.widgets['mainLayout'] = cmds.columnLayout( adjustableColumn=True ) 
        
        # Initialization Frame
        self.widgets['frameLayout1'] = cmds.frameLayout( label='Initialization' )
        self.widgets['rowColumnLayout1'] = cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[ (1,200), (2,200)], columnOffset=[ 1,'right', 3], columnSpacing=[ (1,10), (2,10) ] )
        cmds.text( label='Select an object and click \"Initialize"' )
        cmds.separator( style='none' )
        self.widgets['intitButton'] = cmds.button( label='Initialize', command=self.initialize_callback )
        self.widgets['targetTextField'] = cmds.textField( text='none', editable=False )
        cmds.text( label='Parent Options' )
        cmds.text( label = '' )
        cmds.radioCollection()
        self.widgets['globalRadioButton'] = cmds.radioButton( label='Global' )
        self.widgets['parentRadioButton'] = cmds.radioButton( label='Parent' )
        self.widgets['parentButton'] = cmds.button( label='Set Parent', command=self.parent_callback )
        self.widgets['parentTextField'] = cmds.textField( text='none', editable=False )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        # Parameters Frame
        self.widgets['frameLayout2'] = cmds.frameLayout( label='Parameters' )
        self.widgets['rowColumnLayout2'] = cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[ (1,120), (2,150) ], columnOffset=[ 1,'right', 3], columnSpacing=[ (1,10), (2,10) ] )
        cmds.text( label='Motion Plane:' )  
        self.planeMenu = cmds.optionMenu()
        cmds.menuItem( label='XZ' )
        cmds.menuItem( label='XY' )
        cmds.menuItem( label='ZY' )
        cmds.text( label='Scale:' )
        self.scale = cmds.intField( value=150 )
        cmds.text( label='Smoothness (odd #):' )
        self.smoothness = cmds.intField( value=11, maxValue=99, minValue=3)
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        # Build Frame
        self.widgets['frameLayout3'] = cmds.frameLayout( label='Build' )
        self.widgets['cmds.rowColumnLayout3'] = cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[ (1,200), (2,200) ], columnSpacing=[ (1,10), (2,10) ] )
        self.autoPrePost = cmds.checkBox( label='Auto Pre / Post Roll', value=1 )
        cmds.text( label = '' )
        self.widgets['rotButton'] = cmds.button( label='Rotation', command=self.derive_rotation_callback )
        self.widgets['transButton'] = cmds.button( label='Translation', command=self.integrate_translation_callback )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
    
        cmds.showWindow( self.widgets["window"] )
        
    def parent_callback(self, *args):
        print( '|parent_callback|' )
        if len( cmds.ls( sl=True ) ) == 1:
            parentValue = cmds.ls( sl=True )[0]
            cmds.textField( self.widgets['parentTextField'], edit=True, text=parentValue )
            print( 'parentValue is %s' % ( parentValue ) )
            self.flyer.parentValue = parentValue
        else:
            print("Please select a single object")


    def initialize_callback(self, *args):
        print('|initialize_callback|')
        if len( cmds.ls( sl=True ) ) == 1:
            #print "selection length is: %s" % ( len( cmds.ls( sl=True ) ) )
            targetValue = cmds.ls( sl=True )[0]
            cmds.textField( self.widgets['targetTextField'], edit=True, text=targetValue )
            self.flyer = Flyer( targetValue ) 
        else:
            print("Please select a single object")

    
    def derive_rotation_callback(self, *args):
        print('|derive_rotation_callback|')
        # Get values from Parameter fields
        plane = cmds.optionMenu( self.planeMenu, query=True, value=True )
        scale = cmds.intField( self.scale, query=True, value=True )
        smoothness = cmds.intField( self.smoothness, query=True, value=True )
        autoRoll = cmds.checkBox( self.autoPrePost, query=True, value=True)
        
        if (smoothness % 2) == 0:
            print('smoothness value must be an odd number')
        else:
            #print 'flyer is: %s' % (self.flyer.name)
            #print 'plane: %s' % (plane)
            #print 'scale: %s' % (scale)
            #print( cmds.radioButton( self.widgets['parentRadioButton'], query=True, select=True ) )
            self.flyer.parentState = cmds.radioButton( self.widgets['parentRadioButton'], query=True, select=True )
            self.flyer.smoothness = smoothness
            self.flyer.derive_rotation( plane[0], plane[1], scale, smoothness, autoRoll, 3 )

    
    def integrate_translation_callback( self, *pArgs ):
        print('|integrate_translation_callback|')
        plane = cmds.optionMenu( self.planeMenu, query=True, value=True )
        scale = cmds.intField( self.scale, query=True, value=True )
        autoRoll = cmds.checkBox( self.autoPrePost, query=True, value=True)
        self.flyer.parentState = cmds.radioButton( self.widgets['parentRadioButton'], query=True, select=True )
        #print 'flyer is: %s' % (self.flyer.name)
        #print 'scale: %s' % (scale)
        self.flyer.integrate_translation( plane[0], plane[1], scale, autoRoll )

