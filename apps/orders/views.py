from django.shortcuts import render
from django.views.generic import  View
from .forms import DeliveryAddressForm
from .models import DeliveryAddress
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse,Http404
from django.core.urlresolvers import reverse
from products.models import Cart
from .models import Order,OrderItem
from utils.utils import order_code_format
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from notifications.signals import notify
from users.models import UserProfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



class MyOrderView(LoginRequiredMixin, View):
    def get(self,request):
        orders = Order.objects.filter(user=request.user)
        paginator = Paginator(orders, 10)  # 每页10条记录
        page = request.GET.get("page", 1)
        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)
        return render(request, 'orders.html', {'orders':orders})


class CheckoutView(View):
    def get(self,request):
        dAddress = DeliveryAddress.objects.filter(user=request.user)

        cids = request.GET.getlist('cid', [])

        total_money = 0

        carts = []
        for cid in cids:
            cart = Cart.objects.filter(user=request.user,id=cid).first()

            if cart:
                total_money = total_money + cart.amount * cart.product.price
                carts.append(cart)

        return render(request, 'checkout.html',{'dAddress':dAddress,'carts':carts,"total_money":total_money})



class PaymentView(View):
    """
    提交订单后，生成订单，跳转到支付页面
    有多个商品时，生成订单时根据商家的不同，可能生成多张订单
    """
    def post(self,request):
        daid = request.POST.get('daid',"")

        address = get_object_or_404(DeliveryAddress, user=request.user,id=daid)
        if not address:
            return HttpResponse("收货地址错误！")

        cids = request.POST.getlist('cid',[])
        orderitems = []
        carts = []
        shops = []

        total_money = 0
        for cid in cids:
            cart = get_object_or_404(Cart,user=request.user,id=cid)
            if cart:
                carts.append(cart)

                total_money = total_money + cart.amount * cart.product.price

                orderitem = OrderItem()
                orderitem.product=cart.product
                orderitem.product_name=cart.product.product_name
                orderitem.product_num=cart.amount
                orderitem.product_price=cart.product.price

                orderitems.append(orderitem)

                if cart.product.shop not in shops:
                    shops.append(cart.product.shop)

            else:
                return HttpResponse("订单错误！")

        if len(orderitems) == 0:
            return HttpResponse("没有订单项！")

        orderlist = []

        for shop in shops:
            order = Order()
            order.order_code = order_code_format(request.user.id)
            order.shop = shop
            order.user = request.user
            order.receiver = address.receiver
            order.address = address.province + ' ' + address.city + ' ' + address.town + ' ' + address.address
            order.phoneNumber = address.phoneNumber
            order.amount = total_money
            order.discount_amount = 0
            order.courier_amount = 0
            order.payment_money = 0  # order.amount # + order.courier_amount - order.discount_amount
            order.order_status = 1
            order.order_point = 0
            order.is_active = True

            order.save()
            orderlist.append(order)

        for orderitem in orderitems:
            for order in orderlist:
                if order.shop == orderitem.product.shop:
                    orderitem.order = order
                    orderitem.save()
                    break

        for cart in carts:
            cart.delete()

        system = UserProfile.objects.filter(id=1).first()
        for order in orderlist:
            notify.send(sender=system, recipient=request.user, verb="您已提交订单，订单号为"+order.order_code)

        return  render(request, "payment.html",{"total_money":total_money,"oid":order.id})


class GoToPayView(LoginRequiredMixin,View):
    """
    跳转到支付页面
    """
    def get(self,request):
        oid = request.GET.get('oid',"")
        if not oid:
            return HttpResponse("订单错误！")

        order=Order.objects.filter(user=request.user, id=oid).first()
        if not order:
            return HttpResponse("订单不存在！")

        if order.order_status != '1':
            return render(request, 'payed.html')

        total_money = order.payment_money
        return render(request, "payment.html", {"total_money": total_money,"oid":order.id})



class PayView(LoginRequiredMixin, View):
    """支付"""
    def post(self,request):
        order_id = request.POST.get('oid',"")
        if not order_id:
            return JsonResponse({"status":"no","reason":"支付失败！"})

        order = Order.objects.filter(user=request.user, id=order_id).first()
        if not order:
            return JsonResponse({"status": "no", "reason": "订单不存在, 支付失败！"})

        if order.order_status == '1':
            order.order_status = '2' # 订单状态修改为代发货
        else:
            return JsonResponse({"status": "no", "reason": "订单已支付, 不能重复支付！"})

        order.payment_money = order.amount + order.courier_amount - order.discount_amount
        order.payment_method = '4'  # 支付宝
        order.pay_time = datetime.datetime.now()

        order.order_point = order.payment_money / 100  # 订单积分为支付金额的100分之一

        order.save()

        system = UserProfile.objects.filter(id=1).first()
        notify.send(sender=system, recipient=request.user, verb="支付成功，订单号为" + order.order_code+"，支付金额为"+str(order.payment_money))
        return JsonResponse({"status":"ok"})



class PaySuccessView(LoginRequiredMixin,View):
    """
    支付成功
    """
    def get(self, request):
        oid = request.GET.get('oid',"")
        if not oid:
            raise Http404("订单不存在！")
        order = get_object_or_404(Order,user=request.user,id=oid)
        if not order:
            raise Http404("订单不存在！")

        if order.order_status == '1':
            return HttpResponseRedirect(reverse('gotopay',{"oid":oid}))

        return render(request, "paySuccess.html")


