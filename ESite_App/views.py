from datetime import datetime
from django.utils import timezone
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.views import View, generic
import urllib.request as urllib
from ESite_App.forms import  BillingAddressForm, UpdatePassword, UpdateUserAddressForm, UpdateUserForm,ShippingAddressForm
from .models import BackgroundImage, BillingAddress, Item, LandingPageEdit, Logo, Order, OrderItem, ShippingAddress
from django.contrib import messages
from urllib3 import request
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.



class StoreView(ListView) : 
  model =Item
  template_name="ESite/item_list.html"
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['cart'] = OrderItem.objects.filter(user=self.request.user)
    context['background_image'] = BackgroundImage.objects.all()

    return context 
  def get_context_data(self, **kwargs):
    
    try:
      context = super().get_context_data(**kwargs)
      context['logo'] = Logo.objects.all()

      context['object'] = Order.objects.get(user=self.request.user, ordered=False)
      return context 
    except ObjectDoesNotExist:
      messages.warning(self.request, "You do not have an active order")
    return context 

class CampingTentView(ListView) :
  model = Item
  template_name="ESite/Camping-Tents.html"
  def get_context_data(self,**kwargs):
    

    try:
      context = super().get_context_data(**kwargs)
      context['object'] = Order.objects.get(user=self.request.user, ordered=False)
      context['camping_tents'] = Item.objects.filter(category = 'Camping Tent')

      return context 
    except ObjectDoesNotExist:
      messages.warning(self.request, "You do not have an active order")
    return context 

class SurvivalGadgetsView(ListView):
  model=Item
  template_name = "ESite/Survival_Gadgets.html"
  def get_context_data(self,**kwargs):
      context = super().get_context_data(**kwargs)
      context['object'] = Order.objects.get(user = self.request.user, ordered = False)
      context['survival_gadgets'] = Item.objects.filter(category = 'Survival Gadget')
      return context
class ClothingView(ListView):
  model = Item
  template_name = "ESite/Clothing.html"
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['clothing'] = Item.objects.filter(category = 'Clothing')
    return context

class CookingView(ListView):
  model = Item
  template_name = "ESite/Cooking.html"
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['cooking'] = Item.objects.filter(category = 'Cooking')
    return context

    
class ItemView(DetailView) : 
  model =Item
  template_name="ESite/item-add-to-cart.html"
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['cart'] = OrderItem.objects.filter(user=self.request.user)
    return context 
  def get_context_data(self, **kwargs):
    
    try:
      context = super().get_context_data(**kwargs)
      context['object'] = Order.objects.get(user=self.request.user, ordered=False)
      context['background_image'] = BackgroundImage.objects.all()
      context['logo'] = Logo.objects.all()


      return context 
    except ObjectDoesNotExist:
      messages.warning(self.request, "You do not have an active order")
    return context 
 

class LandingPageView(ListView) : 
  model =Item
  template_name="ESite/index.html"
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['cart'] = OrderItem.objects.filter(user=self.request.user)
    return context

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['bestseller'] = Item.objects.filter(bestseller=True)
      context['object'] = Order.objects.get(user = self.request.user, ordered = False)
      context['logo'] = Logo.objects.all()
      context['edit_landing_page'] = LandingPageEdit.objects.all()
      context['background_image'] = BackgroundImage.objects.all()
      return context 

