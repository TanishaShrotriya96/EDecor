import re
import os 

more="yes"
try:
	while(more=="yes") :
		Directory=str(input("Enter directory name"))
		print(type(Directory))
		print("renaming files in",Directory)
		count=1
		for filename in os.listdir(Directory):
		    print(type(Directory),type(filename))
		    newName=""
		    if filename.endswith(".jpg"):
		       newName=Directory+"/"+str(count)+".jpg"
		       name=Directory+"/"+filename;
		       os.rename(name,newName)
		       count=count+1
		    if filename.endswith(".JPG"):
		       newName=Directory+"/"+str(count)+".JPG"
		       name=Directory+"/"+filename; 	
		       os.rename(name,newName)
		       count=count+1
		    if filename.endswith(".jpeg"):
		       name=Directory+"/"+filename;
		       newName=Directory+"/"+str(count)+".jpeg"
		       os.rename(name,newName)
		       count=count+1
		    if filename.endswith(".JPEG"):
		       name=Directory+"/"+filename;
		       newName=Directory+"/"+str(count)+".JPEG"
		       os.rename(name,newName)
		       count=count+1
		    if filename.endswith(".png"):
		       name=Directory+"/"+filename;
		       newName=Directory+"/"+str(count)+".png"
		       os.rename(name,newName)
		       count=count+1
		    if filename.endswith(".PNG"):
		       name=Directory+"/"+filename;
		       newName=Directory+"/"+str(count)+".PNG"
		       os.rename(name,newName) 
		       count=count+1
		    print(newName)
		more=input("rename in another foler?")
except IOError:
	print("Error")

	
