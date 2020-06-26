import os,sys,re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as BS

#
# map.py -->deepcloud[swwm] coding.
# usage:
#  python3 map.py [tiebaname]

def cls_prt(strs):
    sys.stdout.write(strs + ' '*10+'\r')
    sys.stdout.flush()

target=sys.argv[1]
now=os.getcwd()+'/map/'+target
if not os.path.exists(now):os.mkdir(now)
nowd=os.getcwd()+'/download/'+target+'/'
now+='/'
#title=re.compile(r'(?=<h3 class="core_title_txt pull-left text-overflow  " title=").*(?=")')
imgsrc=re.compile(r'(?=<img class="BDE_Image" src=").*jpg')
detag=re.compile(r'<.*>')
def build_xml(file,dit):
    temp='''
    <data><head><p></p><title></title><date></date></head><body></body></data>
    '''
    xl=ET.XML(temp)
    xl[0][0].text=dit['head'].get('p','')
    xl[0][1].text=dit['head'].get('title','')
    xl[0][2].text=dit['head'].get('date','')
    for k,v in dit['body'].items():
        # k-> floor No. v-> floor info and text (dict)
        anp=ET.XML('''
<floor num="0">
<floorinfo>
<name></name>
<level></level>
<date></date>
</floorinfo>
<text>
</text>
</floor>
        ''')
        anp.set('num',str(k))
        anp[0][0].text=v['floorinfo'].get('name','')
        anp[0][1].text=v['floorinfo'].get('level','')
        anp[0][2].text=v['floorinfo'].get('date','')
        for key,value in v['text'].items():
            value=value.replace('，',',').replace('&','&amp;').replace("'",'&apos;').replace('"','&quot;').replace('<','&lt;').replace('>','&gt;')
            rep='<%s>%s</%s>' %(key,value,key)
            try:
                anp[1].append(ET.XML(rep))
            except:
                pass
        xl[1].append(anp)
        #print(ET.tostring(xl),encoding='unicode')
    mt=ET.tostring(xl)
    if os.path.exists(now+file):
        f=open(now+file,'w')
    else:
        f=open(now+file,'a')
    f.write(mt.decode('utf-8'))
    f.close()
def parsefile(p,pn=1):
    dct={'head':{'p':p,'title':'','date':''},'body':{}}
    i=1
    for i in range(pn):
        f=open(nowd+p+'_'+str(i)+'.html')
        ret=f.read()
        f.close()
        soup=BS(ret,'lxml')
        mtch=soup.find('h3',class_='core_title_txt pull-left text-overflow')
        if mtch:dct['head']['title']=str(mtch.string)
        # find all tiezi <div>
        tiezi=soup.find_all('div',class_='l_post l_post_bright j_l_post clearfix')
        for tz in tiezi:
            # floorinfo
            nowstare=tz.find_all('span',class_='tail-info')
            for yu in nowstare:
                if str(yu.string)[-1]=='楼':
                    floornum=str(yu.string[:-1])
                elif yu.string is None:
                    continue
                date=str(yu.string)
            tempt={floornum:{'floorinfo':{'name':'','level':'','date':''},'text':{}}}
            tempt[floornum]['floorinfo']['date']=date
            nzp=tz.find('a',class_='p_author_name j_user_card')
            if nzp:
                tempt[floornum]['floorinfo']['name']=str(nzp.string)
            QAQ=tz.find('div',class_='d_post_content j_d_post_content')
            for ko in QAQ.contents:
                nastr=str(ko)
                nastr=nastr.replace('<br />','\n').replace('<br>','\n')
                # find img
                rty=imgsrc.findall(nastr)
                if rty:
                    for src in rty:
                        tempt[floornum]['text'].update({'img':scr})
                # empty tag
                nastr=detag.sub('',nastr)
            tempt[floornum]['text'].update({'p':nastr})
            dct['body'].update(tempt)
    build_xml(p+'.xml',dct)
print('[+] map.py Running.Press Ctrl+C to quit.')
p_any=[]
lsxt=os.listdir(nowd)
for ffile in lsxt:
    if os.path.isfile(nowd+ffile):
        nzz=ffile.split('.')[0]
        nzz=nzz.split('_')
        if nzz[0] not in p_any:
            p_any.append(nzz[0])
            nzz[1]=int(nzz[1])
            while (nzz[0]+'_'+str(nzz[1])+'.html') in lsxt:
                nzz[1]+=1
            cls_prt('[+] handle p:'+nzz[0])
            parsefile(nzz[0],nzz[1])
print('[+]','All file parse done.')        
        
    