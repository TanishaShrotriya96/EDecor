
from django.shortcuts import render,get_object_or_404
from django.views.generic import TemplateView, ListView # Import TemplateView.
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse
from django.shortcuts import render_to_response

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
import ntpath

#shows all products by style and by category
def product_list(request, category_slug=None):
    
    print("Running...................product_list") #20 dots
    currentRoom=request.session.get('currentRoom')
    currentStyle=request.session.get('currentStyle')
    roombreadth = request.session.get('roombreadth')
    roomlength = request.session.get('roomlength')
    category = None
    categories = Category.objects.all()
        
    if currentStyle!=None:
        #for All selected in category
        print("currentStyle not None")
        products = Product.objects.filter(available=True,description__icontains=currentStyle)
       
        print(currentStyle," ",currentRoom)
        if category_slug:
            print("category_slug: ",category_slug)
            category = get_object_or_404(Category, slug=category_slug)
            #BEAUTIFUL
            products = Product.objects.filter(category=category,description__icontains=currentStyle)
            print(type(products))
        if category_slug=="nostyle":
            products = Product.objects.filter(available=True)
       

    else:
        print("currentStyle is None")
        products = Product.objects.filter(available=True)
       
        print(currentStyle," ",currentRoom)
        if category_slug:
            print("category_slug: ",category_slug)
            category = get_object_or_404(Category, slug=category_slug)
            products = Product.objects.filter(category=category)
            print(type(products))

    user=request.user.username
    #extracting session variable of current logged in user.
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'user':user
    }

    return render(request, 'polls/product/list.html', context)



#shows each product in detail
def product_detail(request, id, slug):
    print("I am in product_detail")
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    user=request.user.username
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
#To show all the uploaded image rooms
def AllImages(request):
    print("I am inside all images")
    customer_id=request.user.id
    customer_name=request.user.username
    print(request.user.username)
    #print(request.user.email)
    #print(request.user.id)

    #g = get_object_or_404(Document,pk=customer_id)
    #i = get_object_or_404(Document, pk=1)
    i = Document.objects.all().order_by('-id')
    return render(request, 'polls/product/myimages.html', {'imagedata' :i })


def AllFurtherImages(request):
    print("I am inside all images")
    customer_id=request.user.id
    customer_name=request.user.username
    print(request.user.username)
    #print(request.user.email)
    #print(request.user.id)

    #g = get_object_or_404(Document,pk=customer_id)
    #i = get_object_or_404(Document, pk=1)
    i = Document.objects.all().order_by('-id')
    return render(request, 'polls/product/yourimages.html', {'imagedata' :i })

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
            #customer_id=request.session.get('customer_id')
            customer_id=request.user.id
            customer_name=request.user.username
            # create a model object and save the file to database.
            brvalue = form.cleaned_data.get("breadth")
            levalue = form.cleaned_data.get("length")
            
            roomImage = Document(docfile = request.FILES['docfile'], breadth = brvalue, length=levalue, customer_id=customer_id)
            print("Room Image Path is: ", roomImage.docfile.path)
            roomImage.save()
            # change the location of file to a more secure location.
            print("Name of Docfile",roomImage.docfile.path)
            print("Name of File " , request.FILES['docfile'].name)
            print("BREADTH", roomImage.breadth)
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
            br = roomImage.breadth
            le = roomImage.length
            request.session['roomlength']=le
            request.session['roombreadth']=br
            request.session['currentRoom']=file
            request.session['currentStyle']=roomImage.style1
            #used for debug. 
            #print(file)'''
            print("New Path is: "+newName)
            document = roomImage
            print(document)
            
            #=========== Send analysed images to template ===============
            #file=ntpath.basename(newName) 
            li=sorted(os.listdir(os.getcwd()+"/static/Analysis/"))
            c1=li[0]
            c2=li[1]
            c3=li[2]
            c4=li[3]
            c5=li[4]
            c6=li[5]
            c7=li[6]
            c8=li[7]
            c9=li[8]
            c10=li[9]
            c11=li[10]
            c12=li[11]
            c13=li[12]
            c14=li[13]
            c15=li[14]
            c16=li[15]
            c17=li[16]
            c18=li[17]
            c19=li[18]
            c20=li[19]
            c21=li[20]
            c22=li[21]
            c23=li[22]
            c24=li[23]
            c25=li[24]
            c26=li[25]
            #l2=sorted(os.path(li))
            print(li)
            # Redirect to the document list after POST.
            #return HttpResponseRedirect(reverse('list1')).
            return render(request, 'polls/uploadRoom.html', {'document': document, 
                'form': form, 'list':li, 'file':file,'c1':c1,'c2':c2,'c3':c3,'c4':c4,'c5':c5,'c6':c6,'c7':c7,'c8':c8,'c9':c9,'c10':c10,'c11':c11,'c12':c12,'c13':c13,'c14':c14,'c15':c15,'c16':c16,'c17':c17,
                'c18':c18,'c19':c19,'c20':c20,'c21':c21,'c22':c22,'c23':c23,'c24':c24,'c25':c25,'c26':c26},)
    # Load documents for the list page.

    
    #call object detector here
    #print("When inside list1 customer_id is: ", customer_id)
    #print("When inside list1: ", password)

    # print(documents)
    # Render list page with the documents and the form
    print("POST NOT received")
    return render(request, 'polls/uploadRoom.html', { 'form': form},)


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


