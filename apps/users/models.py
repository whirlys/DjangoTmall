from django.db import models

from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name="昵称", null=True, blank=True)
    birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(("male","男"),("female","女")), null=True, blank=True,verbose_name="性别")
    address = models.CharField(max_length=100, default=u"", verbose_name="居住地址", null=True, blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号码")
    avatar = models.ImageField(upload_to="image/avatar/%Y/%m",default="image/avatar.jpg", max_length=100, verbose_name="头像")
    identityCardType = models.CharField(verbose_name="证件类型", max_length=20,
                                        choices=(("IDCard","身份证"), ("passport","护照")), null=True, blank=True)
    identityCardNo = models.CharField(verbose_name="证件号码", max_length=20, null=True, blank=True, default="")
    userPoint = models.IntegerField(verbose_name="用户积分",default=0)
    userLever = models.CharField(verbose_name="会员级别",max_length=20,
                                 choices=(("1","普通会员"),("2","青铜会员"),("3","白金会员"),("4","黄金会员"),("5","砖石会员")),default="1")
    is_saler = models.BooleanField(verbose_name='是否为卖家', default=False)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username