import os
now=os.getcwd()+'/download'
if not os.path.exists(now):os.mkdir(now)
now=os.getcwd()+'/map'
if not os.path.exists(now):os.mkdir(now)
now=os.getcwd()+'/img'
if not os.path.exists(now):os.mkdir(now)
print('安装操作已完成.')
