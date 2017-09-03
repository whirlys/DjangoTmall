from django import forms
from .models import TmallShop
from products.models import Product


class TmallShopForm(forms.ModelForm):
    class Meta:
        model = TmallShop
        exclude = ['owner','is_active','created','updated']
        fields = ['type','shopName','companyInfo','scope','location','businessLicense','is_active']


class ProductForm(forms.ModelForm):

    """
    添加新产品
    """
    class Meta:
        model = Product
        exclude = ['shop','product_code','stock','monthlyVolume','commentNum','sales','created','updated']
        fields = ['category','brand','product_name','subTitle','original_price','price','cost','publish_status','description','is_freeShipping']
        # widgets = {
        #     'category': (attrs={'cols': 80, 'rows': 20}),
        # }


