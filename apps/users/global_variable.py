# 全部变量

from products.models import Cart

def global_variable(request):
    if request.user.is_authenticated():
        cart_num = Cart.objects.filter(user=request.user).count()
    else:
        cart_num=0
    content = {'cart_num':cart_num}
    return content
