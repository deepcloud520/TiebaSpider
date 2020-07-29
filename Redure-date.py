import os,sys,re
import xml.etree.ElementTree as ET

target=sys.argv[1]
now=os.getcwd()+'/map/'+target+'/'
lsxt=os.listdir(now)
count={'year':{}}
for ffile in lsxt:
    try:
        tree = ET.parse(now+ffile)
        root = tree.getroot()
        year=root[0][2].text[:4]
        if year not in count['year']:
            count['year'].update({year:1})
        else:
            count['year'][year]+=1
    except:
        pass
fl=[]
for t in count['year'].keys():
    fl.append(int(t))
fl.sort()
print('----'+target+'----')
jl=0
for p in fl:
    jl+=count['year'][str(p)]
for m in fl:
    noey=count['year'][str(m)]
    lg=round(noey/jl,2)
    print(m,':','*'*int((lg*100)),'<'+str(noey)+'>')
    