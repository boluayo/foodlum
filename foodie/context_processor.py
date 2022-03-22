from foodie.models import Variety,Shopcart



def dropdown(request):
    varieties = Variety.objects.all()
    
    context = {
        'varieties':varieties
    }
    
    return context

def cartread(request):
    cart = Shopcart.objects.filter(user__username= request.user.username,item_paid=False)
    cartcount = 0
    for item in cart:
        cartcount += item.quantity
        
    context ={
        'cartcount': cartcount
    }
    return context