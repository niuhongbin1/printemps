from log import logger
import get_pos
import detail
import classify
import cdir
import save_excel
import json
import sys 
import clear_dir







  


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

def d_du(du):
    path = du[0] + '/'+du[0][7:].replace('/','_')+'_jds.xlsx'
    logger.info(du[0]+' part capturing')
    pos = get_pos.out(du[1])
    lss = [['货号','价格','大小','oa','pool','名称',"MATERIAL","COLOR", "SIZE CHART TYPE",'DESCRIPTION','img url','url','品牌']]
    for po in pos:
        logger.info(po['id']+' capturing---')
        nex = detail.out(po)  
        if nex == None:
            continue
        lss = lss + nex  
        pass
    lss=deleteSameNum(lss)
    if len(lss) == 1:
        return du
    lss = equal_list(lss)
    save_excel.out(path,lss)
    logger.info(path+' saved successfully')
    return None

def deal_err(ers):
    keep = True
    max_t = 5
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

def read_ca_hd():
    try:
        with open("cg_hd.txt", "r",encoding='utf-8') as f:
            return json.loads(f.read())
    except:
        return []
def read_all_ca():
    with open("cg_all.txt", "r",encoding='utf-8') as f:
        return json.loads(f.read())
     
def save_ca_hd(ca_hd):
    #  与 twopic  不同 此处是  打开追加    而 twopic 是  重写
    with open("cg_hd.txt", "w",encoding='utf-8') as f:
        f.write(json.dumps(ca_hd))

def main():
    all_dus = read_all_ca()
    cg_hd = read_ca_hd()
    for i in cg_hd:
        if i in all_dus:
            all_dus.remove(i)
    save_all_ca(all_dus)
    #  ca has done
    ca_hd = []
    ers = []  #  收集失败分类
    dus = all_dus
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
    logger.info('运行完成')
if __name__ == '__main__':
    main()
    exit()



