"""
Author: Meng
Date: 2018/10/2
"""
import sys
from mi_lib.shop_list import get_shop_list
import time
from mi_lib.login_mi import login_get_cookie
from mi_lib.shan_req import shangou_request, shangou_request_one



def main():
    shop_list = get_shop_list()
    shop = input_goods_id(shop_list)
    # print(shop)
    task_executor(shop)


def task_executor(shop):
    while True:
        s_time = shop.get('start_time')
        l_time = time.time()
        if s_time > l_time + 30:
            csx = s_time - l_time
            m = int(csx / 60) % 60
            h = int(csx / (60 * 60))
            s = int(csx % 60)
            stf_ti = '{:02}:{:02}:{:02}'.format(h, m, s)
            sys.stdout.write('\r距秒杀《{}》开始还有 {}'.format(shop.get('name'), stf_ti))
            sys.stdout.flush()
            time.sleep(1)
        else:
            print('还有半分钟就开始秒杀-{},进行秒杀前准备工作'.format(shop.get('name')))
            # 调用selenium登录小米获取cookie
            cookie = login_get_cookie()
            while True:
                l_ti = time.time()
                # 距离开始抢购0.8秒时进入抢购环节
                if s_time > l_ti + 0.8:
                    sys.stdout.write('\r距秒杀《{}》开始还有 {}'.format(shop.get('name'), s_time - l_ti))
                    sys.stdout.flush()
                    time.sleep(0.1)
                else:
                    shangou_request_one(shop, cookie)
                    break
            break


def input_goods_id(shop_list):
    while True:
        shop_id = input('请输入商品ID：')
        if shop_id:
            shop = None
            for item in shop_list:
                if item.get('goods_id') == shop_id:
                    shop = item
                    break
            if shop:
                print('已选择=> 名称：{}， 秒杀时间:{}， ID：{}'.format(shop.get('name'), shop.get('st_time'), shop_id))
                sh = shop
                break
            else:
                print('未找到该商品，请检查商品ID')
        else:
            print('输入内容异常请重新输入')
    return sh


if __name__ == '__main__':
    main()
