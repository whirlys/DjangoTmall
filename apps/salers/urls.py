from django.conf.urls import url
from .views import SalerSettledView,ManageView,MainView,ProductListView,CategoryListView
from .views import ProductCreateView,GetCategoryJson,PropertysView,OrdersView,DeliverGoodsView
from .views import SalerSupportView



urlpatterns = [
    url(r'salerCenter$',SalerSupportView.as_view(), name='salerCenter'),
    url(r'^joinDjangoTmall$',SalerSettledView.as_view(), name='salerSettled'),
    url(r'^manage$', ManageView.as_view(), name='manage'),
    url(r'^main$', MainView.as_view(), name='main'),
    url(r'^productList$', ProductListView.as_view(), name='productlist'),
    url(r'^category$', CategoryListView.as_view(), name='category'),
    url(r'^createProduct$', ProductCreateView.as_view(), name='productCreate'),
    url(r'^getCategoryJson$', GetCategoryJson.as_view(), name='getCategoryJson'),
    url(r'^propertys$' , PropertysView.as_view(), name='propertys'),
    url(r'^orders$', OrdersView.as_view(), name='orders'),
    url(r'^deliverGoods$', DeliverGoodsView.as_view(), name='deliverGoods'),
]
