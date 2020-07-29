import os,sys
import xml.etree.ElementTree as ET
from urllib.request import *
def cls_prt(strs):
    sys.stdout.write(strs + ' '*5+'\r')
    sys.stdout.flush()
target=sys.argv[1]
now=os.getcwd()+'/map/'+target+'/'
now2=os.getcwd()+'/img/'+target+'/'
if not os.path.exists(now2):os.mkdir(now2)
lsxt=os.listdir(now)
count=[]
for ffile in lsxt:
    try:
        tree = ET.parse(now+ffile)
        root = tree.getroot()
        floor=root[1][0][1]
        for c in floor:
            if c.tag=='img' and 'https://gsp0.baidu.com' not in c.text:
                count.append(c.text)
    except:
        pass
i=0
for url in count:
    try:
        r = Request(url)
        htm=urlopen(r)
        html=htm.read()
        htm.close()
    except:
        continue
    with open(now2+str(i)+'.png', "wb") as code:
        code.write(html)
    i+=1
    cls_prt('[+] Download:'+str(i))