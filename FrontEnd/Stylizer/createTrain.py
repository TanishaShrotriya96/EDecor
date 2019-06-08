import os
import re
import random

Directory=str(input("Enter directory name "))
size=int(input("Enter train data size "))
size=int(0.2*size)
li=os.listdir(Directory)
l2=list()
l2=random.sample(li,k=size)
print(l2)

print("Adding files to test set ",Directory)
newD=Directory+"/test"
if(os.path.isdir(newD)==False):
	os.mkdir(newD)
try:
	for name in l2:
		    print(name)
		    old=Directory+"/"+name
		    updated=newD+"/"+name
		    os.rename(old,updated)

except:
	print("Error")    
