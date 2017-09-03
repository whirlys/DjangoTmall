from django.db import models
from users.models import UserProfile
# from products.models import Product
import time
import random

#
# 天猫店铺分为旗舰店、专卖店和专营店三类。入驻条件分别为：
# 1. 旗舰店: 商家以自有品牌（商标为R或TM状态）入驻天猫开设的店铺
# 2. 专卖店: 商家持品牌授权文件在天猫开设的店铺。
# 3. 专营店: 经营天猫同一招商大类下两个及以上品牌商品的店铺。



class TmallShop(models.Model):
    """
    天猫商铺
    """
    owner = models.OneToOneField(UserProfile, related_name='shop',verbose_name='所属用户')
    type = models.CharField(verbose_name='商铺类型', choices=(('flagshipShop','旗舰店'), ('ExclusiveShop','专卖店'),('FranchisedStore','专营店')), max_length=30)
    shopName = models.CharField(verbose_name='店铺名称', max_length=50)
    companyInfo = models.TextField(verbose_name='公司信息')
    scope = models.TextField(verbose_name='经营范围')
    location = models.CharField(verbose_name='所在地', max_length=200)
    businessLicense = models.ImageField(verbose_name='工商执照', upload_to='image/BusinessLicense/%Y/%m')
    is_active = models.BooleanField(verbose_name='是否有效', default=False)
    # logisticsCompany = models.ForeignKey(LogisticsCompany, related_name='tmallShops', verbose_name='合作的物流公司')
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.shopName

    class Meta():
        ordering = ('-created',)
        verbose_name = '天猫商铺'
        verbose_name_plural = '天猫商铺'

#
# class PurchaseOrder(models.Model):
#     """
#     采购单
#     """
#     shop = models.ForeignKey(TmallShop, related_name='purchaseOrder',verbose_name='所属商铺')
#     # product = models.ForeignKey(Product, related_name="purchaseOrder", verbose_name="采购产品")
#     product_code = models.CharField(verbose_name='产品编码', max_length=30)
#     cost = models.DecimalField(verbose_name="进货价格", max_digits=6, decimal_places=2)
#     amount = models.IntegerField(verbose_name='进货数量')
#     purchaser = models.CharField(verbose_name='采购员', max_length=20)
#     factory = models.CharField(verbose_name='采购工厂', max_length=30)
#     telphone = models.CharField(verbose_name='联系电话', max_length=100)
#     created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
#     updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
#
#     def __str__(self):
#         return self.user.companyName
#
#     class Meta():
#         ordering = ('-created',)
#         verbose_name = '采购单'
#         verbose_name_plural = '采购单'


class LogisticsCompany(models.Model):
    """
    物流公司
    """
    companyCode = models.CharField(verbose_name='公司编码',max_length=10)
    companyName = models.CharField(verbose_name='公司名称', max_length=50)
    contact = models.CharField(verbose_name='公司联系人', max_length=50)
    telphone = models.CharField(verbose_name='联系电话', max_length=100)
    price = models.DecimalField(verbose_name='配送单价', max_digits=6, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.companyName

    class Meta():
        ordering = ('-created',)
        verbose_name = '物流公司'
        verbose_name_plural = '物流公司'

    def getCourierNumber(self):
        """
        生成订单号：时间戳  + 4个随机字符
        :return:
        """
        time_stamp = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        rand = ''.join([str(random.randint(0, 9)) for _ in range(4)])

        return self.companyCode + str(time_stamp) +  str(rand)
