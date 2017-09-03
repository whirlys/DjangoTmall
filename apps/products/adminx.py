from .models import Category,Brand,Product,Property,Propertyvalue,ProductImage, Cart
import xadmin

from .actions import OffTheShelfAction



class PropertyInline(object):
    model = Property
    extra = 0


class PropertyvalueInline(object):
    model = Propertyvalue
    extra = 0


class ProductImageInline(object):
    model = ProductImage
    extra = 0


class BrandInfoAdmin(object):
    list_display = ['category','brand_name','telephone','brand_web','brand_desc','brand_status']
    search_fields = ['brand_name']
    list_filter = ['created','brand_status']
    list_editable = [ 'brand_name','brand_status']


class PropertyAdmin(object):
    list_display = ['category','name']
    search_fields = ['name']
    list_filter = ['category']
    list_editable = ['category','name']


class PropertyvalueAdmin(object):
    list_display = ['property','product','value']
    search_fields = ['value']
    list_editable = [ 'value']


class ProductImageAdmin(object):
    list_display=['product','type','image']
    list_filter = ['type']


class CategoryAdmin(object):
    list_display = ['category_name','category_code','created','updated']
    search_fields = ['category_name','category_code']
    list_filter = ['created','updated']
    inlines = [PropertyInline,]
    # data_charts = {
    #     "按类别统计": {'title': "按类别统计", "x-field": "category_name", "y-field": ("products.count"),
    #               "order": ('created',)}
    # }



class ProductAdmin(object):
    list_display = ['product_name','product_code','subTitle','category','brand','original_price','price','cost','publish_status','stock','updated']
    search_fields = ['product_name','product_code','subTitle']
    list_filter = ['created','publish_status']
    inlines = [ PropertyvalueInline, ProductImageInline,]
    actions = [OffTheShelfAction,]
    list_editable = [ 'subTitle','price','publish_status']

    # list_bookmarks = [{
    #     'title': "产品书签test",  # 书签的名称, 显示在书签菜单中
    #     'query': {'product_name': False},  # 过滤参数, 是标准的 queryset 过滤
    #     'order': ('-created',),  # 排序参数
    #     'cols': ('product_name','product_code','subTitle','category','brand','original_price','price','cost','publish_status','stock','updated',),  # 显示的列
    #     'search': '扫地'  # 搜索参数, 指定搜索的内容
    # }
    # ]

    # list_export = ('xls', 'xml', 'json', 'csv')
    # show_detail_fields = ['subTitle']

    # wizard_form_list = [
    #     ("第一步", ("product_name", "product_code","subTitle")),
    #     ("第二步", ("category", "brand", "address")),
    #     ("第三步", ('original_price','price','cost','publish_status','stock',))
    # ]

    readonly_fields = ["updated","created","sales","commentNum","monthlyVolume"]

    # form_layout = (
    #     Main(
    #
    #     )
    # )



class CartAdmin(object):
    list_display = ['user', 'product','amount','add_price','add_time']
    search_fields = ['user']
    list_filter = ['add_time']
    refresh_times = (3, 5)

    show_detail_fields = ['user', 'add_price']
    # list_bookmarks = [
    #     {
    #         'title': "书签一",  # 书签的名称, 显示在书签菜单中
    #         'query': {'user': True},  # 过滤参数, 是标准的 queryset 过滤
    #         'order': ('-add_time'),  # 排序参数
    #         'cols': ('first_name'),  # 显示的列
    #         'search': 'whirly'  # 搜索参数, 指定搜索的内容
    #     },
    # ]
    list_editable = [ 'amount']



xadmin.site.register(Category,CategoryAdmin)
xadmin.site.register(Brand,BrandInfoAdmin)
xadmin.site.register(Product,ProductAdmin)
xadmin.site.register(Property,PropertyAdmin)
xadmin.site.register(Propertyvalue,PropertyvalueAdmin)
xadmin.site.register(ProductImage,ProductImageAdmin)
xadmin.site.register(Cart, CartAdmin)