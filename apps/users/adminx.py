import xadmin
from xadmin import views
from .models import UserProfile
from products.models import Product
# from xadmin.plugins.auth import UserAdmin
# from xadmin.layout import Fieldset, Main, Side, Row
# from django.utils.translation import ugettext as _

# 基本的修改
class BaseSetting(object):
    enable_themes = True   # 打开主题功能
    use_bootswatch = True  #

# 针对全局的
class GlobalSettings(object):
    site_title = "Django仿天猫后台"  # 系统名称
    site_footer = "Django仿天猫"      # 底部版权栏
    menu_style = "accordion"     # 将菜单栏收起来
    # global_search_models = [UserProfile, Product]


# @xadmin.sites.register(views.website.IndexView)
# class MainDashBoard(object):
#     widgets = [
#         [
#             {"type": "html", "title": "Test Widget",
#              "content": "<h3> 欢迎来到Django仿天猫后台！ </h3><p>Join Online Group: <br/>QQ Qun : 282936295</p>"},
#             {"type": "chart", "model": "app.accessrecord", "chart": "user_count",
#              "params": {"_p_date__gte": "2013-01-08", "p": 1, "_p_date__lt": "2013-01-29"}},
#             # {"type": "list", "model": "app.host", "params": {"o": "-guarantee_date"}},
#         ],
#     ]


# 注册，注意一个是BaseAdminView，一个是CommAdminView
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)