from django.urls import path
from .views import homePageView, aboutPageView, contactPageView, productIndexView, productShowView, productCreateView

urlpatterns = [
    path('', homePageView.as_view(), name ='home'),
    path('about/', aboutPageView.as_view(), name='about'),
    path('contact/', contactPageView.as_view(), name='contact'),
    path('products/', productIndexView.as_view(), name='products'),
    path('products/<str:id>/', productShowView.as_view(), name='show'),
    path('products/create', productCreateView.as_view(), name='product-create'),
    path('products/<str:id>', productShowView.as_view(), name='show'),
    
]