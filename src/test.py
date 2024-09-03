import get_pos
import detail
import classify
import cdir
import save_excel
'''
ERROR
/short-jacket-in-wool-and-cashmere/S359Y02X40-8100.html?cgid=women&p=228
'''

def deleteSameNum(num):
    last = num[-1]
    for i in range(len(num)-2, -1, -1): #len(num)-2是倒数第二个数，第一个-1为了生成到0下标
        if last == num[i]:
            del num[i] #删除后位置i处的元素后，其后一个相同的元素又补到了i位置
        else:
            last = num[i]
    return num




def equal_list(l2s):
    #  补齐列表
    longth = len(l2s[0])
    for i in l2s:
        if len(i) >= longth:
            longth = len(i)
    for i in l2s:
        if len(i) < longth:
            i += ['']*(longth-len(i))
    return l2s

if __name__ == '__main__':
    path = './test.xlsx'
    # pos = get_pos.out('footwear-men:arc')
    pos = [{
        'url':'https://www.jdsports.fr/product/noir-under-armour-sac-de-sport-undeniable/16472998_jdsportsfr/',
        'id':'test'
    }]
    lss = [['货号','价格','大小','l3','剩余有货店量','名称',"MATERIAL","COLOR", "SIZE CHART TYPE",'DESCRIPTION','img url']]
    for po in pos:
        print(po,'采集中---')
        lss = lss + detail.out(po)  
        pass
    lss=deleteSameNum(lss)
    lss = equal_list(lss)
    save_excel.out(path,lss)
    print(path,'已储存')