class UrgeDeliveryView(View):
    """
    催卖家发货
    """
    def post(self,request):
        oid = request.POST.get('oid',"")
        if not oid:
            return JsonResponse({"status":"no","reason":"订单不存在"})
        order = Order.objects.filter(user=request.user, id=oid).first()
        if not order:
            return JsonResponse({"status": "no", "reason": "订单不存在, 支付失败！"})

        # 暂时由系统管理员充当卖家
        seller = UserProfile.objects.filter(id=1).first()
        notify.send(sender=seller, recipient=request.user, verb='听说你催了卖家发货？找事？')
        return JsonResponse({"status":"ok"})


class ConfirmReceiveView(LoginRequiredMixin,View):
    """
    确认收货
    """
    def get(self, request):
        oid = request.GET.get('oid', "")
        if not oid:
            return JsonResponse({"status": "no", "reason": "订单号不存在"})
        order = Order.objects.filter(user=request.user, id=oid).first()
        if not order:
            return JsonResponse({"status": "no", "reason": "订单不存在！"})

        return render(request, "confirmReceive.html",{"order":order})

    def post(self,request):
        oid = request.GET.get('oid', "")
        if not oid:
            return JsonResponse({"status": "no", "reason": "订单号不存在"})
        order = Order.objects.filter(user=request.user, id=oid).first()
        if not order:
            return JsonResponse({"status": "no", "reason": "订单不存在！"})

        if order.order_status != "3":
            return HttpResponse("订单状态不为待收货状态！不能收货！")

        order.order_status = "4"
        order.receive_time = datetime.datetime.now()
        order.save()
        return render(request, 'finish.html')


class FinishView(View):
    def get(self, request):
        return render(request, "finish.html")


class DeliveryAddressView(View):
    """
    管理收货地址
    """
    def get(self,request):
        deliveryAddress = DeliveryAddress.objects.filter(user=request.user)

        delete=request.GET.get('delete',"")
        if delete:
            self.delete(request, delete)
            return render(request,'deliveryAddress.html',{"deliveryAddress":deliveryAddress})

        daid = request.GET.get('daid',"")
        if daid:
            editAddress = get_object_or_404(DeliveryAddress,user=request.user,id=daid)
            return render(request, 'deliveryAddress.html',{"editAddress":editAddress,"deliveryAddress":deliveryAddress})
        else:
            return render(request,'deliveryAddress.html',{"deliveryAddress":deliveryAddress})

    def post(self, request):
        deliveryAddressForm = DeliveryAddressForm(request.POST)
        # deliveryAddressForm.user
        if deliveryAddressForm.is_valid():

            daid = request.GET.get('daid','')
            if daid:
                editAddress = get_object_or_404(DeliveryAddress, user=request.user, id=daid)

                editAddress.receiver = deliveryAddressForm.cleaned_data.get('receiver')
                editAddress.phoneNumber = deliveryAddressForm.cleaned_data.get('phoneNumber')
                editAddress.zip = deliveryAddressForm.cleaned_data.get('zip')
                editAddress.province = deliveryAddressForm.cleaned_data.get('province')
                editAddress.city = deliveryAddressForm.cleaned_data.get('city')
                editAddress.town = deliveryAddressForm.cleaned_data.get('town')
                editAddress.address = deliveryAddressForm.cleaned_data.get('address')

                if deliveryAddressForm.cleaned_data.get('is_default'):
                    dAddress = DeliveryAddress.objects.filter(user=request.user)
                    for address in dAddress:
                        address.is_default = False
                        address.save()

                editAddress.is_default = deliveryAddressForm.cleaned_data.get('is_default')

                editAddress.save()

            else:
                deliveryAddress = DeliveryAddress()
                deliveryAddress.user = request.user

                deliveryAddress.receiver = deliveryAddressForm.cleaned_data.get('receiver')
                deliveryAddress.phoneNumber = deliveryAddressForm.cleaned_data.get('phoneNumber')
                deliveryAddress.zip = deliveryAddressForm.cleaned_data.get('zip')
                deliveryAddress.province = deliveryAddressForm.cleaned_data.get('province')
                deliveryAddress.city = deliveryAddressForm.cleaned_data.get('city')
                deliveryAddress.town = deliveryAddressForm.cleaned_data.get('town')
                deliveryAddress.address = deliveryAddressForm.cleaned_data.get('address')

                if deliveryAddressForm.cleaned_data.get('is_default'):
                    dAddress = DeliveryAddress.objects.filter(user=request.user)
                    for address in dAddress:
                        address.is_default = False
                        address.save()

                deliveryAddress.is_default = deliveryAddressForm.cleaned_data.get('is_default')

                deliveryAddress.save()


        return HttpResponseRedirect(reverse('orders:deliveryAddress'))


    def delete(self,request, daid):
        deleteAddress = get_object_or_404(DeliveryAddress, user=request.user,id=daid)

        deleteAddress.delete()

        return HttpResponseRedirect(reverse('orders:deliveryAddress'))


