#本文from：https://blog.csdn.net/weixin_40372371/article/details/80154707

# IP地址取自国内髙匿代理IP网站：http://www.xicidaili.com/nn/
# 仅仅爬取首页IP地址就足够一般使用

from bs4 import BeautifulSoup
import requests
import random
import urllib

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
}

def getHTMLText(url,proxies):
    try:
        r = requests.get(url,proxies=proxies)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except:
        return 0
    else:
        return r.text

def get_ip_list(url):
    web_data = requests.get(url,headers=headers)
    soup = BeautifulSoup(web_data.text, 'html.parser')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
#检测ip可用性，移除不可用ip：（这里其实总会出问题，你移除的ip可能只是暂时不能用，剩下的ip使用一次后可能之后也未必能用）
    for ip in ip_list:
        try:
          proxy_host = "https://" + ip
          proxy_temp = {"https": proxy_host}
          res = urllib.urlopen(url, proxies=proxy_temp).read()
        except Exception as e:
          ip_list.remove(ip)
          continue
    return ip_list

def get_random_ip(ip_list):#随机拿出一个IP去爬别人的网站
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies

if __name__ == '__main__':
    url = 'http://www.xicidaili.com/nn/'
    ip_list = get_ip_list(url)
    proxies = get_random_ip(ip_list)
    print(proxies)
