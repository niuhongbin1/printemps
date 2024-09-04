
import time
import requests
from lxml import etree
import re
import json
import random
import fake_useragent
from loguru import logger

def requ_repeat(link,err_txt,par=None,hes = None):
    """ 用于多次重试

    Args:
        link (_type_): _description_
        err_txt (_type_): _description_

    Returns:
        _type_: _description_
    """
    keep = True
    maxtimes = 10
    count = 0
    while keep and count < maxtimes:
        try:
            if hes == None:
                
                hes = {
                    'Accept':'*/*',
                    'Accept-Encoding':'gzip, deflate, br',
                    'Connection':'keep-alive',
                    "Postman-Token":'2423'+str(int(random.random()*10000)),
                    'User-Agent':'PostmanRuntime/7.36.3'
                }
                pass
            response = requests.request("GET",link,timeout=10,params=par,headers=hes)
            if response.status_code == 200:
                keep = False
                return response
            else:
                count = count + 1
                logger.warning(err_txt+'  获取重试' + str(count))
                pass
        except Exception as e:
            count = count + 1
            logger.warning(err_txt+'  获取重试' + str(count) +'\n'+str(e))
        
    return False


def get_html(url):
    try:
        response = requ_repeat(link=url,err_txt='get_html')
        if response == False:
            return False
        # p_html =etree.HTML(response.text) 
        
        return response.text
    except Exception as e:
        logger.warning(url+'请求失败'+e)
        return False

    

  











def get_infoj(p):
    p  = etree.HTML(p)
    jtx = p.xpath('//script[@type="application/ld+json"]/text()')
    for j in jtx:
        if len(j) == 0:
            continue
        else:
            try:
                info_j = json.loads(j)
                if info_j['@type'] == 'Product':
                    return info_j
                else:
                    continue
            except:
                continue

def get_szs(url):
    """
    """
    sz ={
        'sn':'',
        'soa':'',
        'pr':'',
        'sku':'',   
    }
    ## https://www.printemps.com/ajax.php?pid=7472060&do=getLstRefDispo
    szs_ph = requ_repeat(link='https://www.printemps.com/ajax.php?pid='+url.split('-')[-1]+'&do=getLstRefDispo',err_txt='get_szs')
    if szs_ph == False:
        return [sz]
    else:
        szs = []
        szsdbs = szs_ph.json().keys()
        for szsb in szsdbs:
            szn = szs_ph.json()[szsb]['label']
            
            szoa = szs_ph.json()[szsb]['stock']['total_stock']
            if szoa == 0:
                szoa = '0'
            else:
                szoa = '1'
            pr =szs_ph.json()[szsb]['pxAff']
            sku = szs_ph.json()[szsb]['refId']
            sz = {
                'sn':szn,
                'soa':szoa,
                'pr':pr,
                'sku':sku,
            }
            szs.append(sz)
    return szs

def get_mat(p):
    p  = etree.HTML(p)
    info_0 = p.xpath('//div[@class="accordion-body"]')
    try:
        for infoi in info_0:
            info_ts = infoi.xpath('.//text()')
            for nn in info_ts:
                if 'Composition : ' in nn:
                    info = infoi
                    break   
        mats0 = info.xpath('.//text()')
        mats = []
        for nns in mats0:
            if len(nns.replace('\n','').replace(' ','').replace('\t','')) > 1:
                mats.append(nns)
        for nn in mats:
            if 'Composition' in nn:
                matn = mats.index(nn)
                break
        mat = mats[matn+1].replace('\n','').replace(' ','').replace('\t','')
        
        return mat
    except:
        logger.warning("mat error")
        return None
    


def get_id(p):
    t = p
    id = re.findall('Référence(.*?\\|)',t,re.DOTALL)
    if len(id) == 0:
        return None
    else:
        return id[0].replace(' ','').replace('\n','').replace('\t','').replace(':','').replace(' ','').replace('|','').replace('</span>','')
    
def deal(p,url):
    
    info_j = get_infoj(p)
    
    if info_j == False or info_j == None:
        return [[url,'','err','err','err']]
    name = info_j["name"]
    desp = info_j['description']

    # pr = info_j['offers']['price'] 
    mat = get_mat(p)
    try:
        col = info_j['name'].split('|')[-1]
    except:
        col = None
    imgs = ''
    imglen = 0
    for i in info_j['image']:
        imglen = imglen + 1
        imgs = imgs + i + ','
        if imglen >= 3:
            break
    id = get_id(p)
    szs = get_szs(url)
    # 汇总为二维列表
    des = []
    for sz in szs:
        # [['货号','价格','大小','l3','折前价格','名称',"MATERIAL","COLOR", "SIZE CHART TYPE",'DESCRIPTION','img url']]
        des.append([id,sz["pr"],sz['sn'],sz['soa'],sz['sku'],name,mat,col,None,desp,imgs,url])
    return des



def main(pdd):
    url = pdd
    p = get_html(url)
    if p == False:
        return [[url,'','OS','','','','']]
    else:
        dts = deal(p,url)
    return dts
    
def out(pdd):
    return main(pdd)

if __name__ == '__main__':
    pdd = 'https://www.printemps.com/fr/fr/naked-wolfe-sandales-a-talon-en-cuir-blanc-femme-6294649'
    out(pdd) 