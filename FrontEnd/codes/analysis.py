#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 19:23:33 2019

@author: tanisha
"""

from keras.preprocessing.image import ImageDataGenerator
from keras.applications.mobilenet import preprocess_input
from keras.preprocessing import image
import numpy as np
import sklearn.metrics as metrics
import pandas as pd
import os
from IPython.display import Image
import keras
#====== LOAD MODEL ===============================================================================
# get the name of model to load
from keras.models import model_from_json
name=str(input(("Enter name of model  =>")))
jsonFile=name+".json"
hFile=name+".h5"
#load json and create model
json_file = open(jsonFile, 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights(hFile)
print("\n\nLoaded model from disk")
#/home/tanisha/EDecor/FrontEnd/Stylizer/tflpinkblack
#/home/tanisha/EDecor/FrontEnd/Stylizer/a_v2_bedstyle
#/home/tanisha/EDecor/FrontEnd/Stylizer/a90b8
os.chdir("/home/tanisha/EDecor/FrontEnd/Stylizer/Analysis")
test=pd.read_csv("/home/tanisha/EDecor/true_classes.csv")
test_images=os.listdir("/home/tanisha/EDecor/FrontEnd/Stylizer/Analysis")
test_images=sorted(test_images)
test_images
l1=[]
for image_path in test_images:
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    preprocessed_image=keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)
    #print("1  ",preprocessed_image)
    print("2  ",img_array_expanded_dims)
    #preprocessed_image = prepare_image('/home/tanisha/sample.jpg')
    predictions = model.predict(preprocessed_image)
    print(predictions)
    model
    pred=np.where(predictions==np.max(predictions))
    l1.append(pred)
len(l1)
l1[60:240]
y_pred=[]

for each in l1:
    print(each[1][0])
    y_pred.append(each[1][0])
    # since it is an array of two arrays of which index 0 is another array
    # and index 1 is empty. We want the value inside array at index 0
y_pred
y_true=test["class"].tolist()
type(y_true)

class_labels=['black','pink','white','brown','green','red']
report = metrics.classification_report(y_true[:], y_pred, target_names=class_labels)
print(report)    


#========================= CONFUSION MATRIX PLOT ===================================

import matplotlib.pyplot as plt

#confusion matrix code
cm=metrics.confusion_matrix(y_true,y_pred)

#plotting code
plt.figure(figsize=(8, 6))
plt.imshow(cm, interpolation='nearest', cmap='Blues')
plt.title("Confusion matrix for max frequency class\n\n\n ")
plt.colorbar()

target_names2=['Black','Pink','White','Brown','Green','Red']
target_names=['Black','Pink','White','Brown','Green','Red']
tick_marks = np.arange(len(target_names))
plt.xticks(tick_marks, target_names2, rotation=45)
plt.yticks(tick_marks, target_names)

thresh=cm.max() / 2

import itertools
for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, "{:,}".format(cm[i, j]),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

plt.tight_layout()
plt.ylabel('True label')
#plt.xlabel('Predicted label\n\n Max Frequency Class is - '+FCT[maxFreq])
plt.savefig("ConfusionMatrix")
plt.show()

#======================= Finding metrics using Image Generator ===========
test_datagen = ImageDataGenerator(rescale = 1./255,preprocessing_function=preprocess_input)
test_set = test_datagen.flow_from_directory('/home/tanisha/EDecor/FrontEnd/Stylizer/test',
                                            target_size=(224,224),
                                             color_mode='rgb',
                                             batch_size=32,
                                             class_mode=None,
                                             shuffle=False)

#===========predictions==============================================================================
test_set.reset()
#predictions on test set
step_size_test=1+np.math.ceil(test_set.samples//test_set.batch_size)
#step_size_test=13
#test_set.batch_size=32
#test_set.samples=438
predictions = model.predict_generator(test_set,steps=step_size_test)
print(predictions[:7])
predicted_classes = np.argmax(predictions, axis=1)

true_classes = test_set.classes[:]
class_labels = list(test_set.class_indices.keys())   
class_labels
print(true_classes.shape)
report = metrics.classification_report(true_classes, predicted_classes, target_names=class_labels)
print(report)    
metrics.confusion_matrix(true_classes, predicted_classes)

model.predict(test_set)


