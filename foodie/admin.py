from django.contrib import admin

# Register your models here.
from . models import *


class VarietyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'image', 'created', 'updated')
    list_display_links = ('id','name', 'slug')
    prepopulated_fields = {'slug':('name',)}
    


class MealAdmin(admin.ModelAdmin):
    list_display = ('id', 'variety', 'meal','slug', 'image', 'spicy', 'time', 'price','discount','min_order', 'max_order',  'breakfast', 'lunch', 'dinner','display', 'created', 'updated')
    list_display_links = ('id','variety', 'meal','slug')
    list_editable = ['display','discount','price']
    prepopulated_fields = {'slug':('meal',)}
    


class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'phone', 'email', 'message', 'created','status', 'closed']
    list_display_links = ['id', 'first_name', 'last_name', 'phone']
    


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['cart_code', 'user', 'first_name', 'last_name', 'phone', 'address', 'state', 'image']
    list_display_links = ['cart_code', 'user', 'first_name', 'last_name']
   
    
class ShopcartAdmin(admin.ModelAdmin):
    list_display =  ['id','user','meal','quantity','how_spicy','order_no','item_paid']
    list_display_links = ['id', 'user', 'meal', 'quantity']
    readonly_fields =  ['id','user','meal','quantity','order_no','item_paid']
    
class PaidorderAdmin(admin.ModelAdmin):
    list_display = ['id','user','total','cart_no','payment_code','paid_item','first_name','last_name']
    list_display_links = ['id','user','cart_no','paid_item']
    readonly_fields = ['id','user','total','cart_no','payment_code','paid_item','first_name','last_name']
    
class ShippingAdmin(admin.ModelAdmin):
    list_display =  ['id','user','meal','shipping_no','paid_cart','first_name','last_name','address','phone','state','status','admin_remark']
    list_display_links = ['id','user','meal']
    readonly_fields = ['id','user','shipping_no','paid_cart','first_name','last_name','address','phone','state']


    
admin.site.register(Variety,VarietyAdmin)   
admin.site.register(Meal,MealAdmin)    
admin.site.register(Contact,ContactAdmin)   
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Shopcart,ShopcartAdmin)
admin.site.register(PaidOrder,PaidorderAdmin)
admin.site.register(Shipping,ShippingAdmin)

