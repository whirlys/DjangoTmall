from django.shortcuts import render,redirect
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TmallShopForm, ProductForm
from django.http import HttpResponse,HttpResponseRedirect
from .models import TmallShop,LogisticsCompany
from products.models import Category,Product,ProductImage,Propertyvalue
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from utils.utils import product_code_format
from django.http import JsonResponse
from orders.models import Order
import  datetime


class SalerSupportView(LoginRequiredMixin,View):
    """
    商家入口
    """
    def get(self,request):
        return render(request,'salers/saler-support.html')

class SalerSettledView(LoginRequiredMixin,View):
    """
    商家入驻
    """
    def get(self,request):
        if not request.user.is_saler:
            tmallShopForm = TmallShopForm()
            return render(request, 'salers/apply.html', {'tmallShopForm': tmallShopForm})
        shop = TmallShop.objects.filter(owner=request.user).first()

        if not shop:
            tmallShopForm = TmallShopForm()
            return render(request, 'salers/apply.html', {'tmallShopForm':tmallShopForm})
        elif not shop.is_active:
            return render(request,'salers/waitAudit.html')
        else:
            return HttpResponseRedirect('/saler/manage')


    def post(self,request):
        shop = TmallShop.objects.filter(owner=request.user).first()
        if not shop:
            pass
        elif shop.is_active:
            return HttpResponseRedirect('/saler/manage')
        else:
            return render(request, 'salers/waitAudit.html')
        tmallShopForm = TmallShopForm(request.POST,request.FILES)
        if tmallShopForm.is_valid():
            form = tmallShopForm.save(commit=False)
            form.owner = request.user
            form.save()
            request.user.is_saler = True
            request.user.save()

            return render(request, 'salers/apply.html', {'success': True})

        else:
            return render(request, 'salers/apply.html', {'tmallShopForm': tmallShopForm,"success":False})



class ManageView(View,LoginRequiredMixin):
    """
    商家管理的主页面
    """
    def get(self,request):
        if request.user.is_saler:
            shop = TmallShop.objects.filter(owner=request.user).first()
            if not shop:
                print(shop)
                return HttpResponse('不是商家')
            elif shop.is_active:
                return render(request, 'salers/amz/index.html',{"shop":shop})
            else:
                return render(request, 'salers/waitAudit.html')
        else:
            return HttpResponseRedirect('/saler/joinDjangoTmall')


class MainView(View):
    """
    进入商家管理中心后看到的主页
    """
    def get(self,request):
        return render(request, 'salers/main.html')


class ProductListView(View):
    """
    产品列表
    """
    def get(self,request):
        products = Product.objects.filter(shop=request.user.shop)

        paginator = Paginator(products, 10)  # 每页10条记录
        page = request.GET.get("page", 1)
        try:
            tempPage = paginator.page(page)
        except PageNotAnInteger:
            tempPage = paginator.page(1)
        except EmptyPage:
            tempPage = paginator.page(paginator.num_pages)

        return render(request, 'salers/amz/product-llist.html',{"products":tempPage})


class CategoryListView(View):
    """
    产品分类展示
    """
    def get(self,request):

        categorys= Category.objects.all()
        paginator = Paginator(categorys, 15)  # 每页10条记录
        page = request.GET.get("page", 1)
        try:
            categorys = paginator.page(page)
        except PageNotAnInteger:
            categorys = paginator.page(1)
        except EmptyPage:
            categorys = paginator.page(paginator.num_pages)
        return render(request, 'salers/amz/category.html',{"categorys":categorys})


class ProductCreateView(LoginRequiredMixin,View):
    """添加新产品"""
    def get(self,request):
        productForm = ProductForm()
        return render(request, 'salers/amz/product-add.html',{"productForm":productForm})

    def post(self,request):
        productForm = ProductForm(request.POST)


        if productForm.is_valid():
            # form = productForm.save(commit=False)
            # form.shop = request.user.shop
            # form.product_code = product_code_format(request.user.shop.id)
            # form.save()

            product = Product()

            product.shop = request.user.shop
            product.product_code = product_code_format(request.user.shop.id)
            product.category = productForm.cleaned_data.get('category')
            product.brand = productForm.cleaned_data.get('brand')
            product.product_name = productForm.cleaned_data.get('product_name')
            product.subTitle = productForm.cleaned_data.get('subTitle')
            product.original_price = productForm.cleaned_data.get('original_price')
            product.price = productForm.cleaned_data.get('price')
            product.cost = productForm.cleaned_data.get('cost')
            product.publish_status = productForm.cleaned_data.get('publish_status')
            product.description = productForm.cleaned_data.get('description')
            product.is_freeShipping = productForm.cleaned_data.get('is_freeShipping')

            product.save()

            # modelform保存后获取model?
            for pimage in request.FILES.getlist('pimage'):

                image = ProductImage(product=product, image=pimage, type='image')

                image.save()


            for dimage in request.FILES.getlist('dimage'):

                image = ProductImage(product=product,image=dimage, type='detailImage')
                image.save()

            for property in product.category.propertys.all():
                propertyValue = Propertyvalue()
                propertyValue.property = property
                propertyValue.product = product
                propertyValue.value = ''
                propertyValue.save()


            return render(request, 'salers/amz/propertysForm.html', {'product': product})

        else:
            print(productForm.errors)
            return render(request, 'salers/amz/product-add.html', {"productForm": productForm})


