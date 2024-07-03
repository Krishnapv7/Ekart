from django.urls import path, include
from users.views import LoginView,SignupView,HomeView,CustomLogoutView,PlaceOrderView,OrderSuccessView,AboutUsView,ContactUsView,CartView,ProductDetailView,ProductListView,OrderCreateView,CategoryListView,AddToCartView
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    path('login/', LoginView.as_view(), name='login_page'),
    path('signup/', SignupView.as_view(), name='signup_page'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('home/', HomeView.as_view(), name='home'),
    
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('order/', OrderCreateView.as_view(), name='order_create'),
    path('add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('about/', AboutUsView.as_view(), name='about'),
    path('contact/', ContactUsView.as_view(), name='contact'),
     path('place-order/', PlaceOrderView.as_view(), name='place_order'),
    path('order/success/', OrderSuccessView.as_view(), name='order_success_page'),
    
]
