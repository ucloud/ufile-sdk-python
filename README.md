
Table of Contents
=================

   * [概述](#概述)
      * [US3 对象存储基本概念](#us3-对象存储基本概念)
      * [依赖的Python Package](#依赖的python-package)
      * [文件目录说明](#文件目录说明)
   * [安装](#安装)
      * [本地安装](#本地安装)
      * [使用 pip 安装](#使用-pip-安装)
      * [开发文档生成](#开发文档生成)
   * [快速使用](#快速使用)
   * [默认参数设置](#默认参数设置)
      * [公共参数说明](#公共参数说明)
      * [设置默认参数](#设置默认参数)
      * [设置日志文件](#设置日志文件)
   * [示例代码](#示例代码)
      * [存储空间管理](#存储空间管理)
      * [对象/文件管理](#对象文件管理)
         * [普通上传](#普通上传)
         * [表单上传](#表单上传)
         * [秒传](#秒传)
         * [分片上传和断点续传](#分片上传和断点续传)
         * [文件下载](#文件下载)
         * [删除文件](#删除文件)
         * [解冻](#解冻)
         * [文件类型转换](#文件类型转换)
         * [比较本地文件和远程文件etag](#比较本地文件和远程文件etag)
         * [获取文件列表](#获取文件列表)
         * [获取目录文件列表](#获取目录文件列表)
         * [拷贝](#拷贝)
         * [重命名](#重命名)


本源码包含使用Python对UCloud的对象存储业务US3(原名UFile)进行空间和内容管理的API，适用于Python 2(2.6及以后)和Python 3(3.3及以后)

# 概述

## US3 对象存储基本概念

在对象存储系统中，存储空间（Bucket）是文件（File）的组织管理单位，文件（File）是存储空间的逻辑存储单元。对于每个账号，该账号里存放的每个文件都有唯一的一对存储空间（Bucket）与键（Key）作为标识。我们可以把 Bucket 理解成一类文件的集合，Key 理解成文件名。由于每个 Bucket 需要配置和权限不同，每个账户里面会有多个 Bucket。在 US3 里面，Bucket 主要分为公有和私有两种，公有 Bucket 里面的文件可以对任何人开放，私有 Bucket 需要配置对应访问签名才能访问。

## 依赖的Python Package

* **requests**
可使用``` pip install requests```安装

## 文件目录说明

* docs文件夹:                 开发文档生成文件
* ufile文件夹:                SDK的具体实现
* setup.py:                  package安装文件
* test_ufile文件夹:           测试文件
* examples:                  示例代码

# 安装

## 本地安装

```bash
$ git clone https://github.com/ucloud/ufile-sdk-python.git
$ git checkout <tag/branch>
$ cd ufile-sdk-python
$ python setup.py install

#卸载
$ python setup.py install --record files.txt #获取安装程序安装的文件名
$ cat files.txt | xargs rm -rf          #删除这些文件
```

## 使用 pip 安装

```bash
$ pip install ufile
# 如果你要使用 pre-release 版本
$ pip install --pre ufile

# 如果未安装pip
# pip官网：https://pypi.org/project/pip/
# 或者使用以下方法来安装：
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py   # 下载安装脚本
$ sudo python get-pip.py    # 运行安装脚本 Python3则执行：sudo python3 get-pip.py 

#卸载
$ pip uninstall ufile
```

**注意：在国内的 pip 源会由于网络问题无法更新，建议加上国内的 python 源。**
具体请见：[如何添加 python 国内源？](https://www.baidu.com/s?wd=python%20%E5%9B%BD%E5%86%85%E6%BA%90&rsv_spt=1&rsv_iqid=0xd4c874b700022c35&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_enter=0&rsv_t=ca7cGiKHZYyi4WMSjK1f%2BXazzuAjqbqCTbXjSrEq6oiaXwF3im1hQl9E9xE9fKWkDccY&oq=python%2520%25E5%259B%25BD%25E5%2586%2585%25E6%25BA%2590&rsv_pq=ba65a2f20001ea73)

## 开发文档生成

docs文件夹包含基于sphinx的开发文档生成文件，在此文件夹下可通过运行make html命令可生成build目录，build/html目录即为开发文档

# 快速使用

```python
public_key = ''              #账户公钥
private_key = ''             #账户私钥

bucket = ''                  #公共空间名称
local_file = ''              #本地文件名
put_key = ''                 #上传文件在空间中的名称
save_file = ''               #下载文件保存的文件名

from ufile import filemanager

ufile_handler = filemanager.FileManager(public_key, private_key)

# 上传文件
ret, resp = ufile_handler.putfile(bucket, put_key, local_file, header=None)
assert resp.status_code == 200

# 下载文件
_, resp = ufile_handler.download_file(bucket, put_key, save_file)
assert resp.status_code == 200

# 遍历空间里所有文件
ret, resp = ufile_handler.getfilelist(bucket)
assert resp.status_code == 200
for object in ret["DataSet"]:
    print(object)

# 删除文件
ret, resp = ufile_handler.deletefile(bucket, put_key)
assert resp.status_code == 204
```

# 默认参数设置

ufile文件夹包含SDK的具体实现，该文件夹亦是名为ufile的package的源码文件夹


## 公共参数说明

```python
public_key = ''         #公钥或token
private_key = ''        #私钥或token
```

[如何创建一个token？](https://console.ucloud.cn/ufile/token)

## 设置默认参数

```python
from ufile import config

#设置上传host后缀,外网可用后缀形如 .cn-bj.ufileos.com（cn-bj为北京地区，其他地区具体后缀可见控制台：对象存储-单地域空间管理-存储空间域名）
config.set_default(uploadsuffix='YOUR_UPLOAD_SUFFIX')
#设置下载host后缀，普通下载后缀即上传后缀，CDN下载后缀为 .ufile.ucloud.com.cn
config.set_default(downloadsuffix='YOUR_DOWNLOAD_SUFFIX')
#设置请求连接超时时间，单位为秒
config.set_default(connection_timeout=60)
#设置私有bucket下载链接有效期,单位为秒
config.set_default(expires=60)
#设置上传文件是否校验md5
config.set_default(md5=True)
```

* 如果在实例化 FileManager 和 MultipartUploadUFile 实例时传入相关参数，则生成的实例会使用传入的值，而不是此处设置的默认值。

## 设置日志文件

```python
from ufile import logger

locallogname = '' #完整本地日志文件名
logger.set_log_file(locallogname)
```

# 示例代码

## 存储空间管理

```python
public_key = ''         #账户公钥
private_key = ''        #账户私钥

from ufile import bucketmanager

bucketmanager_handler = bucketmanager.BucketManager(public_key, private_key)

# 创建新的bucket
bucketname = '' #创建的空间名称
region = 'cn-bj'#空间所在的地理区域
ret, resp = bucketmanager_handler.createbucket(bucketname, region,'public')
assert resp.status_code == 200

# 删除bucket
bucketname = '' #待删除的空间名称
ret, resp = bucketmanager_handler.deletebucket(bucketname)
print(ret)

# 获取bucket信息
bucketname = '' # 待查询的空间名称
ret, resp = bucketmanager_handler.describebucket(bucketname)
print(ret)

# 更改bucket属性
bucketname = '' # 待更改的私有空间名称
bucketmanager_handler.updatebucket(bucketname, 'public')
```

## 对象/文件管理

### 普通上传

* demo 程序

```python
public_key = ''         #账户公钥
private_key = ''        #账户私钥

public_bucket = ''      #公共空间名称
private_bucket = ''     #私有空间名称
local_file = ''         #本地文件名
put_key = ''            #上传文件在空间中的名称

from ufile import filemanager

putufile_handler = filemanager.FileManager(public_key, private_key)

# 普通上传文件至公共空间
ret, resp = putufile_handler.putfile(public_bucket, put_key, local_file, header=None)
assert resp.status_code == 200

# 普通上传文件至私有空间
ret, resp = putufile_handler.putfile(private_bucket, put_key, local_file, header=None)
assert resp.status_code == 200

# 普通上传二进制数据流至公共空间
from io import BytesIO
bio = BytesIO(u'Do be a good man'.encode('utf-8'))  #二进制数据流
stream_key = ''                         #上传数据流在空间中的名称
ret, resp = putufile_handler.putstream(public_bucket, stream_key, bio)
```

* HTTP 返回状态码

| 状态码 | 描述                 |
| ------ | -------------------- |
| 200    | 文件或者数据上传成功 |
| 400    | 上传到不存在的空间   |
| 403    | API公私钥错误        |
| 401    | 上传凭证错误         |

### 表单上传

* demo程序

```python
public_key = ''         #账户公钥
private_key = ''        #账户私钥

public_bucket = ''      #公共空间名称
private_bucket = ''     #私有空间名称
local_file = ''         #本地文件名
post_key = ''           #上传文件在空间中的名称

from ufile import filemanager

postufile_handler = filemanager.FileManager(public_key, private_key)

# 表单上传至公共空间
ret, resp = postufile_handler.postfile(public_bucket, post_key, local_file)
assert resp.status_code == 200

# 表单上传至私有空间
ret, resp = postufile_handler.postfile(private_bucket, post_key, local_file)
assert resp.status_code == 200
```

* HTTP 返回状态码

| 状态码 | 描述                 |
| ------ | -------------------- |
| 200    | 文件或者数据上传成功 |
| 400    | 上传到不存在的空间   |
| 403    | API公私钥错误        |
| 401    | 上传凭证错误         |

### 秒传

* demo程序

```python
public_key = ''         #账户公钥
private_key = ''        #账户私钥

public_bucket = ''      #公共空间名称
existkey = ''           #添加上传文件在空间中的名称
nonexistkey = ''        #添加上传文件在空间中的名称
existfile = ''          #本地文件名(空间存在该文件)
nonexistfile = ''       #本地文件名((空间不存在该文件))

from ufile import filemanager

uploadhitufile_handler = filemanager.FileManager(public_key, private_key)

# 秒传已存在文件
ret, resp = uploadhitufile_handler.uploadhit(public_bucket, existkey, existfile)
assert resp.status_code == 200

# 秒传不存在文件
ret, resp = uploadhitufile_handler.uploadhit(public_bucket, nonexistkey, nonexistfile)
assert resp.status_code == 404
```

* HTTP 状态返回码

| 状态码 | 描述               |
| ------ | ------------------ |
| 200    | 文件秒传成功       |
| 400    | 上传到不存在的空间 |
| 403    | API公私钥错误      |
| 401    | 上传凭证错误       |
| 404    | 文件秒传失败       |

### 分片上传和断点续传

* demo程序

```python
public_key = ''         #账户公钥
private_key = ''        #账户私钥

public_bucket = ''      #公共空间名称
sharding_key = ''       #上传文件在空间中的名称
local_file = ''         #本地文件名

from ufile import multipartuploadufile

multipartuploadufile_handler = multipartuploadufile.MultipartUploadUFile(public_key, private_key)

# 分片上传一个全新的文件
ret, resp = multipartuploadufile_handler.uploadfile(public_bucket, sharding_key, local_file)
while True:
    if resp.status_code == 200: # 分片上传成功
        break
    elif resp.status_code == -1:    # 网络连接问题，续传
        ret, resp = multipartuploadufile_handler.resumeuploadfile()
    else:   # 服务或者客户端错误
        print(resp.error)
        break

# 分片上传一个全新的二进制数据流
from io import BytesIO
bio = BytesIO(u'你好'.encode('utf-8'))
ret, resp = multipartuploadufile_handler.uploadstream(public_bucket, sharding_key, bio)
while True:
    if resp.status_code == 200:     # 分片上传成功
        break
    elif resp.status_code == -1:    # 网络连接问题，续传
        ret, resp = multipartuploadufile_handler.resumeuploadstream()
    else:   # 服务器或者客户端错误
        print(resp.error)
        break
```

* HTTP 返回状态码

| 状态码 | 描述                 |
| ------ | -------------------- |
| 200    | 文件或者数据上传成功 |
| 400    | 上传到不存在的空间   |
| 403    | API公私钥错误        |
| 401    | 上传凭证错误         |

### 文件下载

* demo程序

```python
public_key = ''                 #账户公钥
private_key = ''                #账户私钥

public_bucket = ''              #公共空间名称
private_bucket = ''             #私有空间名称
public_savefile = ''            #保存文件名
private_savefile = ''           #保存文件名
range_savefile = ''             #保存文件名
put_key = ''                    #文件在空间中的名称
stream_key = ''                 #文件在空间中的名称

from ufile import filemanager

downloadufile_handler = filemanager.FileManager(public_key, private_key)

# 从公共空间下载文件
ret, resp = downloadufile_handler.download_file(public_bucket, put_key, public_savefile, isprivate=False)
assert resp.status_code == 200

# 从私有空间下载文件
ret, resp = downloadufile_handler.download_file(private_bucket, put_key, private_savefile)
assert resp.status_code == 200

# 下载包含文件范围请求的文件
ret, resp = downloadufile_handler.download_file(public_bucket, put_key, range_savefile, isprivate=False, expires=300, content_range=(0, 15))
assert resp.status_code == 206
```

* HTTP 返回状态码

| 状态码 | 描述                     |
| ------ | ------------------------ |
| 200    | 文件或者数据下载成功     |
| 206    | 文件或者数据范围下载成功 |
| 400    | 不存在的空间             |
| 403    | API公私钥错误            |
| 401    | 下载签名错误             |
| 404    | 下载文件或数据不存在     |
| 416    | 文件范围请求不合法       |

### 删除文件

* demo程序

```python
public_key = ''                 #账户公钥
private_key = ''                #账户私钥

public_bucket = ''              #公共空间名称
private_bucekt = ''             #私有空间名称
delete_key = ''                 #文件在空间中的名称

from ufile import filemanager

deleteufile_handler = filemanager.FileManager(public_key, private_key)

# 删除公共空间的文件
ret, resp = deleteufile_handler.deletefile(public_bucket, delete_key)
assert resp.status_code == 204

# 删除私有空间的文件
ret, resp = deleteufile_handler.deletefile(private_bucket, delete_key)
assert resp.status_code == 204
```

* HTTP 返回状态码

| 状态码 | 描述                 |
| ------ | -------------------- |
| 204    | 文件或者数据删除成功 |
| 403    | API公私钥错误        |
| 401    | 签名错误             |

### 解冻

* demo 程序

```python
public_key = ''                 #账户公钥
private_key = ''                #账户私钥

public_bucket = ''              #公共空间名称
local_file = ''                 #本地文件名
put_key = ''                    #上传文件在空间中的名称
ARCHIVE = 'ARCHIVE'             #冷存文件类型

from ufile import filemanager

putufile_handler = filemanager.FileManager(public_key, private_key)
restorefile_handler = filemanager.FileManager(public_key, private_key)

# 普通上传归档类型的文件至公共空间
header = dict()
header['X-Ufile-Storage-Class'] = ARCHIVE
ret, resp = putufile_handler.putfile(public_bucket, put_key, local_file,  header=header)
assert resp.status_code == 200

# 解冻归档类型的文件
ret, resp = restorefile_handler.restore_file(public_bucket, put_key)
assert resp.status_code == 200
```

* HTTP 返回状态码

| 状态码 | 描述                           |
| ------ | ------------------------------ |
| 200    | 文件解冻成功                   |
| 400    | 不存在的空间 或 文件类型非冷存 |
| 403    | API公私钥错误                  |
| 401    | 上传凭证错误                   |

### 文件类型转换

* demo 程序

```python
public_key = ''                 #账户公钥
private_key = ''                #账户私钥

public_bucket = ''              #公共空间名称
local_file = ''                 #本地文件名
put_key = ''                    #上传文件在空间中的名称
STANDARD = 'STANDARD'           #标准文件类型
IA = 'IA'                       #低频文件类型

from ufile import filemanager

putufile_handler = filemanager.FileManager(public_key, private_key)
classswitch_handler = filemanager.FileManager(public_key, private_key)

# 普通上传文件至公共空间
header = dict()
header['X-Ufile-Storage-Class'] = STANDARD
ret, resp = putufile_handler.putfile(public_bucket, put_key, local_file, header=header)
assert resp.status_code == 200

# 标准文件类型转换为低频文件类型
ret, resp = classswitch_handler.class_switch_file(public_bucket, put_key, IA)
assert resp.status_code == 200
```

* HTTP 返回状态码

| 状态码 | 描述                                                |
| ------ | --------------------------------------------------- |
| 200    | 文件转换类型成功                                    |
| 400    | 不存在的空间                                        |
| 403    | API公私钥错误 或 冷存文件尚未解冻不允许转换文件类型 |
| 401    | 上传凭证错误                                        |

### 比较本地文件和远程文件etag

```python
from ufile import filemanager

public_key = ''                 #账户公钥
private_key = ''                #账户私钥

public_bucket = ''              #添加公共空间名称
put_key = ''                    #添加远程文件key
local_file=''                   #添加本地文件路径

compare_handler = filemanager.FileManager(public_key, private_key)
result=compare_handler.compare_file_etag(public_bucket,put_key,local_file)
if result==True:
    print('etag are the same!')
else:
    print('etag are different!')
```

### 获取文件列表

```python
public_key = ''                 #账户公钥
private_key = ''                #账户私钥

bucket = ''                     #添加空间名称

from ufile import filemanager

getfilelist_hander = filemanager.FileManager(public_key, private_key)

prefix='' #文件前缀
limit=10  #文件列表数目
marker='' #文件列表起始位置
ret, resp = getfilelist_hander.getfilelist(bucket, prefix=prefix, limit=limit, marker=marker)
assert resp.status_code == 200
for object in ret["DataSet"]:
    print(object)
```

### 获取目录文件列表

```python
public_key = ''                 #账户公钥
private_key = ''                #账户私钥

bucket = ''                     #添加空间名称

from ufile import filemanager

listobjects_hander = filemanager.FileManager(public_key, private_key)

prefix=''     #以prefix作为前缀的目录文件列表
maxkeys=100   #指定返回目录文件列表的最大数量
marker=''     #返回以字母排序后，大于marker的目录文件列表
delimiter='/' #delimiter是目录分隔符，当前只"/"和" "，当Delimiter设置为"/"时，返回目录形式的文件列表，当delimiter设置为" "时，返回非目录层级文件列表

ret, resp = listobjects_hander.listobjects(bucket, prefix=prefix, maxkeys=maxkeys, marker=marker, delimiter=delimiter)
assert resp.status_code == 200
```

### 拷贝

* demo 程序

```python
public_key = ''                 #账户公钥
private_key = ''                #账户私钥
public_bucket = ''              #公共空间名称
key = ''                        #目的文件在空间中的名称
srcbucket = ''                  #源文件所在空间名称
srckey = ''                     #源文件名称

from ufile import filemanager

copyufile_handler = filemanager.FileManager(public_key, private_key)

# 拷贝文件
ret, resp = copyufile_handler.copy(public_bucket, key, srcbucket, srckey)
assert resp.status_code == 200
```

* HTTP 返回状态码

| 状态码 | 描述          |
| ------ | ------------- |
| 200    | 文件拷贝成功  |
| 400    | 不存在的空间  |
| 403    | API公私钥错误 |
| 401    | 上传凭证错误  |

### 重命名

* demo 程序

```python
public_key = ''                 #账户公钥
private_key = ''                #账户私钥

public_bucket = ''              #公共空间名称
key = ''                        #源文件在空间中的名称
newkey = ''                     #目的文件在空间中的名称

from ufile import filemanager

renameufile_handler = filemanager.FileManager(public_key, private_key)

# 重命名文件
ret, resp = renameufile_handler.rename(public_bucket, key, newkey, 'true')
assert resp.status_code == 200
```

* HTTP 返回状态码

| 状态码 | 描述           |
| ------ | -------------- |
| 200    | 文件重命名成功 |
| 400    | 不存在的空间   |
| 403    | API公私钥错误  |
| 401    | 上传凭证错误   |
| 406    | 新文件名已存在 |
