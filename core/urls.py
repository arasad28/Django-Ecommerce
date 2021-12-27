from django.urls import path
from .views import HomeView,ItemDetails,add_to_cart,TestView,OrderSummaryView,remove_from_cart,remove_single_item_from_cart,CheckoutView,AddressView,search,mobile_cat,laptop_cat,electronics_cat


app_name = 'core'

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('product/<slug>/',ItemDetails.as_view(),name='product'),
    path('test/',TestView.as_view(),name = 'test'),
    path('add-to-cart/<slug>/',add_to_cart,name='add'),
    path('search/',search,name='search'),
    path('category/mobile',mobile_cat,name='mobile'),
    path('category/laptop',laptop_cat,name='laptop'),
    path('category/electronics',electronics_cat,name='electronics'),
    path('remove-from-cart/<slug>/',remove_from_cart,name="remove"),
    path('remove-item-from-cart/<slug>/',remove_single_item_from_cart,name='remove_single_from_cart'),
    path('cart/',OrderSummaryView.as_view(),name='cart'),
    path('checkout/',CheckoutView.as_view(),name='checkout'),
    path('address/',AddressView.as_view(),name='address'),
]

