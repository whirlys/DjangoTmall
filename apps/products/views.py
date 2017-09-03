from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import get_object_or_404
from .models import Category,Product,Cart
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import logging


# Get an instance of a logger
logger = logging.getLogger('django')


class CategoryView(View):
    """
    跳转到分类页
    """
    def get(self,request):
        cid = request.GET.get("cid","0")
        category = get_object_or_404(Category,id=cid)
        return render(request,'category.html',{"category":category})


class ProductView(View):
    """
    跳转到产品列表页
    """
    def get(self,request):
        pid = request.GET.get("pid","0")
        product = get_object_or_404(Product,id=pid)
        image = product.productImages.filter(type='image')
        detailImage = product.productImages.filter(type='detailImage')
        return  render(request,'product.html',{"product":product,"image":image,"detailImage":detailImage})


class CartView(LoginRequiredMixin ,View):
    """
    跳转到购物车页面
    """
    def get(self,request):
        carts = Cart.objects.filter(user=request.user)
        return render(request,'cart.html',{'carts':carts})


class SearchView(View):
    def get(self,request):
        return render(request, 'search.html')



def cart_add(request):
    if not request.user.is_authenticated():
        return JsonResponse({"status":"no","reason":"用户未登录，不能添加购物车！"})
    pid = request.POST.get('pid',"")
    if not pid:
        return JsonResponse({"status":"no","reason":"产品不存在"})
    product = Product.objects.filter(id=pid).first()
    if not product:
        return JsonResponse({"status":"no","reason":"该产品不存在！"})

    amount = int(request.POST.get('amount',1))
    add_price = request.POST.get('add_price','')
    if add_price == '':
        return JsonResponse({"status":"no","reason":"添加时的价格不存在"})

    carts = Cart.objects.filter(user=request.user)
    for cart in carts:
        if product.id == cart.product.id:
            cart.amount = cart.amount + amount
            cart.save()
            return JsonResponse({"status": "ok"})

    cart = Cart()
    cart.user=request.user
    cart.product=product
    cart.amount=amount
    cart.add_price=add_price

    cart.save()

    return JsonResponse({"status":"ok"})


def cart_minus_plus(request):
    """
    购物车操作，加一或减一，若购物车减少一个，最后的数目不小于0
    """
    if not request.user.is_authenticated():
        return JsonResponse({"status":"no","reason":"用户未登录，不能操作购物车！"})

    action=request.POST.get('action','')
    if action != 'minus' and action != 'plus':
        return JsonResponse({"status": "no", "reason": "购物车无操作！"})

    cid = request.POST.get('cid','')
    if not cid:
        return JsonResponse({"status":"no","reason":"购物车不存在"})
    cart = Cart.objects.filter(user=request.user,id=cid).first()
    if not cart:
        return JsonResponse({"status":"no","reason":"该购物车不存在！"})

    if action == 'minus':
        if cart.amount ==1:
            pass
        else:
            cart.amount = cart.amount - 1
            cart.save()
    else:
        cart.amount = cart.amount + 1
        cart.save()

    return JsonResponse({"status": "ok"})


def cart_delete(request):
    """
    ajax删除购物车
    :param request:
    :return:
    """
    if not request.user.is_authenticated():
        return JsonResponse({"status":"no","reason":"用户未登录，不能操作购物车！"})

    cid = request.POST.get('cid', '')
    if not cid:
        return JsonResponse({"status": "no", "reason": "购物车不存在"})
    cart = Cart.objects.filter(user=request.user, id=cid).first()
    if not cart:
        return JsonResponse({"status": "no", "reason": "该购物车不存在！"})

    cart.delete()
    return JsonResponse({"status": "ok"})
