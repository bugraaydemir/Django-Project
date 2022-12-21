from django.contrib import admin
from django.urls import include, path
from ESite_App import views
from django.conf.urls.static import static
from django.conf import settings
from .views import CampingTentView, ClothingView, CookingView, ItemView, LandingPageView, StoreView,OrderSummaryView, SurvivalGadgetsView,add_to_cart, add_to_order, decrease_from_cart, remove_from_cart, shipping_and_billing, usersettingsview 
app_name = 'ESite_App'
urlpatterns = [

    path('admin/', admin.site.urls),
    path('home', LandingPageView.as_view() , name="home"),
    path('store/', StoreView.as_view() , name="store"),
    path('order/', OrderSummaryView.as_view() , name="order"),

    path('store/<slug>/', ItemView.as_view() , name="store"),
    path('Camping-Tents/', CampingTentView.as_view() , name="CampingTents"),
    path('Survival-Gadgets/', SurvivalGadgetsView.as_view(), name="Survival-Gadgets"),
    path('Clothing/', ClothingView.as_view(), name="Clothing"),
    path('Cooking/', CookingView.as_view(), name="Cooking"),

    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('add_to_order/<slug>/', add_to_order, name='add_to_order'),

    path('decrease_from_cart/<slug>/', decrease_from_cart, name='decrease_from_cart'),

    path('', views.LandingPageView.as_view() , name="home"),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('login/', views.login_request, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout_request, name= "logout"),
    path('email-change/',views.change_email, name= "email-change"),
    path('password-change/',views.password_change, name= "password-change"),
    path('change-address/',views.change_address, name= "change_address"),
    path('delete-address/',views.delete_address, name= "delete_address"),

    path('add-address/',views.add_address, name= "add-address"),
    path('shipping-address/',shipping_and_billing.as_view(), name= "add-address"),

    path('myprofile/',views.myprofile, name= "myprofile"),
    path('usersettings/', usersettingsview.as_view(), name= "usersettings"),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)