import os 
import time 
import classify
def mdrs(ls,panow0,dus):
    for i in ls:
        panow = panow0 +'/'+ i['name'].replace(' ','_').replace('\n','').replace('/','_').replace('...','')
        if os.path.exists(panow):
            pass
        else:
            os.mkdir(panow)
        cd = i['data-url']
        du = [panow,cd]
        dus.append(du)
        if i['sons'] == None:
            continue
        else:
            mdrs(i['sons'],panow,dus)
            pass
        panow = panow0
    




def main(claes):

    dus = []
    mdrs(claes,'../res',dus)

    
    return dus

def out(claes):
    return main(claes)





if __name__ == '__main__':
    cls = classify.out()
    out(cls)
