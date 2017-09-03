
from django.conf.urls import url, include

# from django.contrib import admin
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings
from django.contrib.staticfiles import views as static_views
import notifications.urls
import xadmin
xadmin.autodiscover()

# version模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.register_models()

from users.views import IndexView,LoginView,RegistView,LogoutView



urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    #url(r'xadmin/', include(xadmin.site.urls)),
    url(r'xadmin/', include(xadmin.site.urls)),
    url(r'^captcha/', include('captcha.urls')),
    url('^notifications/', include(notifications.urls, namespace='notifications')),

    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^products/',include('products.urls',namespace='products')),
    url(r'^orders/', include('orders.urls',namespace='orders')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^saler/', include('salers.urls',namespace='salers')),

    url(r'^login/$',LoginView.as_view(),name="login"),
    url(r'^regist/$',RegistView.as_view(),name="regist"),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),



    # 以下在debug=False必须去掉，由nginx等来处理
    # url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    # url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
]

#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', static_views.serve),
    ]