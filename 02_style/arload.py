#********************************************************************
# content = loads Arnold
#
# how to = execute_ar_load()
#
#********************************************************************

import os
import datetime

from Qt import QtCompat

import libLog
import libFunc
import arSaveAs

from arUtil import ArUtil

#**************************************************************************************************
# VARIABLES

TITLE = "load"
LOG   = libLog.init(script=TITLE)

#***************************************************************************************************

class ArLoad(ArUtil):
    def __init__(self):
        super(ArLoad, self).__init__()
        path_ui              = ("/").join([os.path.dirname(__file__), "ui", TITLE + ".ui"])
        self.save_as         = ''
        self.wg_load         = QtCompat.loadUi(path_ui)
        self.load_dir        = ''
        self.load_file       = ''
        self.scene_steps     = ''
        self.software_format = {y:x.upper() for x,y in self.data['software']['EXTENSION'].items()}
        self.software_keys   = list(self.software_format.keys())
        self.wg_load.lstScene.clear()
        self.wg_load.lstStatus.clear()
        self.wg_load.lstSet.clear()
        self.clear_meta()
        self.resize_widget(self.wg_load)
        self.wg_load.show()

        LOG.info('START : ArLoad')

    def press_btn_accept(self):
        if not os.path.exists(self.load_file):
            self.set_status('FAILED LOADING : Path doesn\'t exists: {}'.format(self.load_file),
                msg_type=3)
            return False

    def prepress_menu_item_add_folder(self):
        self.save_as = arSaveAs.start(new_file=False)

    def press_menu_sort(self, list_widget, reverse=False):
        file_list = []
        for index in xrange(list_widget.count()):
             file_list.append(list_widget.item(index).text())
        list_widget.clear()
        list_widget.addItems(sorted(file_list, reverse=reverse))

    def change_last_scene(self):
        self.load_dir = self.data['project']['PATH'][self.wg_load.lstScene.currentItem().text()]
        tmp_content = libFunc.get_file_list(self.load_dir)
        self.scene_steps = len(
            self.data['rules']['SCENES'][self.wg_load.lstScene.currentItem().text()].split('/'))
        if self.scene_steps < 5:
            self.wg_load.lstAsset.hide()
        else:
            self.wg_load.lstAsset.itemSelectionChanged.connect(self.change_last_asset)
            self.wg_load.lstAsset.show()
        self.wg_load.lstSet.clear()
        if tmp_content:
            self.wg_load.lstSet.addItems(sorted(tmp_content))
            self.wg_load.lstSet.setCurrentRow(0)

    def change_last_set(self):
        new_path = self.load_dir + '/' + self.wg_load.lstSet.currentItem().text()
        tmp_content = libFunc.get_file_list(new_path)
        if self.scene_steps < 5:
            self.wg_load.lstTask.clear()
            if tmp_content:
                self.wg_load.lstTask.addItems(sorted(tmp_content))
                self.wg_load.lstTask.setCurrentRow(0)
        else:
            self.wg_load.lstAsset.clear()
            if tmp_content:
                self.wg_load.lstAsset.addItems(sorted(tmp_content))
                self.wg_load.lstAsset.setCurrentRow(0)

    def change_last_asset(self):
        new_path = self.load_dir + '/' + self.wg_load.lstSet.currentItem().text() + '/' + self.wg_load.lstAsset.currentItem().text()
        tmp_content = libFunc.get_file_list(new_path)
        self.wg_load.lstTask.clear()
        if tmp_content:
            self.wg_load.lstTask.addItems(sorted(tmp_content))
            self.wg_load.lstTask.setCurrentRow(0)

    def fill_meta(self):
        self.wgPreview.lblTitle.setText(self.file_name)
        self.wgPreview.lblDate.setText(str
                                      (datetime.datetime.fromtimestamp
                                      (os.path.getmtime
                                      (self.load_file))).split('.', maxsplit=1)[0])
        self.wgPreview.lblSize.setText(str("{0:.2f}".format(os.path.getsize(self.load_file)
                                      /(1024*1024.0)) + " MB"))

    def clear_meta(self):
        self.wgPreview.lblUser.setText('')
        self.wgPreview.lblTitle.setText('')
        self.wgPreview.lblDate.setText('')

def execute_ar_load():
    global main_widget
    main_widget = ArLoad()
