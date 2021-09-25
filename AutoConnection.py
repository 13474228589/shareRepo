# wifiConnection
import pywifi
from pywifi import const
import time
import os
import requests

def wifi_state():
    # 判断本机是否有无线网卡,以及连接状态. return: 已连接或存在无线网卡返回1,否则0.
    #创建一个元线对象
    wifi = pywifi.PyWiFi()
    #取当前机器,第一个元线网卡
    iface = wifi.interfaces()[0] #有可能有多个无线网卡,所以要指定
    #判断是否连接成功
    if iface.status() in [const.IFACE_CONNECTED,const.IFACE_INACTIVE]:
        return 1
    else:
        return 0
        
def wifi_disconnect():
    wifi = pywifi.PyWiFi()  # 创建一个无线对象
    ifaces = wifi.interfaces()[0]  # 取一个无限网卡
    #print(ifaces.name())  # 输出无线网卡名称
    ifaces.disconnect()  # 断开网卡连接

def wifi_connect(wifiName):
    wifi = pywifi.PyWiFi()  # 创建一个无线对象
    ifaces = wifi.interfaces()[0]  # 取一个无限网卡
    #print(ifaces.name())  # 输出无线网卡名称
    ifaces.disconnect()  # 断开网卡连接
    time.sleep(1)  # 缓冲1秒
    profile = pywifi.Profile()  # 配置文件
    profile.ssid = wifiName # wifi名称
    ifaces.remove_all_network_profiles()  # 删除其他配置文件
    tmp_profile = ifaces.add_network_profile(profile)  # 加载配置文件
    ifaces.connect(tmp_profile) # connect part

def web_registe(method=None):
    if method=='logout':
        url_out='http://10.10.43.3/drcom/logout?callback=dr1619595146094&_=1619595138696'
        r=requests.get(url_out)
    else:
        return_value=''
        url_out='http://10.10.43.3/drcom/logout?callback=dr1619595146094&_=1619595138696'
        url_in1='http://10.10.43.3/drcom/login?callback=dr1619594786524&DDDDD=账号&upass=密码&0MKKey=123456&R1=0&R3=0&R6=0&para=00&v6ip=&_=1619594782218'
        url_nameList=['myName']
        url_in=[url_in1]

        for i in range(len(url_nameList)):
            if not web_state():
                requests.get(url_out)
                requests.get(url_in[i])
                if i>=1:
                    print('URL('+url_nameList[i-1]+') is exceptional')
                    return_value+='URL('+url_nameList[i-1]+') is exceptional'+'\n'
            else:
                print('WEB ('+url_nameList[i]+') connection part is finished')
                return_value+='WEB ('+url_nameList[i]+') connection part is finished'+'\n'
                return return_value
        print('URL('+url_nameList[i]+') is exceptional')
        return_value+='URL('+url_nameList[i]+') is exceptional'+'\n'
        return return_value

def web_state():
    url_test='http://baidu.com'
    try:
        header_1 = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        r=requests.get(url_test,headers=header_1)
        if '登录路径' in r.text:
            return 0
        elif '百度一下，你就知道' in r.text:
            return 1
    except:
        return 0

def Auto_connect():
    returnValue=''
    if not web_state():
        for i in range(3): # connect the wifi for three times
            if not wifi_state():
                wifi_connect('web.wlan.bjtu')
                time.sleep(2)
                if wifi_state():
                    print('WIFI connection is finished')
                    returnValue+'\n'+'WIFI connection is finished'
                    break
            else:
                print('WIFI is connected.')
                returnValue+'\n'+'WIFI is connected.'
                break
            print('WIFI connection is unsuccessful')
            returnValue+='WIFI connection is unsuccessful'
        # school wifi login
        
        return returnValue+web_registe()
    return returnValue+'\n'+'WIFI is connected.'

try:
    f=open('F:/programFile/Wifi_Connectiong_Log.txt','a+')
    f.close()
except:
    os.makedirs('F:/programFile')
    f=open('F:/programFile/Wifi_Connectiong_Log.txt','w+')
    f.close()
    print('Created a new file.')

f=open('F:/programFile/Wifi_Connectiong_Log.txt','a+')
f.write(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())+'\n')
f.write(Auto_connect()+'\n'*2)
f.close()
