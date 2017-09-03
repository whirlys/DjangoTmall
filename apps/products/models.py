from django.db import models
from django.core.urlresolvers import reverse
import datetime
from users.models import UserProfile
from salers.models import TmallShop


class Category(models.Model):
    """
    产品的分类，这里只有一级分类
    """
    category_name = models.CharField(verbose_name="分类名称", max_length=50)
    category_code = models.CharField(verbose_name="分类编码", max_length=30, unique=True)
    image = models.ImageField(upload_to="image/CategoryImage/%Y/%m",verbose_name="类别图片",max_length=100, default="")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse('products:category', kwargs={'pk': self.pk})

    class Meta():
        ordering = ('-created',)
        verbose_name = '产品类别'
        verbose_name_plural = '产品类别'  # 修改管理级页面显示


class Brand(models.Model):
    """
    产品的品牌
    """
    category = models.ForeignKey(Category, related_name='brands', verbose_name='所属类别')
    brand_name = models.CharField(verbose_name='品牌名称', max_length=30)
    telephone = models.CharField(verbose_name='联系电话',max_length=15)
    brand_web = models.CharField(verbose_name='官方网站', max_length=100)
    brand_logo = models.ImageField(verbose_name='品牌logo', upload_to='image/logo/%Y', max_length=100)
    brand_desc = models.CharField(verbose_name='品牌描述', max_length=200)
    brand_status = models.CharField(verbose_name='状态', max_length=10, choices=(("enable","启用"), ("disable","禁用")),default="enable")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.brand_name

    class Meta():
        ordering = ('-created',)
        verbose_name = '产品品牌'
        verbose_name_plural = '产品品牌'

    # def get_absolute_url(self):
    #     return reverse('LessonPlay', args=(self.id,))


class Product(models.Model):
    """
    产品
    """
    shop = models.ForeignKey(TmallShop, related_name='products', verbose_name='所属的商铺')
    product_code = models.CharField(verbose_name="编码", max_length=30)
    product_name = models.CharField(verbose_name="名称", max_length=50)
    subTitle = models.CharField(verbose_name="小标题", max_length=50)
    category = models.ForeignKey(Category, related_name="products", verbose_name="类别")
    brand = models.ForeignKey(Brand, related_name="products", verbose_name="品牌")
    original_price = models.DecimalField(verbose_name="原始价格", max_digits=6, decimal_places=2)
    price = models.DecimalField(verbose_name="促销价格", max_digits=6, decimal_places=2)
    cost = models.DecimalField(verbose_name="进货成本", max_digits=6, decimal_places=2)
    publish_status = models.CharField(verbose_name="上下架状态", max_length=5,choices=(("up","上架"),("down","下架")),default="down")
    description = models.CharField(verbose_name="描述", max_length=100, default="")
    stock = models.IntegerField(verbose_name="库存量", default=0)
    monthlyVolume = models.IntegerField(verbose_name="月成交量",default=0)
    commentNum = models.IntegerField(verbose_name="评论数",default=0)
    sales = models.IntegerField(verbose_name="销量",default=0)
    is_freeShipping = models.BooleanField(verbose_name='是否包邮',default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.product_code+"-"+self.product_name

    def get_absolute_url(self):
        return reverse('products:product', kwargs={'pk': self.pk})

    class Meta():
        ordering = ('-created',)
        verbose_name = '产品'
        verbose_name_plural = '产品'

    # def get_absolute_url(self):
    #     return reverse('LessonPlay', args=(self.id,))


class Property(models.Model):
    """
    产品属性，每个分类规定了该该分类下的所有商品的产品属性，即是商品详情下的产品参数
    """
    category = models.ForeignKey(Category, related_name="propertys", verbose_name="所属类别")
    name = models.CharField(verbose_name="属性名",max_length=10)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = '产品属性'
        verbose_name_plural = '产品属性'


    # def get_absolute_url(self):
    #     return reverse('LessonPlay', args=(self.id,))


class Propertyvalue(models.Model):
    """
    产品属性值：即分类下的所有商品各自的商品参数的值，每个产品的属性值和分类下的属性为一对一
    """
    property = models.ForeignKey(Property, related_name="propertyValues", verbose_name="属性值")  #,limit_choices_to={"category":self.product.category}
    product = models.ForeignKey(Product, related_name="propertyValues", verbose_name="所属产品")
    value = models.CharField(verbose_name="属性值", max_length=150)

    def __str__(self):
        return self.value

    class Meta():
        verbose_name = '属性值'
        verbose_name_plural = '属性值'

    # def get_absolute_url(self):
    #     return reverse('LessonPlay', args=(self.id,))


class ProductImage(models.Model):
    """
    产品的图片：有两种类型，一种是轮播图片，一种是商品详情下的图片
    """
    product = models.ForeignKey(Product, related_name="productImages", verbose_name="所属产品")
    type = models.CharField(verbose_name="类型", choices=(("image","产品图片"),("detailImage","详情图片")), max_length=11)
    image = models.ImageField(upload_to="image/productImage/%Y/%m/%d", verbose_name="图片", max_length=100)

    def __str__(self):
        return self.image.path

    class Meta():
        verbose_name = '产品图片'
        verbose_name_plural = '产品图片'

    # def get_absolute_url(self):
    #     return reverse('LessonPlay', args=(self.id,))


# class Comment(models.Model):
#     product = models.ForeignKey(Product, related_name="comments", verbose_name="所属产品")
#



# class Cart(models.Model):
#     """
#     购物车：一个用户有一个购物车，一个购物车有多个购物车项
#     """
#     user = models.OneToOneField(UserProfile, related_name="cart", verbose_name="所属用户")


class Cart(models.Model):
    """
    购物车项，一个购物车项对应一个产品
    """
    user = models.ForeignKey(UserProfile, related_name="cart", verbose_name="所属用户")
    product = models.ForeignKey(Product, related_name="cartItem",verbose_name="对应产品")
    amount = models.IntegerField(verbose_name="数量")
    add_price = models.DecimalField(verbose_name="添加时的价格", max_digits=6, decimal_places=2)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    def __str__(self):
        return str(self.amount) + " * " + self.product.product_name

    class Meta():
        ordering = ['-add_time']
        verbose_name = '购物车'
        verbose_name_plural = '购物车'


