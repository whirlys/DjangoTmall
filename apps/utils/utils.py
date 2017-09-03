import time
import random


def order_code_format(user_id):
    """
    订单编号格式化：时间戳 + 用户id（9位） + 随机数4位
    """
    time_stamp = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    user_id = '%06d' % user_id

    rand = ''.join([str(random.randint(0,9)) for _ in range(4)])

    return 'OD' + str(time_stamp) + str(user_id) + str(rand)




def product_code_format(shop_id):
    """
    产品编号：时间戳 + shopId + 随机数4位
    """
    time_stamp = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    shop_id = '%06d' % shop_id

    rand = ''.join([str(random.randint(0,9)) for _ in range(4)])

    return 'P'  + str(time_stamp) + str(shop_id) + str(rand)

