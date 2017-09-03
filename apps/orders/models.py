from django.db import models
from users.models import UserProfile
from products.models import Product
from salers.models import TmallShop



from users.models import UserProfile


class Order(models.Model):
    """
    订单，每个订单有一个或多个商品
    """
    order_code = models.CharField(verbose_name="订单编号", max_length=30)
    shop = models.ForeignKey(TmallShop, related_name='orders', verbose_name='所属商家')
    user = models.ForeignKey(UserProfile, related_name="orders", verbose_name="所属用户")
    receiver = models.CharField(verbose_name="收货人姓名", max_length=50,null=True,blank=True)
    address = models.CharField(verbose_name="收货地址", max_length=200,null=True,blank=True)
    phoneNumber = models.CharField(verbose_name="手机号码", max_length=11,null=True,blank=True)
    payment_method = models.CharField(verbose_name="支付方式", choices=(("1","现金"),("2","余额"),("3","网银"),("4","支付宝"),("5","微信")), max_length=3,null=True,blank=True)
    amount = models.DecimalField(verbose_name="总金额", max_digits=9, decimal_places=2, default=0)
    discount_amount = models.DecimalField(verbose_name="优惠金额", max_digits=9, decimal_places=2, default=0)
    payment_money = models.DecimalField(verbose_name="支付金额", max_digits=9, decimal_places=2, default=0)
    pay_time =  models.DateTimeField(verbose_name="支付时间", null=True,blank=True)
    deliver_time = models.DateTimeField(verbose_name="发货时间", null=True, blank=True)
    receive_time = models.DateTimeField(verbose_name="收货时间", null=True, blank=True)
    courier_amount = models.DecimalField(verbose_name="运费", max_digits=6, decimal_places=2, default=0)
    courier_company = models.CharField(verbose_name="快递公司", max_length=30, null=True, blank=True)
    courier_number = models.CharField(verbose_name="快递单号", max_length=20, null=True, blank=True)
    order_status = models.CharField(verbose_name="订单状态", choices=(("1","待付款"),("2","待发货"),("3","待收货"),("4","待评价"),("5","已完成")), max_length=3,default=1)
    order_point = models.IntegerField(verbose_name="订单积分", default=0)
    is_active = models.BooleanField(verbose_name='是否激活', default=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="下单时间")
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.order_code

    class Meta():
        ordering = ('-created',)
        verbose_name = '订单'
        verbose_name_plural = '订单'

    def get_orderitem_count(self):
        return self.orderItems.count()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="orderItems", verbose_name="订单项")
    product = models.ForeignKey(Product, related_name="orderItems", verbose_name="订单项")
    product_name = models.CharField(verbose_name="商品名称", max_length=50)
    product_num = models.IntegerField(verbose_name="数量", default=1)
    product_price = models.DecimalField(verbose_name="价格", max_digits=6, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.product_name

    class Meta():
        ordering = ('-created',)
        verbose_name = '订单项'
        verbose_name_plural = '订单项'


class DeliveryAddress(models.Model):
    """
    用户的收货地址
    """
    user = models.ForeignKey(UserProfile, related_name="deliveryAddress",verbose_name="所属用户")
    receiver = models.CharField(verbose_name="收货人姓名", max_length=50)
    phoneNumber = models.CharField(verbose_name="手机号码", max_length=11)
    zip = models.CharField(verbose_name="邮政编码", max_length=10)
    province = models.CharField(verbose_name="省（市区）", max_length=30)
    city = models.CharField(verbose_name="城市", max_length=30)
    town = models.CharField(verbose_name='区域',max_length=30, default="")
    address = models.CharField(verbose_name="详细地址", max_length=100)
    is_default = models.BooleanField(verbose_name='是否默认地址', default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.province + self.city + self.address

    class Meta():
        ordering = ('-created',)
        verbose_name = '收货地址'
        verbose_name_plural = '收货地址'


class PointLog(models.Model):
    """
    用户积分变动日志，记录用户积分的来源，去向
    """
    user = models.ForeignKey(UserProfile, related_name='pointLog', verbose_name='所属用户')
    source = models.CharField(verbose_name='来源或去向', max_length=4,choices=(('1','订单积分'),('2','活动积分'),('3','消费')))
    order_code = models.CharField(verbose_name='来源或去向所属的订单编号',max_length=30,null=True,blank=True)
    change_point = models.IntegerField(verbose_name='变更积分数')
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.user.username + ' ' + self.change_point

    class Meta():
        ordering = ('-created',)
        verbose_name = '积分变更日志'
        verbose_name_plural = '积分变更日志'



# class Returned(models.Model):
#     """
#     用户退货单
#     """


class Comment(models.Model):
    """
    商品评价，限制每个用户对一个订单项的产品只能有一个评价，但可以有多个追评
    """
    product = models.ForeignKey(Product, related_name='comments', verbose_name='所属产品')
    orderItem = models.ForeignKey(OrderItem, related_name='comments', verbose_name='所属订单项')
    user = models.ForeignKey(UserProfile, related_name='comments', verbose_name='所属用户')
    content = models.CharField(verbose_name='评论内容', max_length=500)
    packing = models.CharField(verbose_name='商品包装', max_length=3, default='0',
                               choices=(('1','1分'),('2','2分'),('3','3分'),('4','4分'),('5','5分'),))
    deliverySpeed = models.CharField(verbose_name='送货速度', max_length=3, default='0',
                               choices=(('1','1分'),('2','2分'),('3','3分'),('4','4分'),('5','5分'),))
    deliveryClerkServices = models.CharField(verbose_name='配送员服务态度', max_length=3, default='0',
                               choices=(('1','1分'),('2','2分'),('3','3分'),('4','4分'),('5','5分'),))
    SellerServices = models.CharField(verbose_name='卖家服务', max_length=3, default='0',
                               choices=(('1','1分'),('2','2分'),('3','3分'),('4','4分'),('5','5分'),))
    is_anonymous = models.BooleanField(verbose_name='是否匿名', default=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")



