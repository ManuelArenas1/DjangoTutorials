from django.urls import path
from .views import homePageView, aboutPageView, contactPageView, productIndexView, productShowView, productCreateView, cartRemoveAllView, cartView

urlpatterns = [
    path('', homePageView.as_view(), name ='home'),
    path('about/', aboutPageView.as_view(), name='about'),
    path('contact/', contactPageView.as_view(), name='contact'),
    path('products/', productIndexView.as_view(), name='products'),
    path('products/<str:id>/', productShowView.as_view(), name='show'),
    path('products/create', productCreateView.as_view(), name='product-create'),
    path('products/<str:id>', productShowView.as_view(), name='show'),
    path('cart/', cartView.as_view(), name='cart_index'),
    path('cart/add/<str:product_id>', cartView.as_view(), name='cart_add'),
    path('cart/removeAll', cartRemoveAllView.as_view(), name='cart_removeAll'),
    
]