from urllib.request import *
from urllib.parse import urlencode
import re,sys,os,datetime,socket
#
# >-download tieba context-<
#      deepcloud[swwm] 2020
# usage:
#  python3 tb.py tiebaname (can input chinese) [minpage-maxpage] [configfile] [-os] [-od] [-nrw]
#   -os    ->Only Scan pages url
#   -od    ->Only Download url
#   -nrw   ->Not ReWrite
# egg:
#  python3 tb.py 文坑
#
#
MAXPN=150

def cls_prt(strs):
    sys.stdout.write(strs + ' '*5+'\r')
    sys.stdout.flush()
def openp(it,pn=1):
    req = Request('https://tieba.baidu.com/p/'+it+'?pn='+str(pn)+'&ie=utf-8')
    html = urlopen(req)
    # Encode mode->Random????
    try:
        t=html.read()
    except:
        html.close()
        return ''
    try:
        htm=t.decode('utf-8',errors='ignore')
    except:
        htm=t.decode('GBK')
    html.close()
    return htm
try:
    target=sys.argv[1]
except:
    print('用法：python tb.py [贴吧名] (此以后非必要选项，可不填)[起始页-终止页] [配置文件] [-os] [-od] [-nrw]\n\t-os:只扫描(写入配置文件中)\n\t-od:只下载(写入配置文件中)\n\t-nrw:不重复下载')
    sys.exit()
pn=0
now=os.getcwd()+'/download/'+target
if not os.path.exists(now):os.mkdir(now)

NRW=False
if '-nrw' in sys.argv:NRW=True

d=datetime.datetime.now()
print('[+] 正在运行 于 %s-%s-%s %s:%s:%s' %(d.year,d.month,d.day,d.hour,d.minute,d.second))

# set public timeout
socket.setdefaulttimeout(20)

cont=re.compile(r'(?<=<a rel="noreferrer" href="/p/)[0-9]+')
pnre=re.compile(r'(?<=共有主题数<span class="red_text">)[0-9]+')
page=re.compile(r'(?<=回复贴，共<span class="red">)[0-9]+')
headers={"User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"}
req=Request('https://tieba.baidu.com/f?'+urlencode({'kw':target})+'&ie=utf-8')
htm=urlopen(req)
html=htm.read().decode('utf-8')
htm.close()
found=pnre.findall(html)
if not found:
    print('[-]','无法找到',target,'或者可能反爬虫措施已启动'+'!')
    sys.exit(1)
pn=int(found[0])//50+1
item=[]
start,end=0,pn
if len(sys.argv)>2:
    hjk=sys.argv[2].split('-')
    if len(hjk)>1 and hjk[0]:
        start=int(hjk[0])
        end=int(hjk[1])

print('[+] 已获取:',pn)
if '-od' not in sys.argv:
    for i in range(start,end):
        url='https://tieba.baidu.com/f?'+urlencode({'kw':target})+'&pn='+str((int(i)*50))+'&ie=utf-8'
        rq = Request(url)
        htm = urlopen(rq)
        try:
            item.extend(cont.findall(htm.read().decode('utf-8')))
        except:
            pass
        cls_prt('[+] page:'+str(i)+'|'+str(round(i/pn,4)*100)+'%')
        htm.close()
    if '-os' in sys.argv:
        f=open(sys.argv[3],'a',encoding='utf-8')
        f.writelines(item)
        f.close()
        print('[+]','扫描已完成.')
if '-od' in sys.argv:
    f=open(sys.argv[3],encoding='utf-8')
    item=f.readlines()
    f.close()
if '-os' not in sys.argv:
    print('\n[+]','扫描已完成。开始下载')
    for it in item:
        try:
            file=now+'/'+it
            html=openp(it)
            rt=page.findall(html)
            if not rt:continue
            pages=int(rt[0])
            if pages>MAXPN:
                continue
            for n in range(pages):
                cls_prt('[+] 正在下载：'+it+'-'+str(n))
                if NRW:
                    if os.path.exists(file+'_'+str(n)+'.html',encoding='utf-8'):
                        continue
                html=openp(it,int(n))
                if NRW:
                    if not os.path.exists(file+'_'+str(n)+'.html',encoding='utf-8'):
                        f=open(file+'_'+str(n)+'.html',mode='a',encoding='utf-8')
                        f.write(html)
                        f.close()
                else:
                    try:
                        f=open(file+'_'+str(n)+'.html',mode='w',encoding='utf-8')
                    except:
                        f=open(file+'_'+str(n)+'.html',mode='a',encoding='utf-8')
                    f.write(html)
                    f.close()
        except KeyboardInterrupt:
            print('[-]','停止             ')
            sys.exit(0)
print('[+]','完成.                ')
    