class GetCategoryJson(View):
    def post(self,request):
        """
        添加新的产品的时候，选择一个分类后，返回该分类的属性列表，动态生成属性表单
        """
        cid = request.POST.get('cid','')
        if not cid:
            return JsonResponse({"status":"no","reason":"不存在"})
        category = Category.objects.filter(id=cid).first()

        if not category:
            return JsonResponse({"status": "no", "reason":"类别不存在"})

        data = []

        for brand in category.brands.all():
            temp = {}
            temp['id'] = brand.id
            temp['name'] = brand.brand_name
            data.append(temp)

        return JsonResponse({"status":"ok","brands":data})

class PropertysView(View):
    def get(self,request):
        """
        修改产品属性值PropertysView
        """
        pid = request.GET.get('pid', '')
        if not pid:
            return  HttpResponse("没有pid")
        product = Product.objects.filter(shop=request.user.shop,id=pid).first()
        if not product:
            return HttpResponse("pid对应的产品不存在")
        return render(request,'salers/amz/propertysForm.html',{'product':product})



    def post(self,request):
        pid = request.POST.get('pid','')

        if not pid:
            return JsonResponse({"status":"no","reason":"产品号不存在"})
        product = Product.objects.filter(shop=request.user.shop,id=pid).first()
        if not product:
            return JsonResponse({"status":"no","reason":"产品不存在"})

        pvid = request.POST.get('pvid','')

        if not pvid:
            return JsonResponse({"status":"no","reason":"属性值号不存在"})
        propertyvalue = Propertyvalue.objects.filter(id=pvid,product=product).first()
        if not propertyvalue:
            return JsonResponse({"status":"no","reason":"属性值不存在"})

        value = request.POST.get("value","")
        if not value:
            return JsonResponse({"status":"no","reason":"属性值不能为空"})

        propertyvalue.value = value

        propertyvalue.save()

        return JsonResponse({"status":"ok"})


class OrdersView(LoginRequiredMixin,View):
    """
    商家订单列表，根据参数过滤：未完成，未付款等
    """
    def get(self,request):
        orders = Order.objects.filter(shop=request.user.shop)

        status_num = {}
        status_num['0'] = orders.count()
        status_num['1'] = orders.filter(order_status='1').count()
        status_num['2'] = orders.filter(order_status='2').count()
        status_num['3'] = orders.filter(order_status='3').count()
        status_num['4'] = orders.filter(order_status='4').count()
        status_num['5'] = orders.filter(order_status='5').count()

        status = request.GET.get('status',"")
        if status:
            orders = orders.filter(order_status=status)

        paginator = Paginator(orders, 10)  # 每页10条记录
        page = request.GET.get("page", 1)
        try:
            tempPage = paginator.page(page)
        except PageNotAnInteger:
            tempPage = paginator.page(1)
        except EmptyPage:
            tempPage = paginator.page(paginator.num_pages)

        return render(request,'salers/amz/orders-list.html',{"orders":tempPage,"status_num":status_num})



class DeliverGoodsView(LoginRequiredMixin,View):
    """
    商家点击发货按钮，ajax快速发货，随机获取一个物流公司
    """
    def post(self,request):
        oid = request.POST.get('oid','')
        if not oid:
            return JsonResponse({'status':'no','reason':'订单号不存在！'})

        order = Order.objects.filter(shop=request.user.shop, id=oid).first()
        if not order:
            return JsonResponse({"status":"no","reason":"订单不存在"})

        if order.order_status != '2':
            return JsonResponse({"status":"no","reason":"该订单不处于待发货状态，不能发货！"})

        logisticsCompany = LogisticsCompany.objects.all().order_by('?').first()
        order.courier_company = logisticsCompany.companyName
        order.courier_number = logisticsCompany.getCourierNumber()
        order.deliver_time = datetime.datetime.now()
        order.order_status = '3'

        order.save()

        return JsonResponse({"status":"ok"})