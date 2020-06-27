from urllib.request import *
from urllib.parse import urlencode
import re,sys,os,datetime

#
# >-download tieba context-<
#      deepcloud[swwm] 2020
# usage:
#  python3 tb.py tiebaname (can input chinese) [minpage-maxpage] [configfile] [-os] [-od]
#   -os    ->Only Scan pages url
#   -od    ->Only Download url
# egg:
#  python3 tb.py 文坑
#
#
def cls_prt(strs):
    sys.stdout.write(strs + ' '*5+'\r')
    sys.stdout.flush()
def openp(it,pn=1):
    req = Request('https://tieba.baidu.com/p/'+it+'?pn='+str(pn)+'&ie=utf-8')
    html = urlopen(req)
    # Encode mode->Random????
    try:
        htm=html.read().decode('utf-8',errors='ignore')
    except:
        htm=html.read().decode('GBK')
    html.close()
    return htm
target=sys.argv[1]
pn=0
now=os.getcwd()+'/download/'+target
if not os.path.exists(now):os.mkdir(now)

d=datetime.datetime.now()
print('[+] Running at %s-%s-%s %s:%s:%s' %(d.year,d.month,d.day,d.hour,d.minute,d.second))


cont=re.compile(r'(?<=<a rel="noreferrer" href="/p/)[0-9]+')
pnre=re.compile(r'(?<=共有主题数<span class="red_text">)[0-9]+')
page=re.compile(r'(?<=回复贴，共<span class="red">)[0-9]+')

#headers={"User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"}
req=Request('https://tieba.baidu.com/f?'+urlencode({'kw':target})+'&ie=utf-8')
htm=urlopen(req)
html=htm.read().decode('utf-8')
htm.close()
found=pnre.findall(html)
if not found:
    print('[-]','Could not Found',target+'!')
    sys.exit(1)
pn=int(found[0])//50+1
item=[]
if len(sys.argv)>=2:
    start,end=0,pn
else:
    start,end=sys.argv[2].split('-')
print('[+] Scan page:',pn)
if '-od' not in sys.argv:
    for i in range(start,end):
        url='https://tieba.baidu.com/f?'+urlencode({'kw':target})+'&pn='+str((int(i)*50+50))+'&ie=utf-8'
        rq = Request(url)
        htm = urlopen(rq)
        item.extend(cont.findall(htm.read().decode('utf-8')))
        cls_prt('[+] page:'+str(i)+'|'+str(round(i/pn,4)*100)+'%')
        htm.close()
    if '-os' in sys.argv:
        f=open(sys.argv[3],'a')
        f.writelines(item)
        f.close()
        print('[+]','Scan page done.')
if '-od' in sys.argv:
    f=open(sys.argv[3])
    item=f.readlines()
    f.close()
if '-os' not in sys.argv:
    print('\n[+]','Ok,it\'s time to download')
    for it in item:
        try:
            file=now+'/'+it
            html=openp(it)
            rt=page.findall(html)
            if not rt:continue
            pages=int(rt[0])
            for n in range(pages):
                html=openp(it,int(n)+1)
                try:
                    f=open(file+'_'+str(n)+'.html',mode='w')
                except:
                    f=open(file+'_'+str(n)+'.html',mode='a')
                f.write(html)
                f.close()
            cls_prt('[+] NowDownload:'+it+'-'+str(n))
        except KeyboardInterrupt:
            print('[-]','Stop             ')
            sys.exit(0)
print('[+]','Complete.                ')
    