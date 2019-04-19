import os
import re

Directory=str(input("Enter directory name "))
#print(type(Directory))
print("sorting files in ",Directory)
li=os.listdir(Directory)
l2=list()
for x in li : 
	l2.append(x.strip("['.jpg','.jpeg','.png','.JPG','.JPEG','.PNG']"))

l2 = list(map(int, l2))
l2 = sorted(l2)
count =1 
missing_indices=list()
for each in l2:
	if(l2.index(each)!=each-1) : 
		missing_indices.append(each-1)

print(missing_indices)
'''try:
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
	print("Error")  '''  
