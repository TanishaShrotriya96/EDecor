# Convolutional Neural Network

# Installing Theano
# pip install --upgrade --no-deps git+git://github.com/Theano/Theano.git

# Installing Tensorflow
# pip install tensorflow

# Installing Keras
# pip install --upgrade keras

# Part 1 - Building the CNN

# Importing the Keras libraries and packages
from keras.models import Sequential #initializes neural network (as a sequence of layers)
from keras.layers import Conv2D # used for Convolution step (2D images)
from keras.layers import MaxPooling2D # adds the poolig layers
from keras.layers import Flatten #convert all pooled feature maps into large feature vector
from keras.layers import Dense #add fully connected layers to ANN architecture
from keras.models import model_from_json
import os
os.chdir('/home/tanisha/EDecor/FrontEnd/Stylizer')

# Initialising the CNN
classifier = Sequential()

# Step 1 - Convolution 
# we decide the number of feature detectors to slide over the input image.
#Conv2D(filters=32,(perFilterRows=3,perFilterCols=3))
#input shape tells the shape of input image shape which is 3D since it is color image.
#theano backend uses (3,64,64) (channels, width,length)
#tensorflow backend uses the following.
#Relu adds non linearity 
classifier.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'))

# Step 2 - Pooling
#reduce the grid size to reduce the total number of nodes.
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Adding a second convolutional layer
classifier.add(Conv2D(32, (3, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Step 3 - Flattening
classifier.add(Flatten())

# Step 4 - Full connection
classifier.add(Dense(units = 128, activation = 'relu'))
classifier.add(Dense(units = 2, activation = 'softmax'))

# Compiling the CNN
classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

# Part 2 - Fitting the CNN to the images

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('train',
                                                 target_size = (64, 64),
                                                 batch_size = 12,
                                                 class_mode = 'categorical')

test_set = test_datagen.flow_from_directory('test',
                                            target_size = (64, 64),
                                            batch_size =12,
                                            class_mode = 'categorical')

classifier.fit_generator(training_set,
                         steps_per_epoch = 100,
                         epochs = 15,
                         validation_data = test_set,
                         validation_steps =100,
                         shuffle=True,
                         use_multiprocessing=True)
#===================================================================================
import os
#save the model
name=str(input(("Enter name of model")))
jsonFile=name+".json"
model_json = classifier.to_json()
with open(jsonFile, "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
hFile=name+".h5"
classifier.save_weights(hFile)
print("Saved model to disk")

#=====================================================================================
#Save classes to indices mapping
classes=training_set.class_indices
print(classes)
        
name=str(input(("Enter name of file  =>")))
trainFile=name+".txt" 
#saving class to number mappings
with open(trainFile, 'w') as f:
    for key, value in classes.items():
        f.write('%s:%s\n' % (key, value))

#code to open dictionary of classes
classes = dict()
with open(trainFile) as raw_data:
    for item in raw_data:
        if ':' in item:
            key,value = item.split(':', 1)
            classes[key]=value.strip('\n')
        else:
            pass # deal with bad lines of text here
classes
type(training_set)

#=====================================================================================
# get the name of model to load
name=str(input(("Enter name of model  =>")))
jsonFile=name+".json"
hFile=name+".h5"
#load json and create model
json_file = open(jsonFile, 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights(hFile)
print("\n\nLoaded model from disk")
#b8e25t801a60i128


import numpy as np
from keras.preprocessing import image
DIR="single_image"
batch=len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
print(batch)
files=os.listdir("single_image")
print(files)
l1 = list()
for name in files :
    filename="single_image/"+name
    print(name)
    test_image = image.load_img(filename,target_size=(64,64))
    #add third dimension for color image.
    test_image = image.img_to_array(test_image)
    #add one more dimension that corresponds to batch.
    l1.append(test_image)
    
print(len(l1))
#print(l1)

l2=np.array(l1)
type(l2)
l2.shape
result =loaded_model.predict_classes(l2, batch_size=batch)

#grouping images according to recommendation 
print(result)
pairs = list(zip(result,files))
type(pairs)
from collections import defaultdict
dictionary = defaultdict(list) # defaults to list
for k, v in pairs:
    dictionary[k].append(v)
print(dictionary)    


classes=training_set.class_indices
classes
        
name=str(input(("Enter name of file  =>")))
trainFile=name+".txt" 

#saving class to number mappings
with open(trainFile, 'w') as f:
    for key, value in classes.items():
        f.write('%s:%s\n' % (key, value))

#code to open dictionary of classes
classes = dict()
with open(trainFile) as raw_data:
    for item in raw_data:
        if ':' in item:
            key,value = item.split(':', 1)
            classes[key]=value.strip('\n')
        else:
            pass # deal with bad lines of text here
classes
type(training_set)
