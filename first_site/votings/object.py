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
#sys.path.append("..")
from object_detection.utils import ops as utils_ops
from keras.models import model_from_json
#if StrictVersion(tf.__version__) < StrictVersion('1.9.0'):
# raise ImportError('Please upgrade your TensorFlow installation to v1.9.* or later!')
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
import matplotlib
#import cache to store loaded model
from django.core.cache import cache
#import cv2

#declaring and defining GLOBAL VARIABLES

#os.chdir('/home/tanisha/EDecor/FrontEnd/models/research/object_detection')

DIR=os.getcwd().strip('first_site')+'FrontEnd/models/research/object_detection/'
# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_FROZEN_GRAPH =os.getcwd().strip('first_site')+'FrontEnd/codes/ssd_mobilenet_v1_coco_2017_11_17/frozen_inference_graph.pb'
#PATH_TO_FROZEN_GRAPH = '/home/tanisha/EDecor/FrontEnd/faster_rcnn_resnet50_coco_2018_01_28/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.

PATH_TO_LABELS = DIR+"data/mscoco_label_map.pbtxt"
detection_graph = tf.Graph()
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)
PATH_TO_TEST_IMAGES_DIR = os.getcwd().strip('first_site')+'FrontEnd/crisisPred/static/test_images'
# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)
TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image{}.jpg'.format(i)) for i in range(1, 8) ]


class ObjectDetection :
	
	def __init__(self):

		#loading frozen graph
		with detection_graph.as_default():
		  od_graph_def = tf.GraphDef()
		  with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
		    serialized_graph = fid.read()
		    od_graph_def.ParseFromString(serialized_graph)
		    tf.import_graph_def(od_graph_def, name='')

		print("Starting object detection")
		print("Path to frozen graph: ",PATH_TO_FROZEN_GRAPH)
		print("Path to labels: ", PATH_TO_LABELS)
		print("Detection_graph: ", detection_graph)
		#print("Category_index: ", category_index[1])
		print("Path to test_images: ", PATH_TO_TEST_IMAGES_DIR)
		#print("Paths of all test_images: ", TEST_IMAGE_PATHS)
		print("Image Size Variable: ", IMAGE_SIZE)

	def run_inference_for_single_image(self,image, graph):
	  with graph.as_default():
	    with tf.Session() as sess:
	      # Get handles to input and output tensors
	      ops = tf.get_default_graph().get_operations()
	      all_tensor_names = {output.name for op in ops for output in op.outputs}
	      tensor_dict = {}
	      
	      for key in ['num_detections', 'detection_boxes', 'detection_scores', 'detection_classes', 'detection_masks']:
	        tensor_name = key + ':0'
	        if tensor_name in all_tensor_names:
	          tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)
	      
	      if 'detection_masks' in tensor_dict:
	        # The following processing is only for single image
	        detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
	        detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
	        # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
	        real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
	        detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
	        detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
	        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(detection_masks, 
	        	detection_boxes, image.shape[0], image.shape[1])
	        detection_masks_reframed = tf.cast(tf.greater(detection_masks_reframed, 0.5), tf.uint8)
	        # Follow the convention by adding back the batch dimension
	        tensor_dict['detection_masks'] = tf.expand_dims(detection_masks_reframed, 0)
	      
	      image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')
	      # Run inference
	      output_dict = sess.run(tensor_dict,
	                             feed_dict={image_tensor: np.expand_dims(image, 0)})
	      # all outputs are float32 numpy arrays, so convert types as appropriate
	      output_dict['num_detections'] = int(output_dict['num_detections'][0])
	      output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.uint8)
	      output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
	      output_dict['detection_scores'] = output_dict['detection_scores'][0]
	     
	      if 'detection_masks' in output_dict:
	        output_dict['detection_masks'] = output_dict['detection_masks'][0]
	  
	  return output_dict

	def load_image_into_numpy_array(self,image):
	  (im_width, im_height) = image.size
	  return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)