
from django.shortcuts import render,get_object_or_404
from django.views.generic import TemplateView, ListView # Import TemplateView.
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse

from votings.models import *
from votings.forms import *
#import cv2
#from .model import bed
#used for saving uploaded image to static folder.
import os
#importing object detection code
from votings.object import *
from votings.processing import *
from django.http import HttpResponse
from .models import Category, Product 
from cart.forms import CartAddProductForm
#from .model import bed
import json
# to find substring in description of product to categorize by style
import re

def product_list(request, category_slug=None):
    print("Running...................product_list") #20 dots
    currentRoom=request.session.get('currentRoom')
    currentStyle=request.session.get('currentStyle')

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True,description__icontains=currentStyle)
   
    print(currentStyle+" "+currentRoom)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        #BEAUTIFUL
        products = Product.objects.filter(category=category,description__icontains=currentStyle)

        print(type(products))
    user=request.session.get('customer_name')
    #extracting session variable of current logged in user.
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'user':user
    }
    return render(request, 'polls/product/list.html', context)


def product_detail(request, id, slug):
    print("I am in product_detail")
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    user=request.session.get('customer_name')
    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        'user':user
    }
    return render(request, 'polls/product/detail.html', context)


class IndexPageView(TemplateView):

    template_name = "polls/index.html"


class CatPageView(TemplateView):
    template_name = "polls/cat.html"

def uploadRoom(request):

    # Handle file upload
    print("I am inside uploadRoom")
    form = DocumentForm() # A empty, unbound form.
    print("Created a Document Form")
    if(request.method == 'POST'):

        print("POST request received")
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")
            # obtain session id of user.
            customer_id=request.session.get('customer_id')

            # create a model object and save the file to database.
            roomImage = Document(docfile = request.FILES['docfile'], customer_id=customer_id)
            print("Room Image Path is: ", roomImage.docfile.path)
            roomImage.save()
            # change the location of file to a more secure location.
            print("Name of Docfile",roomImage.docfile.path)
            print("Name of File " , request.FILES['docfile'].name)
            oldName=roomImage.docfile.path
            newName=os.getcwd()+"/static/users/"+ roomImage.docfile.name
            os.rename(oldName,newName)
            
            # load the image of room and detect the objects.
            processRoom=ProcessRoomImage()
            detected_objs=processRoom.DetectObjects(newName)
            print(detected_objs)
            
            # extract the objects from room.
            objects=processRoom.ObjectExtraction(detected_objs,newName)

            # return style of the objects.
            styles=processRoom.LoadStylizer(objects)
            print(styles)
            # styles is a list of tuples
            # so we sort based on second value in each tuple so key =x[1]
            # and we want it to e in descending order
            styles=sorted(styles,key=lambda x: x[1], reverse=True)
            print(styles)
            # saving the style of user.
            style1=styles[0][0]
            style2=styles[1][0]
            
            roomImage.style1=processRoom.getStyleName(style1)
            roomImage.style2=processRoom.getStyleName(style2)          
            roomImage.save()

            #save the room image as the current session image.
            file=roomImage.docfile.name      
            request.session['currentRoom']=file
            request.session['currentStyle']=roomImage.style1
            
            #used for debug. 
            #print(file)
            print("New Path is: "+newName)
            document = roomImage
            print(document)
            # Redirect to the document list after POST.
            #return HttpResponseRedirect(reverse('list1')).
            return render(request, 'polls/uploadRoom.html', {'document': document, 'form': form},)
    # Load documents for the list page.

    
    #call object detector here
    #print("When inside list1 customer_id is: ", customer_id)
    #print("When inside list1: ", password)

    # print(documents)
    # Render list page with the documents and the form
    print("POST NOT received")
    return render(request, 'polls/uploadRoom.html', { 'form': form},)

def login(request):

    print("here")
    # when secure request is received for login
    if(request.method =='POST'):
         print("CONNECTED TO LOGIN")

         username= request.POST.get('user')
         password= request.POST.get('password')

         #counting total users in database where the username and password match
         #the max count can be one and if either or both are incorrect then
         #it will be 0
         customer_obj=CustomerDetails.objects.get(
                      name=username,password=password)
         
         print(customer_obj,"Counting total users: ",customer_obj)

         # if user is authenticated then
         if(customer_obj): 
             print("Name Matched")
             #create a session id for the specific user with id and username
             customer_id=customer_obj.id
             #setting session variables for the logged in session
             request.session['customer_id']=customer_id
             request.session['customer_name']=customer_obj.name

             print("When inside login customer_id is : ", customer_id)
             print("Now rendering list.html")
             #now render the html page for upload functionality
             return render(request, 'polls/uploadRoom.html')
         else:
             #else render the same page
             return render(request, 'polls/index.html')
    else:
        return render(request, 'polls/index.html')

def logout(request) :
    print("I am in logout")
    if(request.method == 'POST'):
        request.session.flush()
    return render(request, 'polls/index.html')

'''#from django.shortcuts import render
#from django.template.loader import get_template
# Create your views here.
#from django.http import HttpResponse


#def index(request):
 #   return HttpResponse("Hello, world. You're at the polls index.")

#def basefunc(request):
#	b = get_template('polls/login.html')
#	html = b.render({'shubhangi':'hi'})
#	return HttpResponse(html)
    #return HttpResponse("Hello, world. You're at the polls index.")'''


