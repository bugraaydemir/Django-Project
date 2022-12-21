from django.contrib import admin
from .models import BackgroundImage, Item, Order, OrderItem,LandingPageEdit
# Register your models here.
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(LandingPageEdit)
admin.site.register(BackgroundImage)
