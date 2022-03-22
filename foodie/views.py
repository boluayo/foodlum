import uuid
import requests
import json

from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Q



# Create your views here.
# from foodie.models import *
from foodie.forms import *




def index(request):
    breakfast = Meal.objects.filter(breakfast=True,display=True).order_by('-id')[:4]
    lunch = Meal.objects.filter(lunch=True,display=True).order_by('-id')[:4]
    dinner = Meal.objects.filter(dinner=True,display=True).order_by('-id')[:4]
    varieties = Variety.objects.all()
    
    
    context = {
        'breakfast':breakfast,
        'lunch':lunch,
        'dinner':dinner,
        'varieties':varieties,
    }
    return render(request, 'index.html', context)




def meals(request):
    if 'itemsearch' in request.GET:
       searched = request.GET['itemsearch']
       meals  = Meal.objects.filter(Q(Q(meal__icontains=searched)|Q(time__icontains=searched)))
    else:
        meals = Meal.objects.all()
    
    context = {
        'meals':meals,
    }
    return render(request, 'meals.html', context)


def searched(request):
    if request.method == 'POST':
        searched = request.POST['itemsearch']
        search_item  = Q(Q(meal__icontains=searched)|Q(time__icontains=searched))
        search_meals  = Meal.objects.filter(search_item)                                 
    else:
       search_meals = Meal.objects.all()
    
    context = {
        'search_meals':search_meals,
    }
    return render(request, 'searched.html', context)


def meal(request, id,slug):
    meal = Meal.objects.get(pk=id)
       
    context = {
        'meal':meal,
    }
    return render(request, 'meal.html', context)






def variety(request, id, slug):
    variety = Meal.objects.filter(variety_id=id)
    single = Variety.objects.get(pk=id)

    
    context = {
        'variety': variety,
        'single':single,
    
    }
    return render(request, 'variety.html', context)

def varieties(request):
    
    return render(request, 'varieties.html')

# def checkout(request):
    
#     return render(request, 'checkout.html')

#contact 
def contact(request):
    cform = ContactForm() #instantiate an empty form for a GET request
    if request.method == 'POST':
        cform = ContactForm(request.POST)#instantiate the form for a POST request
        if cform.is_valid():
            cform.save()
            messages.success(request, 'Thank you for contacting us, Our Customer Care will reach you soon😊')
            return redirect('index')
        else:
            messages.error(request, cform.errors)
            return redirect('index')
    
    context = {
        'cform':cform
    }
    
    return render(request,'index.html', context)
#contact done


#profile 
def user_profile(request):
    user_profile = Profile.objects.get(user__username=request.user.username)
        
    context = {
        'user_profile':user_profile,
    }
    return render(request, 'user_profile.html', context)


@login_required(login_url='register')
def profile_update(request):
    load_profile = Profile.objects.get(user__username=request.user.username)
    form = ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            user = form.save()
            messages.success(request,f'Dear {user.first_name} your  update is successful🙂')
            return redirect('user_profile')
        else:
            messages.error(request,form.errors)
            return redirect('profile')
        
    context = {
        'load_profile':load_profile,
        'form':form
    }
    
    return render(request, 'profile_update.html', context)
#profile done





def signin(request):
    #making a post request
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user:
            login(request, user)
            messages.success(request, f"welcome {user.first_name}, its good to have you here!")
            return redirect('index')
        else:
            messages.error(request, 'incorrect Username or Password')
            return redirect('signin')
    
    varieties = Variety.objects.all()
    context = {
        'varieties':varieties
    }
    
    return render(request, 'signin.html', context)




def logoutt(request):
    logout(request)
    return redirect('signin')





#authentication methods
def register(request):
    form = RegisterForm() #instantiate the reistration form for a GET request
    if request.method =='POST': # check if a POST method for persisting data to the DB
        phone = request.POST['phone']
        image = request.POST['image']
        form = RegisterForm(request.POST) # instantiate the reisterform for a POST request
        if form.is_valid(): # ensures security checks here
            user = form.save() # save data if data is valid
            profile = Profile(user = user)
            profile.first_name = user.first_name
            profile.last_name = user.last_name
            profile.phone = phone
            profile.image = image
            profile.save()
            login(request, user)
            messages.success(request, f' Dear Customer Register Successful😊')
            return redirect('signin') # send user any page you desire, in this case Homepage
        else:
            messages.error(request, 'incorrect User or Password')
            return redirect('register')
    
    context = {
        'form':form
    }
        
    return render(request, 'register.html', context)

#Authentication done


#changepassword
@login_required(login_url='register')
def password_update(request):
    load_profile = Profile.objects.get(user__username=request.user.username)
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, f' Dear {user.first_name}, Your password has been updated successfully✅✅✅')
            return redirect('user_profile')
        else:
            messages.error(request, form.errors)
            return redirect('password-update')
               
    
    context = {
        'load_profile':load_profile,
        'form':form
    }
    return render(request, 'password_update.html', context)
#changepassword done


# def thank_you(request):
    # thank_you = thank_you.objects.get(user__username=request.user.username)
    # varieties = Variety.objects.all()
    
    # context = {
    #     'thank_you':thank_you,
    #     'varieties':varieties,
    # }
     
 
 
#  shopcart

