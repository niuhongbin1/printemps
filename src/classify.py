import time
import requests
from lxml import etree




def get_html_404():
    curl = 'https://www.printemps.com/fr/fr/jupes-femme'
    hs = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    rep = requests.get(url=curl,timeout=5,headers=hs)
    text = rep.text
    # with open('./c.html',mode='r',encoding='utf-8') as t:
    #     text = t.read()
    p_html = etree.HTML(text)
    
    
    ds = n1(p_html)
    
    return ds

def n1(p):
    root = []
    j = 0
    lis = p.xpath('//nav[@class="menu"]/ul/li')[2:5]
    for i in lis:
        name = i.xpath('./a/span/text()')
        
        if len(name) != 0:
            ff = {
                'name':name[0].replace('\n','').replace(' ',''),
                'data-url':None,
                'sons':[]
            }
            
            ff['sons'] = n2(i)
            
            root.append(ff)
            
        else:
            continue
        pass

    return root

def jnn(n):
    """  排除不需要的类别

    Args:
        n (_type_): _description_

    Returns:
        _type_: _description_
    """
  
    if "Toutl'univer" in n:
        return True
    elif "Vior" in n:
        return True
    else:
        return False



def n2(li):
    """找出二级目录

    Args:
        li (_type_): _description_
    """
    n1s = []
    lis = li.xpath('./ul/div/section/div/li')[:-1]

    
    for i in lis:
        try :
            n = i.xpath('./a/span/text()')[0].replace('\n','').replace(' ','').replace('\t','')
            if jnn(n):
                continue
        except:
            print('二级分类出错')
        ff = {
                'name':n,
                'data-url':None,
                'sons':n3(i)
            }
        n1s.append(ff)
    return n1s

def n3(li):
    """ 三级目录
    """
    lis = li.xpath('./ul/li')[:-1]
    n1s = []
    for i in lis:
        name = i.xpath('./a/span/text()')
        try:
            name = name[0].replace('\n','').replace(' ','').replace('\t','')
            du = i.xpath('./a/@href')[0]
        except:
            print('三级分类名称出错')
            continue
        just = jnn(name)
        if just:
            continue
        ff = {
                'name':name,
                'data-url':du,
                'sons':None
            }
        n1s.append(ff)
    return n1s


def out():
    r = get_html_404()
    return r


if __name__ == '__main__':
    out()

