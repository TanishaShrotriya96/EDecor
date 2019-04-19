from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
#databases imported
from .models import CustomerDetails,ItemDetails	
#for error handling. May not be in use 
import pdb

#used with upload image functionality
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse
from classify.models import Document
from classify.forms import DocumentForm

#used for saving uploaded image to static folder.
import os

#the algorithm file
from classify.object import *
# Create your views here.

def predict(request):
	print("Here")
	from sklearn.model_selection import train_test_split
	import numpy as np # linear algebra
	import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
	import pickle

	#read and preprocess data
	data=pd.read_csv("/home/tanisha/files/crisis-data.csv")
	data=data.iloc[:,4:7]
	data=data.dropna()


	ICT =list(pd.get_dummies(data['Initial Call Type'],prefix="ICT",dummy_na=False).columns.values)

	#create one-hot encodings and expand data set
	data = pd.concat([data,pd.get_dummies(data['Initial Call Type'], prefix='ICT',dummy_na=True)],axis=1).drop(['Initial Call Type'],axis=1)
	data = pd.concat([data,pd.get_dummies(data['Final Call Type'], prefix='FCT',dummy_na=True)],axis=1).drop(['Final Call Type'],axis=1)

	#may not be used
	data = pd.concat([data,pd.get_dummies(data['Call Type'], prefix='CT',dummy_na=True)],axis=1).drop(['Call Type'],axis=1)

	X=data.filter(regex=("ICT.*"))
	y=data.filter(regex=("FCT.*"))

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
	FCT=list(y_train.columns.values)

	# read model
	rf = pickle.load(open('/home/tanisha/files/rf.sav', 'rb'))

	input="ICT_SECONDARY - FORGERY/BUNCO/SCAMS/ID THEFT"
	
	if(request.GET.get('b1')):
		 input= request.GET.get('Name')

	print('Requested Call Type is ', input)
	l=[0]
	l= l*len(X_test.columns)
	l[ICT.index(input)]=1

	x=pd.DataFrame([l])

	y_pred = rf.predict(x)

	print('Predicted Final Call Type Is :',FCT[np.argmax(y_pred[0])])
	x=FCT[np.argmax(y_pred[0])]
	context={'x':x}
	return render(request,'predict.html',context)
	    
def calender(request):

    t = get_template('calender.html')
    html = t.render({'prediction': 'hi'})
    return HttpResponse(html)
    #return HttpResponse("You're looking at question %s.")

def eventD(request):

    t = get_template('eventD.html')
    html = t.render({'prediction': 'hi'})
    return HttpResponse(html)
    #return HttpResponse("You're looking at question %s.")

def dynamic(request):
    l1=list()
    l1=[("0",["sample1.jpeg","sample2.jpeg","sample3.jpeg"]),("1",["sample4.jpg"])]
    
    print(l1[0][1])
    input=""
    print(ItemDetails.objects.all())
    print(ItemDetails.item)
    print("HERE")

    if(request.GET.get('getList')):
       print("HERE2")
       input= request.GET.get('mySearch')
    print("HERE again")
    print(input)
    content=""
    if(input=="0"):
    	print("Now here")    
    	content=l1[0][1]
    if(input=="1"):
    	print("Now here")    
    	content=l1[1][1]
    print(content)
    context={'content':content}
    #pdb.set_trace()
    return render(request,'dynamic.html',context)
	    
def list1(request):
    # Handle file upload
    if(request.method == 'POST'):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            file=request.FILES['docfile']
            newdoc.save()
            oldName=newdoc.docfile.path
            newName="static/users/"+newdoc.docfile.name
            os.rename(oldName,newName)
            print(newdoc.docfile.path,file)
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list1'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page

    documents = Document.objects.all()
    # print(documents)
    # Render list page with the documents and the form
    return render(request, 'list.html', {'documents': documents, 'form': form},)
