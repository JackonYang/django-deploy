# django-deploy

django 项目的快速部署模版

nginx + uwsgi + supervisord

## 基本用法

```
$ python gen.py --help
usage: python gen.py [options] path/to/django/project/

generate etc files for deploying

positional arguments:
  project_path          path of target project

optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        domain name
  -e ETC, --etc ETC     path of deploy etc
  -p VAR, --var VAR     path of var files
  -n PROCESS_NUM, --process_num PROCESS_NUM
                        maximum number of uwsgi worker processes
```

## 案例演示

#### 生成配置文件

以 [django-starter-kit](https://github.com/JackonYang/django-starter-kit) 项目为例

```shell
$ python gen.py --domain www.jackon.me ../django-starter-kit/
--------------------  options  --------------------
domain: www.jackon.me
project_name: django-starter-kit
etc_root: /Users/jackon/django-deploy/deploy_etc
media_root: /Users/jackon/django-starter-kit/media
django_socket_file: socket/django_django-starter-kit.sock
project_root: /Users/jackon/django-starter-kit
static_root: /Users/jackon/django-starter-kit/static
settings: base.settings
var_root: /Users/jackon/django-deploy/var
django_root: /Users/jackon/django-starter-kit
process_num: 4
-------------------------------------------------
```

得到 `deploy_etc` 和 `var` 2 个文件夹:

```bash
|____deploy_etc
| |____nginx
| | |____project.conf
| | |____uwsgi_params
| |____supervisor
| | |____supervisord.conf
| |____uwsgi
| | |____uwsgi.ini
| |____wsgi.py
|____var
| |____log
| |____socket
```

#### nginx & 域名

将 deploy_etc/nginx/project.conf 连接到 nginx etc 目录下。

重启 nginx

如果是本地测试，没有绑定域名，
可用修改 hosts 文件的方式测试。

修改 `/etc/hosts`,
加入

```
127.0.0.1	www.jackon.me
```

www.jackon.me 改成刚刚指定的 domain name。

#### 启动 supervisord

```
supervisord -n -c deploy_etc/supervisor/supervisord.conf
```

若要 supervisord 在后台允许，则去掉 `-n` 参数，

即

```
supervisord -c deploy_etc/supervisor/supervisord.conf
```

#### 浏览器内打开网页

网站已经成功启动，

网页就在那里。

#### supervisor ctl 管理进程的状态

进入 `supervisor>` 以后，
可以通过 start / stop / status 命令管理进程。

```
$ supervisorctl -c deploy_etc/supervisor/supervisord.conf
wsgi-django-starter-kit          RUNNING   pid 98799, uptime 0:00:06
supervisor> stop wsgi-django-starter-kit
wsgi-django-starter-kit: stopped
supervisor> start wsgi-django-starter-kit
wsgi-django-starter-kit: started
supervisor> status
wsgi-django-starter-kit          RUNNING   pid 98836, uptime 0:00:03
supervisor>
```

#### 快速重启 django 的 uwsgi 进程

```shell
$ touch deploy_etc/uwsgi/uwsgi.ini
```
