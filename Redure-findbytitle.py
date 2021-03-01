import os,sys
import xml.etree.ElementTree as ET
from urllib.request import *
def cls_prt(strs):
    sys.stdout.write(strs + ' '*10+'\r')
    sys.stdout.flush()
try:
    target=sys.argv[1]
    title=sys.argv[2]
except IndexError:
    print('用法:python Redure-findbytitle.py [已处理好的贴吧名] [标题部分或全部名称]')
    sys.exit()
target=sys.argv[1]
now=os.getcwd()+'/map/'+target+'/'
lsxt=os.listdir(now)
count=[]
i=0
for ffile in lsxt:
    try:
        i+=1
        cls_prt('[+] '+ffile+'<->'+str(i))
        tree = ET.parse(now+ffile)
        root = tree.getroot()
        if title in root[0][1].text:
            print(ffile+'            ')
    except:
        pass
print('[+]','完成。.')
