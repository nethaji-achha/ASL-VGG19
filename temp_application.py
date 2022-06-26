from ast import Try
from msilib.schema import Directory
import os
import shutil
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

import pandas as pd
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras.preprocessing import image
from keras.models import load_model
from keras.applications.vgg19 import preprocess_input

def CreateWidgets():
	link_Label = Label(root, text ="Select The Files : ",bg = "#E8D579")
	link_Label.grid(row = 1, column = 0,pady = 150, padx = 150)
	
	root.sourceText = Entry(root, width = 50,textvariable = sourceLocation)
	root.sourceText.grid(row = 1, column = 1,pady = 5, padx = 5,columnspan = 2)
	
	source_browseButton = Button(root, text ="Browse",command = SourceBrowse, width = 15)
	source_browseButton.grid(row = 1, column = 3,pady = 5, padx = 5)
	
	copyButton = Button(root, text ="Recognize the Sign language", command = pridicting, width = 25)
	copyButton.grid(row = 3, column = 1,pady = 50, padx = 5)
    
    
def SourceBrowse():
    root.sourceText.delete(0, END)
    root.files_list = list(filedialog.askopenfilenames(initialdir ="/"))
    root.sourceText.insert('1', root.files_list)
    # only select one file
    if len(root.files_list) > 1:
        messagebox.showinfo("Warning", "Please select only one file")
        root.files_list = []
        root.sourceText.delete(0, END)
        return
    # check if the file is an image
    if root.files_list[0].split('.')[-1] not in ['jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG']:
        messagebox.showinfo("Warning", "Please select an image file")
        root.files_list = []
        root.sourceText.delete(0, END)
        return
    # check if the file is a valid image
    try:
        img = Image.open(root.files_list[0])
    except:
        messagebox.showinfo("Warning", "Please select a valid image file")
        root.files_list = []
        root.sourceText.delete(0, END)
        return
    


def pridicting():
    files_list = root.files_list
    for f in files_list:
        i_path = f
        imgName= i_path.split('/')[-1]
        model = load_model('./main_Model.h5')
        label = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        img = image.load_img(i_path, target_size = (200,200))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        features = model.predict(x)
        thresholded = (features>0.5)*1
        ind = np.argmax(thresholded)
        print('Pridict label : ', label[ind])
        messagebox.showinfo("Result", label[ind])
        root.files_list = []
        root.sourceText.delete(0, END)
        return

        


# Creating object of tk class
root = tk.Tk()
	
# Setting the title and background color
# disabling the resizing property
root.geometry("960x700")
root.title("ASL Sign language Recognizer")
root.config(background = "black")

sourceLocation = StringVar()
	
# Calling the CreateWidgets() function
CreateWidgets()
	
# Defining infinite loop
root.mainloop()
