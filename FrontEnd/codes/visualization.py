import numpy as np
import tensorflow as tf
from distutils.version import StrictVersion
from collections import defaultdict
from io import StringIO
from PIL import Image
import PIL 
from keras.preprocessing import image as im
import os
from keras.models import model_from_json
import matplotlib.pyplot as plt
import pandas as pd
from keras.models import Model
from vis.visualization import visualize_cam

print("Got model")

name = os.getcwd()+'/a90b8'
jsonFile = name+".json"
hFile = name+".h5"

#load json and create model
json_file = open(jsonFile, 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)  
# load weights into new model
print("Before",loaded_model.get_weights()[1])
loaded_model.load_weights(hFile)
print("Weights",)
print("After",loaded_model.get_weights()[1])

#=======================================================
#finding out more about the model

print(loaded_model.summary())
print(loaded_model.layers)
#get model layer which comes before flattening
output_layer=loaded_model.get_layer('max_pooling2d_2')

print(output_layer.get_config())
'''
#create model with this layer as an output
model=Model(inputs=loaded_model.input, outputs=output_layer.output)

#get the feature map weights from final dense layer
final_dense=loaded_model.get_layer('dense_2')
W=final_dense.get_weights()[0]'''
#=======================================================


#=======================================================
#loading image

l1 = list()
img = Image.open(os.getcwd()+'/sample.jpg') 
   
img = img.resize((64,64),Image.ANTIALIAS)
img_np = im.img_to_array(img)

l1.append(img_np) # preparing list for stylizer
l2 = np.array(l1)
result = loaded_model.predict(l2, batch_size=10)    
print(result)

model=visualize_cam(loaded_model, layer_idx=6, filter_indices=None, seed_input=img_np)

plt.figure(figsize=(12,8))
plt.imshow(model)
plt.show(block=True)
#=======================================================
#get the classes to style name mapping
'''
#name=str(input(("Enter name of file  =>")))
trainedWeights = os.getcwd()+'/style'
trainFile = trainedWeights+".txt"
#code to open dictionary of classes
classes = dict()
with open(trainFile) as raw_data:
    for item in raw_data:
        if ':' in item:
            key,value = item.split(':', 1)
            classes[key] = value.strip('\n')
        else:
            pass # deal with bad lines of text here
#======================================================
# printing for debugging purposes

print("Classes are: "+ str(classes))
keys = list(classes.keys())
print("keys: ", keys)
values = list(classes.values())
print("values: ", values)

#=====================================================
#finding style which is seen in most quantity

result = list(result)
unique = set(result)
print("unique results"+ str(unique))
total=list()
print("Before for each in unique")

for each in unique:
    count = result.count(each)
    value = keys[values.index(str(each))]
    print("(str(each)", str(each))
    print("values.index(str(each)) ",values.index(str(each)))
    print("keys[values.index(str(each))]",keys[values.index(str(each))])
    total.append((each,count))
print("classes found as :",total)
'''