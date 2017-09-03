from xadmin.plugins.actions import BaseActionView
from django.http import HttpResponse

class OffTheShelfAction(BaseActionView):
    """
    将商品批量下架
    """
    # 这里需要填写三个属性
    action_name = "offTheShelfAction"  #: 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    #: 描述, 出现在 Action 菜单中, 可以使用 ``%(verbose_name_plural)s`` 代替 Model 的名字.
    description = ('将 %(verbose_name_plural)s 批量下架')
    model_perm = 'change'  #: 该 Action 所需权限

    # 而后实现 do_action 方法
    def do_action(self, queryset):
        # queryset 是包含了已经选择的数据的 queryset
        for obj in queryset:
            obj.publish_status = 'down'
            obj.save()
        # 返回 HttpResponse
        return HttpResponse("已将所选产品下架！")