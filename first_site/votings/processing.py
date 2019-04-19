from votings.object import *
from keras.backend import clear_session
from django.core.cache import cache

class ProcessRoomImage:

  detector=ObjectDetection() 
  #===================================================
  #Loading single image and detecting objects
  def DetectObjects(self,roomImage):
    
    images=Image.open(roomImage) 
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
        
        img=img.resize((64,64),Image.ANTIALIAS)
        img_np = im.img_to_array(img)
        
        l1.append(img_np) # preparing list for stylizer


    l2=np.array(l1)
    print("\n\nExtracted objects added to numpy array")
    print(type(l2))
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
        name=os.getcwd()+'/static/StylizerModel/a90b8'
        jsonFile=name+".json"
        hFile=name+".h5"

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
        print("\n\nLoaded model from disk")   
        cache.set(model_cache_key, loaded_model, None) # save in the cache
        print("Model in cache", cache.get(model_cache_key))
        print("Here")
        # in above line, None is the timeout parameter. It means cache forever
        

    print("Inside LoadStylizer")
    result =loaded_model.predict_classes(l2, batch_size=10)    
    print("Classes are : ", result)

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
    print("keys: ", keys)
    values=list(classes.values())
    print("values: ", values)

    #=====================================================
    #finding style which is seen in most quantity
    
    result=list(result)
    unique=set(result)
    print("unique results"+ str(unique))
    total=list()
    print("Before for each in unique")

    for each in unique:
        count=result.count(each)
        value=keys[values.index(str(each))]
        print("(str(each)", str(each))
        print("values.index(str(each)) ",values.index(str(each)))
        print("keys[values.index(str(each))]",keys[values.index(str(each))])
        total.append((each,count))
    print("classes found as :",total)
    clear_session()
    return total

  def getStyleName(self, styleId):
    switcher= {
        0: 'black',
        1: 'pink',
    }
    
    return switcher.get(styleId, "none")     
