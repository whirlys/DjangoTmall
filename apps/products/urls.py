from django.conf.urls import url, include
from .views import CategoryView,ProductView,CartView,SearchView,cart_add,cart_minus_plus, cart_delete

urlpatterns = [
    url(r'^category$', CategoryView.as_view(),name="category"),
    url(r'^product$',ProductView.as_view(),name="product"),
    url(r'^cart$',CartView.as_view(),name="cart"),
    url(r'^search$', SearchView.as_view(),name="search"),
    url(r'^add_cart$',cart_add, name='add_cart'),
    url(r'cart_minus$', cart_minus_plus, name='cart_minus_plus'),
    url(r'cart_delete$', cart_delete, name='cart_delete'),
]