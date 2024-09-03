'''
传入种类 url 获得产品详情页  url 
'''


# import requests
from lxml import etree
import time 
import re
import json
import logging
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


def requ_repeat(link,err_txt,par=None,mod='get',data=None,headers=None):
    """ 用于多次重试

    Args:
        link (_type_): _description_
        err_txt (_type_): _description_

    Returns:
        _type_: _description_
    """
    keep = True
    maxtimes = 5
    count = 0
    por ={
        
    }
    while keep and count < maxtimes:
        try:
            
            if mod == 'get':
                response = requests.get(link,timeout=5,params=par)
            elif mod == 'post':
                response = requests.post(link,timeout=5,params=par,data=data,headers=headers)
            if response.status_code == 200:
                keep = False
                return response
            else:
                count = count + 1
                print(link+err_txt+'  获取重试' + str(count))
                pass
        except Exception as e:
            print(e,link)
            count = count + 1
            print(err_txt+'  获取重试' + str(count))
        
    return False



def data(a,pid,purl):
    url = 'https://www.printemps.com/ajax.php'
    try:
        data_0 = {
            "do": "search",
            "action": "search",
            "requests[0][indexName]": pid,
            "requests[0][params][hitsPerPage]": "60",
            "requests[0][params][clickAnalytics]": "true",
            "requests[0][params][query]": "",
            "requests[0][params][highlightPreTag]": "__ais-highlight__",
            "requests[0][params][highlightPostTag]": "__/ais-highlight__",
            "requests[0][params][page]": str(a),
            "requests[0][params][maxValuesPerFacet]": "400",
            "requests[0][params][facets][0]": "mark",
            "requests[0][params][facets][1]": "categoryMenus",
            "requests[0][params][facets][2]": "categoryDetails",
            "requests[0][params][facets][3]": "color",
            "requests[0][params][facets][4]": "soldes",
            "requests[0][params][facets][5]": "attributes.Aspect",
            "requests[0][params][facets][6]": "attributes.Coupe",
            "requests[0][params][facets][7]": "attributes.Détails",
            "requests[0][params][facets][8]": "attributes.Longueur",
            "requests[0][params][facets][9]": "attributes.Notes olfactives",
            "requests[0][params][facets][10]": "merchants",
            "requests[0][params][facets][11]": "prices",
            'requests[0][params][tagFilters]':'',
        }
        data = MultipartEncoder(data_0)
        headers = {
            "Content-Type": data.content_type,
            'Accept-Encoding':'gzip,deflate,br',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'content-length':'2929',
            "Referer": purl,
            "X-Requested-With": "XMLHttpRequest",
            }
        response = requ_repeat(url,'获取产品列表',mod='post',data=data,headers=headers)
        if response == False:
            return [False,False]
        else:
            pj = response.json()
            return [pj,True]
    except:
        print('获取产品列表失败')
        return [False,False]



def pos(p_htmls):

    pdds = []     
    pxs = p_htmls["results"][0]["hits"]
    
    for px in pxs:
        pd = px['ficheProduitUrl']
        pdds.append(pd)
    return pdds

            


def main(url):
    # cgid = get_cgid(url)
    a = 0
    pid = url.split('/')[-1]
    pdds = []
    while True:
        jus = data(a,pid,url)
        if jus[0] == False:
            break
        else:
            pdds_sum = pos(jus[0])
            if len(pdds_sum)< 60:
                jus[1] = False
                pass
            pdds = pdds + pdds_sum

            if jus[1] == False:
                break
            else: 
                a = a+1
                pass
            pass
        pass
    return pdds
        
        
        
def out(cgid):
    # print('-----------  print  ----------')
    return main(cgid)

if __name__ == '__main__':
    # 该  cgid  为类别链接最后  cgid 
     out('https://www.printemps.com/fr/fr/bottes-femme')