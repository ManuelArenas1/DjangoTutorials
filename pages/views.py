from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.shortcuts import render, redirect

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
    
class Product:
    products = [
        {"id":"1", "name":"TV", "description":"Best TV", "price": 1500},
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": 2000},
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": 500},
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": 300},

    ]

class productIndexView(View):
    template_name = 'pages/products/index.html' 

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "Product List"
        viewData["products"] = Product.products

        return render(request, self.template_name, viewData)
    
class productShowView(View):
    template_name = 'pages/products/show.html'
    
    
    def get(self, request, id):
        try:
            product = Product.products[int(id)-1]
        except (IndexError, ValueError):
            return HttpResponseRedirect(reverse('home'))
        viewData = {}
        product = Product.products[int(id)-1]
        viewData["title"] = product["name"] + " - Online Store"
        viewData["subtitle"] = product["name"] + " - Product information"
        viewData["product"] = product
        return render(request, self.template_name, viewData)
    

class productForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

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
            # coge los datos del formulario 
            name = form.cleaned_data.get('name')
            price = form.cleaned_data.get('price')
            # les genera un nuevo id
            new_id = str(len(Product.products) + 1)
            # crea un nuevo producto
            new_product = {
                "id": new_id,
                "name": name,
                "description": "No description",
                "price": price
            }

            # lo agrega a la lista de productos
            Product.products.append(new_product)
            
            # Muestra el nuevo template
            viewData = {}
            viewData["title"] = "Product Created"
            viewData["product"] = new_product
            return render(request, 'pages/products/success.html', viewData)
        else:
            viewData = {}
            viewData["title"] = "Create Product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)
        
