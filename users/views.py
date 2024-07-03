from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import CustomUserSerializer, CustomAuthTokenSerializer
from django.views.generic import TemplateView,ListView,View,DetailView
from .forms import CustomUserCreationForm
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth import login as auth_login 
from django.http import JsonResponse
from .models import Product, Category, Order,CartItem,OrderItem
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import logout


class CustomUserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        auth_login(request, user)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return redirect('home')

class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        view = CustomAuthToken.as_view()
        response = view(request, *args, **kwargs)
        
        if response.status_code == 200:
            return redirect('home') 
        return response  
    
class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('login_page'))
    
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('login_page'))

class SignupView(TemplateView):
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CustomUserCreationForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_page')  
        return self.render_to_response(self.get_context_data(form=form))


class HomeView(TemplateView):
    template_name = 'home.html'



class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        for category in categories:
            category.products = Product.objects.filter(category=category)
        context['categories'] = categories
        return context

class OrderCreateView(View):
    def post(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(user=request.user)
        
        order = Order.objects.create(user=request.user)

        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )

        
        cart_items.delete()

        return redirect('order_success_page')
    
class OrderSuccessView(TemplateView):
    template_name = 'order_success.html'    

    
class AddToCartView(TemplateView):
    template_name = 'product_list.html'  

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, pk=product_id)

        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        messages.success(request, f"{product.name} added to cart.")

        
        return redirect('product_list')

class CartView(TemplateView):
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = CartItem.objects.filter(user=self.request.user)
        
        total_amount = 0  
        
        for item in cart_items:
            item.total_price = item.product.price * item.quantity
            total_amount += item.total_price
        
        context['cart_items'] = cart_items
        context['total_amount'] = total_amount
        return context

class PlaceOrderView(View):
    def post(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(user=request.user)

        order = Order.objects.create(user=request.user)

        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )

        cart_items.delete()

        return redirect('order_success_page')
    
class AboutUsView(TemplateView):
    template_name = 'about.html'

class ContactUsView(TemplateView):
    template_name = 'contact.html'



    