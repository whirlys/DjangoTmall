import  xadmin
from .models import TmallShop,LogisticsCompany


class TmallShopAdmin(object):
    list_display = ['owner','type','shopName','companyInfo','scope','location','businessLicense','is_active','created','updated']
    search_fields = ['shopName']
    list_filter = ['companyInfo','is_active','created']


class LogisticsCompanyAdmin(object):
    list_display = ['companyCode','companyName','contact','telphone','price','created','updated']
    search_fields = ['companyCode','companyName','contact','telphone']
    list_filter = ['created','updated']


xadmin.site.register(TmallShop,TmallShopAdmin)
xadmin.site.register(LogisticsCompany,LogisticsCompanyAdmin)