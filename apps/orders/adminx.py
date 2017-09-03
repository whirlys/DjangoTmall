import xadmin
from .models import  Order,OrderItem,DeliveryAddress,PointLog


class OrderItemAdmin(object):
    list_display = ['order','product','product_name','product_num','product_price','created','updated']
    search_fields = ['order']
    list_filter = ['created']


class OrderItemInline(object):
    model = OrderItem
    extra = 0


class OrderAdmin(object):
    list_display = ['order_code','shop','user','receiver','address','phoneNumber','payment_method','amount','payment_money','courier_amount','courier_company','courier_number','order_status','is_active']
    search_fields =['order_code']
    list_filter =['order_status','created']
    inlines = [OrderItemInline,]


class DeliveryAddressAdmin(object):
    list_display = ['user','receiver','phoneNumber','zip','province','city','town','address','is_default','created','updated']
    search_fields = ['receiver','phoneNumber']
    list_filter = ['created']


class PointLogAdmin(object):
    list_display =[ 'user','source','order_code','change_point','created']
    search_fields = ['user','order_code']
    list_filter = ['source','created']


xadmin.site.register(Order, OrderAdmin)
xadmin.site.register(OrderItem, OrderItemAdmin)
xadmin.site.register(DeliveryAddress,DeliveryAddressAdmin)
xadmin.site.register(PointLog, PointLogAdmin)