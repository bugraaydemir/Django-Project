from email.policy import default
from pickle import TRUE
from django.conf import settings
from django.db import models
from django.urls import reverse

app_label = 'ESite_App'

# Create your models here.
CATEGORY_CHOICES = (
 ('Camping Tent','Camping Tent'),
 ('Survival Gadget','Survival Gadget'),
 ('Clothing','Clothing'),
 ('Cooking','Cooking'),
)


class LandingPageEdit(models.Model):
    Cascade_Image= models.ImageField()

def get_absolute_url(self):
    return reverse("Esite_App:item_list", kwargs={
        'slug': self.slug
})
class BackgroundImage(models.Model):
 Background_Image = models.ImageField()

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20, default=None)
    Images = models.ImageField(upload_to = 'static/images', default=None)
    Image_1 = models.ImageField(upload_to = 'static/images', default=None)
    Image_2= models.ImageField(upload_to = 'static/images', default=None)
    Image_3= models.ImageField(upload_to = 'static/images', default=None)


    slug = models.SlugField(max_length=140, default=None)
    description = models.TextField(max_length=140, default=None)
    bestseller = models.BooleanField(default=False)
    Color = models.CharField(max_length=20,  blank=True)
    Color2 = models.CharField(max_length=20, blank=True)
    Color3 = models.CharField(max_length=20, blank=True)
    Color4 = models.CharField(max_length=20, blank=True)
    Color5 = models.CharField(max_length=20, blank=True)
    Color6 = models.CharField(max_length=20, blank=True)




    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("ESite_App:store", kwargs={
            'slug': self.slug
        })
    def get_add_to_cart_url(self):
        return reverse("ESite_App:add-to-cart", kwargs={
            'slug': self.slug
        })
    def get_remove_from_cart_url(self):
        return reverse("ESite_App:remove_from_cart", kwargs={
            'slug': self.slug
        })
    def get_decrease_from_cart(self):
        return reverse ("ESite_App:decrease_from_cart", kwargs = {
            'slug': self.slug
        })
    def get_add_to_order(self):
        return reverse ("ESite_App:add_to_order", kwargs = {
            'slug': self.slug
        })
        
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    color = models.CharField(default='', max_length=20)
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_item_color(self):
        return self.color
    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40, default=None)
    last_name = models.CharField(max_length=40, default=None)
    phone_number = models.IntegerField(default=False)

    company = models.CharField(max_length=40, default=None)
    city = models.CharField(max_length=30,default=None)
    zipcode = models.FloatField(default=False)
    address = models.TextField(max_length=400, default=None)

def __str__(self):
    return self.user.username

def get_delete_address(self):
    return reverse ("ESite_App:delete_address"
    )

class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40, default=None)
    last_name = models.CharField(max_length=40, default=None)
    company = models.CharField(max_length=40, default=None)
    city = models.CharField(max_length=30,default=None)
    zipcode = models.FloatField(default=False)
    address = models.TextField(max_length=400, default=None)
    phone_number = models.IntegerField(default=False)
def __str__(self):
    return self.user.username

def get_absolute_url(self):
    return reverse("ESite_App:store")