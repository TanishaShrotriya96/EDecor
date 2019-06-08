from votings.object import *
from keras.backend import clear_session
from keras import backend as K
from django.core.cache import cache
import keras
import seaborn as sns
import re
import matplotlib.pyplot as plt
import cv2
import matplotlib.image as mpimg
import pandas as pd 
#used for extracting name of file from path to file
import ntpath

class ProcessRoomImage:

  detector=ObjectDetection() 
  name=""
  #===================================================
  #Loading single image and detecting objects
  def DetectObjects(self,roomImage):
    
    images=Image.open(roomImage) 
    self.name=roomImage
    #print("Image is as follows : \n\n\n")
    #images.show() 
    #print(images.size)
      # the array based representation of the image will be used later in order to prepare the
      # result image with boxes and labels on it.
    image_np = self.detector.load_image_into_numpy_array(images)
      # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
      # Actual detection.
    output_dict = self.detector.run_inference_for_single_image(image_np, detection_graph)
    vis_util.visualize_boxes_and_labels_on_image_array(
          image_np,
          output_dict['detection_boxes'],
          output_dict['detection_classes'],
          output_dict['detection_scores'],
          category_index,
          instance_masks=output_dict.get('detection_masks'),
          use_normalized_coordinates=True,
          line_thickness=8)

    print("\n\nDetected objects")
    #plt.figure(figsize=IMAGE_SIZE)
    #plt.save(os.getcwd()+"/static/users/cache")
    #plt.imshow(image_np)

    print("\n\nCoordinates of detected objects")
    coordinates=output_dict['detection_boxes']
    #rint(coordinates)
    #print(type(coordinates))
    return coordinates

  def ObjectExtraction(self,coordinates,roomImage):

    images=Image.open(roomImage) 
    coordinates =coordinates[np.sum(coordinates,axis=1)!=0]
    print(coordinates)
    print("image width: ")
    print("image height: ")
    
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
        img_np = self.detector.load_image_into_numpy_array(img)
        print(img_np.shape)
        print(img.size)
        #print(img.show())
        #plt.figure(figsize=IMAGE_SIZE)
        #plt.imshow(img_np)
        
        #size will change based on size given to model
        img=img.resize((224,224),Image.ANTIALIAS)
        img_np = im.img_to_array(img)
        
        #required for mobilenet model, not for sequential
        preprocessed_image=keras.applications.mobilenet.preprocess_input(img_np)

        l1.append(preprocessed_image) # preparing list for stylizer

    img_np = self.detector.load_image_into_numpy_array(images)
    print(img_np.shape)
    print(img.size)    
    #size will change based on size given to model
    img=img.resize((224,224),Image.ANTIALIAS)
    img_np = im.img_to_array(img)
    preprocessed_image=keras.applications.mobilenet.preprocess_input(img_np)
    l1.append(preprocessed_image) # preparing list for stylizer

    l2=np.array(l1)
    print("\n\nExtracted objects added to numpy array")
    print("last image prediction is : ",l2[-1])
    print("Shape of last prediction: ", l2[-1].shape)
    print("First value tells total objects sent to stylizer ",l2.shape)
    return l2 

  def LoadStylizer(self,l2):

    model_cache_key = 'model_cache' 
    # this key is used to `set` and `get` 
    # your trained model from the cache

    loaded_model = cache.get(model_cache_key) # get model from cache

    print("Got model")
    if loaded_model is None:
        print(", but unavailable")
        # your model isn't in the cache
        # so `set` it

        #get the model into json and hf format
        #name=str(input(("Enter name of model  =>")))
        name=os.getcwd()+'/static/StylizerModel/tfl'
        #name=os.getcwd()+'/static/StylizerModel/colors'
        jsonFile=name+".json"
        hFile=name+".h5"

        #load json and create model
        json_file = open(jsonFile, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)  
        # load weights into new model
        #print("Before",loaded_model.get_weights()[1])
        loaded_model.load_weights(hFile)
        #print("Weights",)
        #print("After",loaded_model.get_weights()[1])
        #print("\n\nLoaded model from disk")   
        cache.set(model_cache_key, loaded_model, None) # save in the cache
        #print("Model in cache", cache.get(model_cache_key))
        #print("Here")
        # in above line, None is the timeout parameter. It means cache forever
        

    #print("Inside LoadStylizer")
    #result =loaded_model.predict_classes(l2, batch_size=10)    
    result =loaded_model.predict(l2, batch_size=10)    
    print("Classes are (till 7th index): ", result[:7])
 
    #=======================================================
    #get the classes to style name mapping

    #name=str(input(("Enter name of file  =>")))
    trainedWeights=os.getcwd()+'/static/StylizerModel/style'
    trainFile=trainedWeights+".txt"
    #code to open dictionary of classes
    classes = dict()
    with open(trainFile) as raw_data:
        for item in raw_data:
            if ':' in item:
                key,value = item.split(':', 1)
                classes[key]=value.strip('\n')
            else:
                pass # deal with bad lines of text here
    #======================================================
    # printing for debugging purposes

    print("Classes are: "+ str(classes))
    keys=list(classes.keys())
    #print("keys: ", keys)
    values=list(classes.values())
    #print("values: ", values)

    #=====================================================
    #finding style which is seen in most quantity
    
    #needed for transfer learning mobilenet model
    pred=[]
    for each in result:
        #print(each)
        #print(np.max(each))
        #print(np.where(each==np.max(each)))
        pred.append(np.where(each==np.max(each))[0][0])
        # since it is an array of two arrays of which index 0 is another array
        # and index 1 is empty. We want the value inside array at index 0
    print(pred) 
    
    #result=list(result)
    #unique=set(result)
    result=list(pred)
    unique=set(pred)
    print("unique results"+ str(unique))
    total=list()
    #print("Before for each in unique")

    for each in unique:
        count=result.count(each)
        value=keys[values.index(str(each))]
        print("(str(each)", str(each))
        print("values.index(str(each)) ",values.index(str(each)))
        print("keys[values.index(str(each))]",keys[values.index(str(each))])
        total.append((each,count))
    print("classes found as :",total)
    
    #================= CREATE CLASS ACTIVATION MAP =====================
    model=loaded_model
    results=pd.DataFrame({'probability':result[-1],'category':["black","pink"]})

    f = sns.barplot(x='probability',y='category',data=results,color="red")
    sns.set_style(style='white')
    f.grid(False)
    f.spines["top"].set_visible(False)
    f.spines["right"].set_visible(False)
    f.spines["bottom"].set_visible(False)
    f.spines["left"].set_visible(False)
    f.set_title('Predictions:')

    argmax = np.argmax(result[-1])
    output = model.output[:, argmax]
    #for i,layer in enumerate(model.layers):
        #print(i,layer.name)


    layers=[]
    names=['conv_pw_1_relu','conv_pw_2_relu','conv_pw_3_relu','conv_pw_4_relu','conv_pw_5_relu',
           'conv_pw_6_relu','conv_pw_7_relu','conv_pw_8_relu','conv_pw_9_relu','conv_pw_10_relu',
           'conv_pw_11_relu','conv_pw_12_relu','conv_pw_13_relu'] 
    for i,layer in enumerate(model.layers):
        if(re.search("conv_pw_\d*_relu",layer.name)):
            layers.append(model.get_layer(layer.name))
       
    len(layers)      
    #create new directory to store all analysis images for current room image 
    #file=ntpath.basename(self.name) 
    #if(os.path.isdir(os.getcwd()+"/static/Analysis/"+file)==False):
     #   os.mkdir(os.getcwd()+"/static/Analysis/"+file)
    
    for each in range(0,len(layers)):
        print(layers[each].output)
        grads = K.gradients(output, layers[each].output)[0]
        pooled_grads = K.mean(grads, axis=(0, 1, 2))
        iterate = K.function([model.input], [pooled_grads, layers[each].output[0]])
        processed_image=l2[-1]
        processed_image=np.expand_dims(processed_image,axis=0)
    
        print(processed_image.shape)
        pooled_grads_value, conv_layer_output_value = iterate([processed_image])
        for i in range(layers[each].output_shape[3]):
            conv_layer_output_value[:, :, i] *= pooled_grads_value[i]
            
    #==================plot heatmap===================================================  
        heatmap = np.mean(conv_layer_output_value, axis=-1)
        heatmap = np.maximum(heatmap, 0)
        heatmap /= np.max(heatmap)
        plt.matshow(heatmap)
        plt.savefig(os.getcwd()+"/static/Analysis/conv"+str(each)+".jpg")
        #plt.show()
        img = l2[-1]
        heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        hif = .8
        superimposed_img = heatmap * hif + img
        out = os.getcwd()+"/static/Analysis/camconv"+str(each)+".jpg"
        cv2.imwrite(out, superimposed_img)
        img=mpimg.imread(out)

    clear_session()
    return total

  def getStyleName(self, styleId):
    switcher= {
        0: 'black',
        1: 'pink',
    }
    
    return switcher.get(styleId, "none")     
