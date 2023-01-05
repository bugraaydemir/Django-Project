from django.contrib import admin
from .models import BackgroundImage, Item, Order, OrderItem,LandingPageEdit,Logo
# Register your models here.
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(LandingPageEdit)
admin.site.register(BackgroundImage)
admin.site.register(Logo)