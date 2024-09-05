import get_pos
import detail
import classify
import cdir
import save_excel
import threading
from loguru import logger
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

def deleteSameNum(num):
    last = num[-1]
    for i in range(len(num)-2, -1, -1): #len(num)-2是倒数第二个数，第一个-1为了生成到0下标
        if last == num[i]:
            del num[i] #删除后位置i处的元素后，其后一个相同的元素又补到了i位置
        else:
            last = num[i]
    return num

class myThread (threading.Thread):
    def __init__(self,po):
        threading.Thread.__init__(self)
        # self.threadID = threadID
        self.po = po
        self.det = None
    def run(self):
        self.det = ayhet_det(self.po)
    def get_det(self):
        return self.det

def ayhet_det(po):
    logger.info(po+' capturing---')
    # time.sleep(0.8)
    nex = detail.out(po)
    return nex

def split_list(lst, n):
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]



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
    pos0 = get_pos.out('https://www.printemps.com/fr/fr/cowboy-homme')
    lss = [['货号','价格','大小','l3','剩余有货店量','名称',"MATERIAL","COLOR", "SIZE CHART TYPE",'DESCRIPTION','img url']]
    # for po in pos:
    #     print(po,'采集中---')
    #     lss = lss + detail.out(po)  
    #     pass
    results =[ ]
    tasks =[ ]
    # loop = asyncio.get_event_loop()
    poss = split_list(pos0,10)
    for pos in poss:
        for po in pos:
            task = myThread(po)
            task.start()
            tasks.append(task)
        for task in tasks:
            task.join()
            results.append(task.get_det())
    
    for i in results:
        if i == None:
            continue
        lss = lss + i
    lss=deleteSameNum(lss)
    lss = equal_list(lss)
    save_excel.out(path,lss)
    print(path,'已储存')

