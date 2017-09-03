from .views import ITaobaoView,AccountSettingsView, PersonalData,user_avatar_upload
from .views import LogisticsView,NotificationsView
from django.conf.urls import url,include



urlpatterns = [
    url(r'^itaobao/$', PersonalData.as_view(), name='itaobao'),
    url(r'^accountSettings/$',AccountSettingsView.as_view(), name='accountSettings'),
    url(r'^personalData/$', PersonalData.as_view(), name='personalData'),
    url(r'^avatar/$',user_avatar_upload,name='avatar'),
    url(r'^logistics', LogisticsView.as_view(), name="logistics"),
    url(r'^notifications$',NotificationsView.as_view(), name='notifications'),
]
