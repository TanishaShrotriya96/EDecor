import os
import re

Directory=str(input("Enter directory name "))
#print(type(Directory))
print("sorting files in ",Directory)
li=os.listdir(Directory)
#print(type(li),li)
newD=Directory+"/sorted"
if(os.path.isdir(newD)==False):
	os.mkdir(newD)
pattern=re.compile("\d*\.(jpg|JPG|jpeg|JPEG|png|PNG)")
try:
	for name in li:
		if (pattern.match(name)):
		    print("sorting file")
		    old=Directory+"/"+name
		    updated=newD+"/"+name
		    os.rename(old,updated)
	li=os.listdir(newD)
	unique=set(li)
	duplicates=list()
	print("here")
	for each in unique:
	    count=li.count(each)
	    if(count>1):
	        duplicates.append(each)
	print(duplicates)
except:
	print("Error")    
