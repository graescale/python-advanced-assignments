
<p style="color: red; font-weight: bold">>>>>>  gd2md-html alert:  ERRORs: 5; WARNINGs: 2; ALERTS: 9.</p>
<ul style="color: red; font-weight: bold"><li>See top comment block for details on ERRORs and WARNINGs. <li>In the converted Markdown or HTML, search for inline alerts that start with >>>>>  gd2md-html alert:  for specific instances that need correction.</ul>

<p style="color: red; font-weight: bold">Links to alert messages:</p><a href="#gdcalert1">alert1</a>
<a href="#gdcalert2">alert2</a>
<a href="#gdcalert3">alert3</a>
<a href="#gdcalert4">alert4</a>
<a href="#gdcalert5">alert5</a>
<a href="#gdcalert6">alert6</a>
<a href="#gdcalert7">alert7</a>
<a href="#gdcalert8">alert8</a>
<a href="#gdcalert9">alert9</a>

<p style="color: red; font-weight: bold">>>>>> PLEASE check and correct alert issues and delete this message and the inline alerts.<hr></p>



# AnimSim v0.4 Documentation

author: Grae Revell

version: 0.4

Status: Development


## Release Notes



* Added option to automatically add pre & post roll.


# Contents



<p id="gdcalert1" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: undefined internal link (link text: "Description"). Did you generate a TOC? </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert2">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

