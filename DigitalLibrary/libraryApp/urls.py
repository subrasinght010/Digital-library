from django.urls import path
from libraryApp import views
from .forms import LoginForm,CheckoutForm
from django.conf import settings
from django.conf.urls.static import static
from .views import (
                    add_to_cart_issue,add_to_cart,
                    ItemDetailView,PaymentView,
                    CheckoutView,OrderSummaryView,
                    remove_single_item_from_cart_issue,
                    remove_single_item_from_cart,
                    remove_from_cart_issue,
                    remove_from_cart
                    )
from django.contrib.auth import views as auth_views

app_name = 'libraryApp'

urlpatterns = [
    path('', views.HomeView.as_view(),name='home'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('account/login/',auth_views.LoginView.as_view(template_name="libraryApp/login.html",authentication_form=LoginForm),name='login'),
    path('signup/', views.UserRegistrationView.as_view(),name='signup'),
    path('order-summary/',views.OrderSummaryView.as_view(), name='order-summary'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-to-cart-issue/<slug>/', add_to_cart_issue, name='add-to-cart-issue'),
    path('productdetail/<slug>/', ItemDetailView.as_view(), name='productdetail'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-from-cart_issue/<slug>/', remove_from_cart_issue, name='remove-from-cart-issue'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,name='remove-single-item-from-cart'),
    path('remove_single_item_from_cart_issue/<slug>/', remove_single_item_from_cart_issue,name='remove-single-item-from-cart-issue'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),

]
"""path('Passwordchange/',auth_views.LoginView.as_view(template_name="libraryApp/Passwordchange.html",form_class=PasswordchangeForm),name='Passwordchange'),"""
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
