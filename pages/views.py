
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from .models import Product

# Create your views here.
class homePageView(TemplateView):
    template_name = 'pages/home.html'


class aboutPageView(TemplateView):
    template_name = 'pages/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
          "title": "About Us - Online Store",
          "subtitle": "About Us",
          "description": "This is an about page",
          "author": "Developed: by Manuel",   
        })
        return context
    
class contactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
          "title": "Contact  - Online Store",
          "subtitle": "Contact Us",
          "phone": "+57 312 345 6789",
          "email": "contact@onlinestore.com",
          "address": "Calle 123, Bogotá, Colombia"
           
        })
        return context
    


class productIndexView(View):
    template_name = 'pages/products/index.html' 

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "Product List"
        viewData["products"] = Product.objects.all()

        return render(request, self.template_name, viewData)
    
class productShowView(View):
    template_name = 'pages/products/show.html'
    
    
    def get(self, request, id):
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("eL ID del producto debe ser mayor a 1")
            product = get_object_or_404(Product, pk=product_id)
        except (IndexError, ValueError):
            return HttpResponseRedirect(reverse('home'))
        viewData = {}
        product = get_object_or_404(Product, pk=product_id)
        viewData["title"] = product.name + " - Online Store"
        viewData["subtitle"] = product.name + " - Product information"
        viewData["product"] = product
        return render(request, self.template_name, viewData)
    

class productForm(forms.ModelForm):
   class Meta:
    model = Product
    fields = ['name', 'price']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <=0:
            raise forms.ValidationError("Price must be greater than zero")
        return price


class productCreateView(View):
    template_name = 'pages/products/create.html'

    def get(self, request):
        form = productForm()
        viewData = {}
        viewData["title"] = "Create Product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)
    
    def post(self, request):
        form = productForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product-create')
            
           
        else:
            viewData = {}
            viewData["title"] = "Create Product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)
        

class productListView(ListView):
    model = Product
    template_name = 'show.html'
    context_object_name = 'products' # permite el loop en los productos del template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products - Online Store'
        context['Subtitle'] = 'List of products'

        return context


class cartView(View):
    template_name = 'pages/cart/index.html' 

    def get(self, request):
        products = {}
        products[121] = {'name': 'TV Samsung', 'Price': '1000'}
        products[11] = {'name': 'iphone', 'Price': '2000'}


        cart_products = {}
        cart_product_data = request.session.get('cart_product_data', {})


        for key, product in products.items():
            if str(key) in cart_product_data.keys():
                cart_products[key] = product
        
        view_data = {
            'title': 'Cart - Online Store',
            'subtitle': 'Shopping Cart',
            'products': products,
            'cart_products': cart_products
        }

        return render(request, self.template_name, view_data)


    def post(self, request, product_id):
        cart_product_data = request.session.get('cart_product_data',{})
        cart_product_data[product_id] = product_id
        request.session['cart_product_data'] = cart_product_data

        return redirect('cart_index')


class cartRemoveAllView(View):
    def post(self, request):
        if 'cart_product_data' in request.session:
            del request.session['cart_product_data']
        return redirect('cart_index')


def ImageViewFactory(image_storage):
    class ImageView(View):
        template_name = 'pages/images/index.html'


        def get(self, request):
            image_url = request.session.get('image_url', "")
            return render(request, self.template_name, {'image_url': image_url})

        def post(self, request):
            image_url = image_storage.store(request)
            request.session['image_url'] = image_url
            return redirect('image_index')
    return ImageView
    

