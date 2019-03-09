#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 14:26:59 2019

@author: tanisha
"""
import numpy as np
import os
import tensorflow as tf
from distutils.version import StrictVersion
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
import PIL 
import numpy as np
from keras.preprocessing import image as im
# This is needed since the notebook is stored in the object_detection folder.
import os
os.chdir('/home/tanisha/EDecor/FrontEnd/models/research/object_detection')
#sys.path.append("..")
from object_detection.utils import ops as utils_ops
from keras.models import model_from_json
#if StrictVersion(tf.__version__) < StrictVersion('1.9.0'):
 # raise ImportError('Please upgrade your TensorFlow installation to v1.9.* or later!')

from utils import label_map_util
from utils import visualization_utils as vis_util
%matplotlib inline


# What model to download.
MODEL_NAME = '/home/tanisha/EDecor/FrontEnd/faster_rcnn_resnet50_coco_2018_01_28'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_FROZEN_GRAPH = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')


detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')


category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

PATH_TO_TEST_IMAGES_DIR = 'test_images'
TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image{}.jpg'.format(i)) for i in range(1, 8) ]
TEST_IMAGE_PATHS 
# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)

def run_inference_for_single_image(image, graph):
  with graph.as_default():
    with tf.Session() as sess:
      # Get handles to input and output tensors
      ops = tf.get_default_graph().get_operations()
      all_tensor_names = {output.name for op in ops for output in op.outputs}
      tensor_dict = {}
      for key in [
          'num_detections', 'detection_boxes', 'detection_scores',
          'detection_classes', 'detection_masks'
      ]:
        tensor_name = key + ':0'
        if tensor_name in all_tensor_names:
          tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
              tensor_name)
      if 'detection_masks' in tensor_dict:
        # The following processing is only for single image
        detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
        detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
        # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
        real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
        detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
        detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
            detection_masks, detection_boxes, image.shape[0], image.shape[1])
        detection_masks_reframed = tf.cast(
            tf.greater(detection_masks_reframed, 0.5), tf.uint8)
        # Follow the convention by adding back the batch dimension
        tensor_dict['detection_masks'] = tf.expand_dims(
            detection_masks_reframed, 0)
      image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

      # Run inference
      output_dict = sess.run(tensor_dict,
                             feed_dict={image_tensor: np.expand_dims(image, 0)})

      # all outputs are float32 numpy arrays, so convert types as appropriate
      output_dict['num_detections'] = int(output_dict['num_detections'][0])
      output_dict['detection_classes'] = output_dict[
          'detection_classes'][0].astype(np.uint8)
      output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
      output_dict['detection_scores'] = output_dict['detection_scores'][0]
      if 'detection_masks' in output_dict:
        output_dict['detection_masks'] = output_dict['detection_masks'][0]
  return output_dict

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)

'''for image_path in TEST_IMAGE_PATHS:
  image = Image.open(image_path)
  image.size
  # the array based representation of the image will be used later in order to prepare the
  # result image with boxes and labels on it.
  image_np = load_image_into_numpy_array(image)
  # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
  image_np_expanded = np.expand_dims(image_np, axis=0)
  # Actual detection.
  output_dict = run_inference_for_single_image(image_np, detection_graph)
  # Visualization of the results of a detection.
  vis_util.visualize_boxes_and_labels_on_image_array(
      image_np,
      output_dict['detection_boxes'],
      output_dict['detection_classes'],
      output_dict['detection_scores'],
      category_index,
      instance_masks=output_dict.get('detection_masks'),
      use_normalized_coordinates=True,
      line_thickness=8)
  plt.figure(figsize=IMAGE_SIZE)
  plt.imshow(image_np)'''
  
#===================================================
#Loading single image and detecting objects

TEST_IMAGE_PATHS  
images=Image.open(TEST_IMAGE_PATHS[5]) 
print("Image is as follows : \n\n\n")
images.show() 
print(images.size)
  # the array based representation of the image will be used later in order to prepare the
  # result image with boxes and labels on it.
image_np = load_image_into_numpy_array(images)
  # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
image_np_expanded = np.expand_dims(image_np, axis=0)
  # Actual detection.
output_dict = run_inference_for_single_image(image_np, detection_graph)
vis_util.visualize_boxes_and_labels_on_image_array(
      image_np,
      output_dict['detection_boxes'],
      output_dict['detection_classes'],
      output_dict['detection_scores'],
      category_index,
      instance_masks=output_dict.get('detection_masks'),
      use_normalized_coordinates=True,
      line_thickness=8)

print("\n\nDetected objects: ")
plt.figure(figsize=IMAGE_SIZE)
plt.imshow(image_np)

print("\n\nCoordinates of detected objects")
coordinates=output_dict['detection_boxes']
print(coordinates)
#===========================================================================
#cropping detected object for style
#getting non zero coordinates
coordinates =coordinates[np.sum(coordinates,axis=1)!=0]
print(coordinates)
width=images.size[0]
height=images.size[1]
l1 = list()
print("\n\nExtracting detected objects")
for each in coordinates :
    ymin=each[0]
    xmin=each[1]
    ymax=each[2]
    xmax=each[3]
    left=xmin*width
    right=xmax*width
    top=ymin*height
    bottom=ymax*height
    img=images.crop((left,top,right,bottom))
    print(img.size)
    img_np = load_image_into_numpy_array(img)
    print(img_np.shape)
    print(img.size)
    print(img.show())
    plt.figure(figsize=IMAGE_SIZE)
    plt.imshow(img_np)
    
    img=img.resize((64,64),Image.ANTIALIAS)
    img_np = im.img_to_array(img)
    
    l1.append(img_np) # preparing list for stylizer


l2=np.array(l1)
print("\n\nExtracted objects added to numpy array")
print(type(l2))
print("First value tells total objects sent to stylizer ",l2.shape)
# ===================================================
# load stylizer

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
#feed these images to classifier
result =loaded_model.predict_classes(l2, batch_size=10)    
print("Classes are : ", result)
#/home/tanisha/EDecor/FrontEnd/Stylizer/a90b8
#=======================================================
name=str(input(("Enter name of file  =>")))
trainFile=name+".txt"
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

#=====================================================
result=list(result)
unique=set(result)
print(unique)
total=list()
print("here")
for each in unique:
    count=result.count(each)
    total.append(count)
total

if(total[0]<total[1]) :
    images=Image.open("/home/tanisha/EDecor/FrontEnd/models/research/object_detection/test_images/image7.jpg") 
    image_np = load_image_into_numpy_array(images)
    plt.figure(figsize=IMAGE_SIZE)
    plt.imshow(image_np)
if(total[0]>total[1]):
    images=Image.open("/home/tanisha/EDecor/FrontEnd/models/research/object_detection/test_images/image8.jpg") 
    image_np = load_image_into_numpy_array(images)
    plt.figure(figsize=IMAGE_SIZE)
    plt.imshow(image_np)
    
#code to pass 5 images and then choose based on style extracted.