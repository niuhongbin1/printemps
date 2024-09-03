from log import logger
import get_pos
import detail
import classify
import cdir
import save_excel
import json
import sys 
import clear_dir
import threading
import time






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


def d_du(du):
    time.sleep(3)
    path = du[0] + '/'+du[0][7:].replace('/','_')+'_print.xlsx'
    logger.info(du[0]+' part capturing')
    pos0 = get_pos.out(du[1])
    lss = [['货号','价格','大小','oa','sku','名称',"MATERIAL","COLOR", "SIZE CHART TYPE",'DESCRIPTION','img url','url']]
    # for po in pos:
    #     logger.info(po['id']+' capturing---')
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
    if len(lss) == 1:
        return du
    try:
        save_excel.out(path,lss)
    except:
        logger.info('保存失败')
        return du
    logger.info(path+' saved successfully')
    return None

def deal_err(ers):
    keep = True
    max_t = 3
    cu = 1 
    fin_ers = []
    while cu < max_t and keep:
        ers_in = []
        logger.info('错误尝试 >>>' + str(cu))
        for i in ers:
            er = d_du(i)
            # er = i
            if er != None:
                ers_in.append(er)
            pass
        
        if ers_in == []:
            keep = False
        else:
            ers = ers_in
            cu = cu+1
        
        fin_ers = ers_in   
    logger.info('错误重试结束')
    logger.info(fin_ers)


def save_all_ca(dus):
    with open("cg_all.txt", "w",encoding='utf-8') as f:
        f.write(json.dumps(dus))
        
def save_ca_hd(ca_hd):
    with open("cg_hd.txt", "w",encoding='utf-8') as f:
        f.write(json.dumps(ca_hd))


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


def main():
    
    # pi()
    logger.info(' 自动清空  res   文件夹 \n勿关闭窗口  输出信息已转入  data.txt\n运行完毕会自动关闭')
    clear_dir.clean_folder('../res')
    clss = classify.out()
    dus = cdir.out(clss)
    # 保存所有分类
    save_all_ca(dus)
    #  ca has done
    ca_hd = []

    ers = []  #  收集失败分类
    for i in dus:
        # i = dus[15]
        if i[1] != None:
            er = d_du(i)
            # er = i
            if er != None:
                ers.append(er)
            else:
                ca_hd.append(i)
                #  保存已经采集的分类
                save_ca_hd(ca_hd)
        pass
    pass

    # 失败分类重新请求
    if len(ers) != 0:
        deal_err(ers)
    print('运行完成')
if __name__ == '__main__':
    main()
    exit()