[Description](#heading=h.ywpkmm8zq6f5)



<p id="gdcalert2" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: undefined internal link (link text: "Launching"). Did you generate a TOC? </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert3">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

[Launching](#heading=h.stbq8k868g1d)



<p id="gdcalert3" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: undefined internal link (link text: "Overview"). Did you generate a TOC? </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert4">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

[Overview](#heading=h.svy7wwppihn)



<p id="gdcalert4" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: undefined internal link (link text: "Workflow"). Did you generate a TOC? </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert5">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

[Workflow](#heading=h.lm69wf9tz6k0)



<p id="gdcalert5" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: undefined internal link (link text: "Tips & Tricks"). Did you generate a TOC? </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert6">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

[Tips & Tricks](#heading=h.suktwqj0m9hb)


# Description

AnimSim (working title) builds additive animation on layers to simulate the effect of rotation of a self-balancing object on its translation and vice-versa.

For example, you can animate a helicopter’s translation and use AnimSim to generate the realistic pitch (rotate X) and roll (rotate Z) necessary to achieve your animated maneuver. 

Likewise, you can animate a helicopter’s rotation, (pitch and roll) and use AnimSim to generate the resulting translation.

You can also use them together. After changing an object’s path or translation, you can simply update the rotation. Don’t like the rotation it generated? Add a rotation layer and keyframe some new poses and then use AnimSim to update the translation.

There are two modes:



* Build rotation based on translation
* Build translation based on rotation.


# Launching

AnimSim requires a Python module not loaded in Maya 2018 by default. In order to use the tool, you must first launch Maya with the following command in a terminal:

**ctxl &lt;show> -a maya -P sciPy**

Once Maya is open, load the script:



1. In Maya, open the Script Editor and click:

     **File > Source Script…**

2. Choose:

    ** /mnt/users/grevell/tools/scripts/AnimSim/anim_sim_v0.4.py**


To launch AnimSim, run the following command in a Python tab in the Script Editor. (You may also copy this to a Python shelf for easier access)

**anim_sim = AnimSim()**


# Overview



<p id="gdcalert6" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image1.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert7">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image1.png "image_tooltip")



### Initialization

Select a single object and press the **Initialize **button to set the object as the target for future operations. The object’s name will appear next to the button to confirm the selection.

To change objects, select another object and press the Initialize button.

If the object is parented to another animated object (such as the srt_SUB_CON), choose the “Parent” radio button, select the parent object and click **Set Parent**. The parent object’s name will appear next to the button to confirm the selection.


### Parameters


#### Plane

Sets the 2D plane in which the object is moving.


#### Scale

Sets the object’s scale. Larger numbers indicate a larger scale.


#### Smoothness

Sets the amount of smoothness to apply to the translation animation in order to build rotation. Maya’s animation curves are deceptively pointy so translation curves must be smoothed before deriving rotation.

The Smoothness value must be an odd number.

**N.B. Anim Sim requires a pre/post roll equivalent to or greater than the Smoothness value relative to the current Time Slider range. Turn on ‘Auto Pre / Post Roll’ in order to automatically set the pre / post roll range.**


### Build


#### Auto Pre / Post Roll

Automatically sets the pre / post roll range so users don’t have to adjust the Time Slider.


#### Rotation

Creates an additive animation layer containing rotation curves in 2 axes (relative to the Plane parameter) named auto_rotation_layer.

*Pressing the Rotation button again will overwrite keys on the auto_rotation_layer.


#### Translation

Creates an additive animation layer containing translation curves in 2 axes (relative to the Plane parameter) named auto_translation_layer.

*Pressing the Translation button again will overwrite keys on the auto_translation_layer.


# Workflow


### Overview

Anim Sim builds rotation and translation animation on separate animation layers.



<p id="gdcalert7" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image2.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert8">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image2.png "image_tooltip")




* Rotation is built by first creating or editing an object’s translation and clicking the Build Rotation button. This will generate rotation curves on an automatically created auto_rotation_layer.
* Translation is built by first creating or editing an object’s rotation and clicking the Build Translation button. This will generate translation curves on an automatically created auto_translation_layer.

Creating realistic self-balancing motion depends on an object’s translation and rotation being synchronized. After creating or editing translation keys, Build Rotation will match the rotation to the object’s current global translation. Likewise, after you create or edit rotation keys, Build Translation will match the translation to the object’s current global rotation.

To keep the rotation and translation synchronized, the general workflow follows a simple, repeatable pattern:



<p id="gdcalert8" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline drawings not supported directly from Docs. You may want to copy the inline drawing to a standalone drawing and export by reference. See <a href="https://github.com/evbacher/gd2md-html/wiki/Google-Drawings-by-reference">Google Drawings by reference</a> for details. The img URL below is a placeholder. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert9">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![drawing](https://docs.google.com/drawings/d/12345/export/png)

**It is strongly recommended that you key the object’s translation and rotation on separate, dedicated animation layers.**



<p id="gdcalert9" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image3.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert10">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image3.png "image_tooltip")



### Usage


#### Build Rotation



1. Animate an object’s translation (dedicated animation layer recommended).
2. Launch the tool. (You may also launch it before animating).
3. Select the object.
4. Press the **Initialize **button.
5. Verify the name displayed in the tool is correct.
6. Set desired parameters.
7. Verify that 
* **Auto Pre / Post** is checked

        OR

* You have animated both pre and post-roll equivalent to or greater than the Smoothness parameter value and that the pre and post-roll are visible within the Time Slider.
8. Verify that the object’s local and global rotation values (i.e. parents, SRT controls, etc.) are a constant 0.
9. Press the **Build** **Rotation **button.
10. Enjoy the miracle of creation.
11. Adjust the translation animation as desired and repeat steps 6-10.

*N.B. AnimSim builds rotation curves based on the object's global translation. This includes translation on animation layers as well as point constraints.


#### Build Translation



1. Animate an object’s rotation (dedicated animation layer recommended) (or build it with the **Build Rotation** button).
2. Launch the tool. (You may also launch it before animating).
3. Select the object. (Skip steps 3-5 if the object is already initialized)
4. Press the **Initialize **button.
5. Verify the name displayed in the tool is correct.
6. Set desired parameters.
7. Press the **Build** **Rotation **button.
8. Weep in silent awe.
9. Adjust the rotation animation as desired and repeat steps 6-8.


# Tips & Tricks



* Key translation and rotation curves each on separate, dedicated animation layers.
* Clicking either **Build **button will overwrite keys on the associated auto layer only for the time range you set. Keys outside the time range will not be affected.
* To keep your translation and rotation synchronized, try keeping the same smoothness value.
* Try putting specific actions (like performances and gestures) on separate animation layers to better organize your work.
* When you’re happy with the animation, try copying the rotation curves with offset to other parts of the rig (wings, thrusters, head, etc.) for a more integrated animation.

End
