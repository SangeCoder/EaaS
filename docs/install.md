## Jumpserver v0.4.0 版本安装详细过程

### 环境

- 系统: CentOS 6.5 x86\_64 mini
- Python: 版本 2.7.13 (未来支持 3.5)
- 安装目录 
	- /opt/jumpserver
	- /opt/coco

#### 一. 环境准备

##### 1.1 安装基本工具和库

	$ yum -y install sqlite-devel git epel-release
	$ yum -y install python-devel libffi-devel openssl-devel
	$ yum -y install gcc gcc-c++
	
	
##### 1.2 安装Python

这里可以参考 [https://segmentfault.com/a/1190000000654227][1] 也可以下载我编译的rpm版本:

	$ wget http://repo.jumpserver.org/python27-2.7.13-1.el6.x86_64.rpm 	
	$ yum localinstall -y python27-2.7.13-1.el6.x86_64.rpm	
	$ bash	
	$ python2.7 -V	
	Python 2.7.13
	
设置默认python版本为2.7.13:
```
$ mv /usr/bin/python /usr/bin/python.bak	
$ which python2.7
/data/server/python27/bin/python2.7
$ ln -s /data/server/python27/bin/python2.7 /usr/bin/python
$python
Python 2.7.13
```	
设置yum默认python用2.6:
```
$ vim /usr/bin/yum
#!/usr/bin/python2.6

```

#### 二. Jumpserver安装

##### 2.1 下载仓库代码

	$ cd /opt
	$ git clone https://github.com/jumpserver/jumpserver.git
	$ cd jumpserver
	$ git checkout dev

##### 2.2 安装依赖

	$ cd requirements 
	$ sudo yum -y install `cat rpm_requirements.txt`
	$ pip2.7 install -r requirements.txt -i https://pypi.doubanio.com/simple


##### 2.3 准备配置文件

	$ cd ..
	$ cp config_example.py config.py
	$ vim config.py

	// 默认使用的是 DevelpmentConfig 所以应该去修改这部分
	class DevelopmentConfig(Config):
	EMAIL_HOST = 'smtp.exmail.qq.com'
	EMAIL_PORT = 465
	EMAIL_HOST_USER = 'ask@jumpserver.org'
	EMAIL_HOST_PASSWORD = 'xxx'
	EMAIL_USE_SSL = True   // 端口是 465 设置 True 否则 False
	EMAIL_USE_TLS = False  // 端口是 587 设置为 True 否则 False
	SITE_URL = 'http://localhost:8080'  // 发送邮件会使用这个地址 

##### 2.4 初始化数据库

	$ cd utils
	$ sh make_migrations.sh
	$ sh init_db.sh

##### 2.5 安装redis server

	$ yum -y install redis
	$ service redis start  

**2.6 启动**
```
$ cd ..
$ python2.7 run_server.py
```
访问  http://ip:8080
账号密码： admin admin

**2.7 测试使用**
- 创建用户  
	会发送邮件，测试是否正常修改密码，登录

- 创建管理用户
	创建一个管理用户， 创建资产时需要关联

- 创建资产
	创建一个 资产，关联刚创建的管理用户

- 创建系统用户
	系统用户是用来登录资产的，授权时需要

- 创建授权规则
	关联用户，资产，系统用户 形成授权规则，授权的系统用户会自动推送到资产上


#### 三. 安装 SSH SERVER - COCO
**3.1 下载代码库**
```
$ cd /opt
$ git clone https://github.com/jumpserver/coco.git
```

**3.2 安装依赖**
```
$ cd coco
$ pip2.7 install -r requirements.txt -i https://pypi.doubanio.com/simple
```

**3.3 启动**

```
$ python2.7 run_server.py
```

说明： Coco启动后会向jumpserver注册，请去 jumpserver页面 - 应用程序 - terminal - coco - Accept 允许， 这时 coco就 运行在 2222端口，可以ssh来连接

命令行：
``` 
ssh admin@192.168.244.128 -p2222
```

**3.5 测试**
- 测试登录 ssh server
- 测试跳转
- 测试命令记录回

[1]:	https://segmentfault.com/a/1190000000654227
[2]:	https://github.com/jumpserver/jumpserver.git
[3]:	https://github.com/jumpserver/coco.git
