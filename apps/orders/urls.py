from django.conf.urls import url, include
from .views import MyOrderView, CheckoutView,PaymentView,PaySuccessView, ConfirmReceiveView, FinishView,DeliveryAddressView
from .views import GoToPayView,PayView,UrgeDeliveryView


urlpatterns = [
    url(r'^myOrders$', MyOrderView.as_view(),name="myOrders"),
    url(r'^checkout$', CheckoutView.as_view(), name="checkout"),
    url(r'^payment$', PaymentView.as_view(), name="payment"),
    url(r'^paySuccess$', PaySuccessView.as_view(), name="paySuccess"),
    url(r'^confirmReceive$', ConfirmReceiveView.as_view(), name="confirmReceive"),
    url(r'^finish$', FinishView.as_view(), name="finish"),
    url(r'^deliveryAddress$', DeliveryAddressView.as_view(), name='deliveryAddress'),
    url(r'goToPay$', GoToPayView.as_view(), name='gotopay'),
    url(r'pay$',PayView.as_view(),name='pay'),
    url(r'urgeDelivery$', UrgeDeliveryView.as_view(), name='urge'),

]