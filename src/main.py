#!/usr/bin/env python

''' A basic GUi to use ImageViewer class to show its functionalities and use cases. '''
import os
import sys
from actions import ImageViewer
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, uic, QtWidgets
from utils.utils import getImages, save_to_txt, load_text


class Iwindow(QtWidgets.QMainWindow, uic.loadUiType("main.ui")[0]):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.cntr, self.numImages = -1, -1  # self.cntr have the info of which image is selected/displayed
        self.caption_root_path = 'captions'
        self.image_viewer = ImageViewer(self.qlabel_image)
        self.__connectEvents()
        self.showMaximized()
        
        self.image_viewer.enablePan(True)
        self.image_viewer.loadImage("/usr/app/assets/sample.png")    # initial place holder

    def __connectEvents(self):
        self.next_im.clicked.connect(self.nextImg)
        self.actionOpen_File.triggered.connect(self.selectDir)
        self.actionExit_2.triggered.connect(self.exit)
        
        self.prev_im.clicked.connect(self.prevImg)
        self.qlist_images.itemClicked.connect(self.item_click)
        self.save_caption.clicked.connect(self.saveCaption)

        self.actionZoom_In.triggered.connect(self.image_viewer.zoomPlus)
        self.actionZoom_Out.triggered.connect(self.image_viewer.zoomMinus)
        self.actionReset_Zoom.triggered.connect(self.image_viewer.resetZoom)
        
    def selectDir(self):
        ''' Select a directory, make list of images in it and display the first image in the list. '''
        # open 'select folder' dialog box
        self.folder = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if not self.folder:
            QtWidgets.QMessageBox.warning(self, 'No Folder Selected', 'Please select a valid Folder')
            return
        
        self.logs      = getImages(self.folder)
        self.numImages = len(self.logs)

        # make qitems of the image names
        self.items = [QtWidgets.QListWidgetItem(log['name']) for log in self.logs]
        for item in self.items:
            self.qlist_images.addItem(item)

        # display first image and enable Pan 
        self.cntr = 0
        self.image_viewer.enablePan(True)
        self.image_viewer.loadImage(self.logs[self.cntr]['path'])
       
        self.items[self.cntr].setSelected(True)
        self.load_caption()
        
        # enable the next image button on the gui if multiple images are loaded
        if self.numImages > 1:
            self.next_im.setEnabled(True)
        
        caption_dir = os.path.join(self.folder, self.caption_root_path)
        if not os.path.isdir(caption_dir):
            os.makedirs(caption_dir)
            
    def resizeEvent(self, evt):
        if self.cntr >= 0:
            self.image_viewer.onResize()

    def nextImg(self):
        if self.cntr < self.numImages -1:
            if self.caption_text_box.text() != "":
                self.saveCaption()
            self.cntr += 1
            
            self.image_viewer.loadImage(self.logs[self.cntr]['path'])
            self.items[self.cntr].setSelected(True)
            self.load_caption()
        else:
            QtWidgets.QMessageBox.warning(self, 'Sorry', 'No more Images!')

    def prevImg(self):
        if self.cntr > 0:
            if self.caption_text_box.text() != "":
                self.saveCaption()
            self.cntr -= 1
            
            self.image_viewer.loadImage(self.logs[self.cntr]['path'])
            self.items[self.cntr].setSelected(True)
            self.load_caption()
        else:
            QtWidgets.QMessageBox.warning(self, 'Sorry', 'It is the first image!')
            
    def saveCaption(self):
        if self.cntr >= 0:
            caption = self.caption_text_box.text()
            save_dir = self.get_selected_image_name()
            if caption != "":
                save_dir = os.path.join(
                    self.folder, 
                    self.caption_root_path, 
                    save_dir
                )
                save_to_txt(save_dir, caption)
            else:
                QtWidgets.QMessageBox.warning(self, 'Sorry', 'empty caption')
        else:
            QtWidgets.QMessageBox.warning(self, 'Sorry', 'No image to save caption')
  
    def load_caption(self):
        if self.cntr >= 0:
            path = self.get_selected_image_name()
            full_path = os.path.join(
                self.folder,
                self.caption_root_path,
                path
            )
            if os.path.isfile(full_path):
                txt = load_text(full_path)
                self.caption_text_box.setText(txt)
            else:
                self.caption_text_box.setText('')
        
    def get_selected_image_name(self):
        txt_file_name = self.items[self.cntr].text()
        txt_file_name = os.path.splitext(txt_file_name)[0]
        txt_file_name = '{}.txt'.format(txt_file_name)
        return txt_file_name
            
    
    def item_click(self, item):
        if self.caption_text_box.text() != "":
            self.saveCaption()
        self.cntr = self.items.index(item)
        self.image_viewer.loadImage(self.logs[self.cntr]['path'])
        self.load_caption()

    # next and prev using keyboad
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Down or event.key() == Qt.Key_Enter:
            self.nextImg()
        if event.key() == Qt.Key_Up:
            self.prevImg()
            
    def exit(self):
        sys.exit(0)
        
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create("Cleanlooks"))
    app.setPalette(QtWidgets.QApplication.style().standardPalette())
    parentWindow = Iwindow(None)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()