def addtocart(request):
    # cart_code = str(uuid.uuid4())
    cartno = Profile.objects.get(user__username=request.user.username)
    cart_no = cartno.cart_code
    if request.method == 'POST':
        addquantity = int(request.POST['quantity'])
        addid = request.POST['mealid']
        mealid = Meal.objects.get(pk=addid)
        addspice = request.POST['how_spicy']
        # addspicy = request.POST.get('spicy', None)
        
        #instantiate the cart for prospective users
        cart= Shopcart.objects.filter(user__username=request.user.username,item_paid=False)
        if cart:   #instantiate the cart for a selected item
            more =Shopcart.objects.filter(meal_id=mealid.id,user__username=request.user.username,quantity=addquantity,how_spicy =addspice).first()
            if more:
                more.quantity = addquantity
                more.how_spicy = addspice
                more.save()
                messages.success(request,'product added to Shopcart')
                return redirect('meals')
            
            else:  #  add new items
                newitem = Shopcart()
                newitem.user = request.user
                newitem.meal = mealid
                newitem.quantity=addquantity
                newitem.how_spicy =addspice
                newitem.order_no= cart_no
                newitem.item_paid = False
                newitem.save()
                messages.success(request, 'product added to your shopcart!')
                return redirect('meals')

            
        else:  # create a cart
            newcart = Shopcart()
            newcart.user = request.user
            newcart.meal = mealid
            newcart.quantity=addquantity
            newcart.how_spicy =addspice
            newcart.order_no= cart_no
            newcart.item_paid = False
            newcart.save()
            messages.success(request, 'item has been added to your shopcart!')
        
    return redirect('meals')

def cart(request):
    cart = Shopcart.objects.filter(user__username=request.user.username, item_paid=False)
    
    subtotal = 0
    vat = 0
    total= 0
    
    
    for item in cart:
        if item.meal.discount:
            subtotal += item.meal.discount * item.quantity
        else:
            subtotal += item.meal.price * item.quantity
     
     #vat is at 7.5% of the subtotal      
    vat = 0.075 * subtotal
    
    #addition of vat and subtotal gives the total value to be charged  
    total = vat + subtotal
      
    context ={
        'cart':cart,
        'subtotal':subtotal,
        'vat':vat,
        'total':total,
        # 'orderno':cart[0].order_no
    }
    return render(request,'cart.html', context)


# delete items from shopcart
@login_required(login_url='signin')
def remove_item(request):
    deleteitem = request.POST['deleteitem']
    Shopcart.objects.filter(pk=deleteitem).delete()
    messages.success(request, 'item successfully deleted from your shopcart')
    return redirect('meals')
    


def checkout (request):
        cart = Shopcart.objects.filter(user__username=request.user.username, item_paid=False)
        profile = Profile.objects.get(user__username = request.user.username)
    
        subtotal = 0
        vat = 0
        total= 0
    
    
        for item in cart:
            if item.meal.discount:
                subtotal += item.meal.discount * item.quantity
            else:
                subtotal += item.meal.price * item.quantity
     
     #vat is at 7.5%       
        vat = 0.075 * subtotal
    
    #addition of vat and subtotal gives the total value to be charged  
        total = vat + subtotal
      
        context = {
        'cart':cart,
        'total':total,
        'profile':profile,
       
        
    }
        return render(request,'checkout.html', context)
    
   


@login_required(login_url='signin') 
def placeorder(request):
    if request.method == 'POST':
        #collect data to send to paystack
        #the api_key(application programming interface key) and curl (call url) will be sourced from paystack site,
        #paystack will give test secret key for testing, when u want to go live paystack will give live key
        #cburl (callback url), total, ref_num, order_num, email provided by me in my application
        #call to paystack
        api_key = 'sk_test_03185958cad1c48ab628d15f5616b4fea288b330'
        curl = 'https://api.paystack.co/transaction/initialize'
        cburl = 'http://3.85.119.178/paidorder'
        # cburl = 'http://localhost:8000/paidorder'
        ref_num = str(uuid.uuid4())
        total = float(request.POST['get_total']) * 100
        cartno = Profile.objects.get(user__username=request.user.username)
        order_num = cartno.cart_code
        address = request.POST['address']
        phone = request.POST['phone']
        state = request.POST['state']
        user = User.objects.get(username = request.user.username)
        
        headers ={'Authorization': f'Bearer {api_key}'}
        data ={'reference':ref_num, 'order_number':order_num, 'amount': int(total), 'callback_url':cburl, 'email':user.email,'currency':'NGN'}
        
        # collect data to send to paystack done
        # if currency is not stated the default is Dollar
        
        # call to paystack
        try:
            r = requests.post(curl, headers=headers, json=data)
        except Exception:
            messages.error(request, 'Network busy, please refresh and try again. thank you.')
        else:
            transback = json.loads(r.text)
            rd_url = transback['data']['authorization_url']
          
            
            # take record of transaction made
            paidorder = PaidOrder()
            paidorder.user = user
            paidorder.total = total/100
            paidorder.cart_no = order_num
            paidorder.payment_code = ref_num
            paidorder.paid_item = True
            paidorder.first_name = user.first_name
            paidorder.last_name = user.last_name
            paidorder.save()
            
            shipping = Shipping()
            shipping.user = user
            shipping.shipping_no = order_num
            shipping.paid_cart = True
            shipping.first_name = user.first_name
            shipping.last_name = user.last_name
            shipping.address = address
            shipping.phone = phone
            shipping.state = state
            shipping.save()
           
            #take record of transaction made done
            return redirect(rd_url)
        # call to paystack done, when transaction is successful it redirects to the callback page
        
        # if transaction error occurs it redirects to checkout
    return redirect('checkout')

def paidorder(request):
    cart = Shopcart.objects.filter(user__username=request.user.username, item_paid=False)
    for item in cart:
        item.item_paid = True 
        item.save()
    
    return render(request, 'paidorder.html')


# shopcart done