@csrf_exempt
def signup(request):
    
    if request.method == "POST":
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        email = request.POST.get('Email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password2 = request.POST.get('Password2')
        
        if username == '':
          messages.error(request, "Enter a Username!")
          return redirect('/signup')

        if email == '':
          messages.error(request, "Enter a email adress!")
          return redirect('/signup')

        if password == '':
          messages.error(request, "Enter Password!")
          return redirect('/signup')

        if first_name == '':
          messages.error(request, "Enter your name!")
          return redirect('/signup')
        if last_name == '':
          messages.error(request, "Enter your name!")
          return redirect('/signup')

        if User.objects.filter(username=username):
          messages.error(request, "Username already exists!")
          return redirect('/signup')

        if User.objects.filter(email=email):
          messages.error(request, "Email already exists!")
          return redirect('/signup')



        if len(username) < 5:
          messages.error(
        request, "Username must be higher than 4 characters")
        
          return redirect('/signup')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric")
            return redirect('/signup')

        else:
            myuser = User.objects.create_user(username, email, password,first_name = first_name, last_name=last_name)

            myuser.first_name = first_name
            myuser.last_name = last_name
            myuser.save()

        return redirect('/add-address/')



    return render(request,"ESite/signup.html")


@csrf_exempt
def login_request(request):
  context = RequestContext(request)
  if request.method == 'POST':
          username = request.POST['userlog']
          password = request.POST['passlog']
          user = authenticate(username=username, password=password)
          if user is not None:
              if user.is_active:
                  login(request, user)
                  messages.success(request, 'You are succesfully logged in!')
                  return redirect('/store')


  return render(request, "Esite/login.html")           




def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect('/home/')


@login_required(login_url='/login')
def myprofile(request):
  
  return render(request, "ESite/EditProfile/myprofile.html")

class usersettingsview(ListView):
  decorators = [login_required]
  model = ShippingAddress
  template_name = "ESite/EditProfile/User-Settings.html"
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['shippingaddress'] = ShippingAddress.objects.filter(user=self.request.user)
    
    return context
  
@login_required(login_url='/login/')
def delete_address(request):
    address = get_object_or_404(ShippingAddress.objects.filter(user= request.user))
    address.user = request.user
    address.delete()
    return redirect('/usersettings/')  


def change_address(request):
  context ={}
  context ['form'] = UpdateUserAddressForm

  if request.method == 'POST':
    user_form = UpdateUserAddressForm(data=request.POST, instance=request.user)
    if user_form.is_valid():
      user_form.save()
      messages.success(request, 'Your profile is updated successfully')
      return redirect('/myprofile/')
    else:
      user_form = UpdateUserAddressForm(instance=request.user)
      
  return render(request, "Esite/EditProfile/myprofile.html",context)
      
@login_required(login_url='/login')
def change_email(request):
  context ={}
  context['form']= UpdateUserForm()
  try:
    if request.method == 'POST':
  
     user_form = UpdateUserForm(request.POST, instance=request.user)
     if user_form.is_valid():
             user_form.save()
             messages.success(request, 'Your profile is updated successfully')
             return redirect('/myprofile/')
     else:
       user_form = UpdateUserForm(instance=request.user)
  except: HttpResponse("Does Not Exist")
  return render(request, "Esite/EditProfile/myprofile.html",context)




@login_required(login_url='/login')
def password_change(request):
  context ={}
  context['form']= UpdatePassword()

  if request.method == 'POST':
    user_form = UpdatePassword(request.POST)
    if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('/myprofile')
    else:
      user_form = UpdatePassword(instance=request.user)

  return render(request, "Esite/EditProfile/myprofile.html",context)

@login_required
def add_address(request):
  if request.method == 'POST':
    user_form = ShippingAddressForm(request.POST)
    if user_form.is_valid():
      user_form = user_form.save(commit=False)
      user_form.user = request.user
      user_form.save()
      messages.success(request, 'Your profile is updated successfully')
      return redirect('/myprofile/')
  else:
    user_form = ShippingAddressForm(instance=request.user)
  return render(request, "Esite/EditProfile/AddAddress.html", {'form': ShippingAddressForm})


@login_required
def add_to_cart(request, slug):
  item = get_object_or_404(Item, slug=slug)
  order_item, created = OrderItem.objects.get_or_create(
    item=item,
    user=request.user,
    ordered=False
    )
  order_qs = Order.objects.filter(user=request.user, ordered=False)
  if order_qs.exists():
    order = order_qs[0]
    if order.items.filter(item__slug=item.slug).exists():
      order_item.quantity += 1
      order_item.save()
      messages.info(request, "This item quantity was updated.")
      return redirect("ESite_App:store")
    else:
      order.items.add(order_item)
      messages.info(request, "This item was added to your cart.")
      return redirect("ESite_App:store")
  else:
    
    ordered_date = timezone.now()
    order = Order.objects.create(
      user=request.user, ordered_date=ordered_date)
    order.items.add(order_item)
    messages.info(request, "This item was added to your cart.")

    return redirect("ESite_App:store")
class shipping_and_billing(CreateView):
  model = ShippingAddress, BillingAddress
  form_class = BillingAddressForm
  template_name = "ESite/shipping-address.html"
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['shippingaddress'] = ShippingAddress.objects.filter(user=self.request.user)
    return context
  def form_valid(self, form):
    form.instance.user = self.request.user
    form.instance.post_date = datetime.now()
    form.save()
    return redirect('ESite_App:payment')
@login_required
def add_to_order(request, slug):
  item = get_object_or_404(Item, slug=slug)
  order_item, created = OrderItem.objects.get_or_create(
    item=item,
    user=request.user,
    ordered=False
    )
  order_qs = Order.objects.filter(user=request.user, ordered=False)
  if order_qs.exists():
    order = order_qs[0]
    if order.items.filter(item__slug=item.slug).exists():
      order_item.quantity += 1
      order_item.save()
      messages.info(request, "This item quantity was updated.")
      return redirect("ESite_App:order")
    else:
      order.items.add(order_item)
      messages.info(request, "This item was added to your cart.")
      return redirect("ESite_App:order")
  else:
    
    ordered_date = timezone.now()
    order = Order.objects.create(
      user=request.user, ordered_date=ordered_date)
    order.items.add(order_item)
    messages.info(request, "This item was added to your cart.")

    return redirect("ESite_App:order")  
def decrease_from_cart(request,slug):
  item = get_object_or_404(Item, slug=slug)
  order_qs = Order.objects.filter(
    user = request.user,
    ordered = False
  )
  if order_qs.exists():
    order = order_qs[0]
    if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
               
                user=request.user,
                ordered=False
            )[0]
            order_item.quantity -= 1
            order_item.save()
            messages.info(request, "This item was removed from your cart.")
            return redirect("ESite_App:order")
    else:
            messages.info(request, "This item was not in your cart")
            return redirect("ESite_App:store", slug=slug)
  else:
        messages.info(request, "You do not have an active order")
        return redirect("ESite_App:store", slug=slug)

            
@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("ESite_App:store", slug=slug)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("ESite_App:store", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("ESite_App:store", slug=slug)

        


    
class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user = self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'ESite/Ordersummary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/home")
            