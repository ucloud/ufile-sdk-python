
Table of Contents
=================

   * [概述](#概述)
      * [文件目录说明](#文件目录说明)
   * [安装](#安装)
      * [本地安装](#本地安装)
      * [使用 pip 安装](#使用-pip-安装)
      * [开发文档生成](#开发文档生成)
   * [快速使用](#快速使用)
   * [参数设置](#参数设置)
      * [设置公共参数](#设置公共参数)
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
   * [版本记录](#版本记录)
   * [联系我们](#联系我们)


本源码包含使用Python对UCloud的对象存储业务US3(原名UFile)进行空间和内容管理的API，适用于Python 2(2.6及以后)和Python 3(3.3及以后)。

# 概述

本源码包含使用Python对UCloud的对象存储业务US3(原名UFile)进行空间和内容管理的API，适用于Python 2(2.6及以后)和Python 3(3.3及以后)。

## 文件目录说明

```shell
UFILE-SDK-PYTHON
├─docs               开发文档生成目录
├─examples           示例代码存放目录
├─setup.py           package安装文件
├─test_ufile         测试文件存放目录
├─ufile              SDK的具体实现
```

# 安装

## 本地安装

```bash
$ git clone https://github.com/ucloud/ufile-sdk-python.git
$ git checkout <tag/branch>
$ cd ufile-sdk-python
$ python setup.py install

#卸载
$ python setup.py install --record files.txt #获取安装程序安装的文件名
$ cat files.txt | xargs rm -rf               #删除这些文件
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

## 开发文档生成

docs文件夹包含基于sphinx的开发文档生成文件，在此文件夹下可通过运行make html命令可生成build目录，build/html目录即为开发文档。

# 快速使用

```python
# 密钥可在https://console.ucloud.cn/uapi/apikey中获取
public_key = ''              #账户公钥
private_key = ''             #账户私钥

bucket = ''                  #空间名称
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

# 参数设置


## 设置公共参数

```python
public_key = ''         #公钥或token
private_key = ''        #私钥或token
```

* 密钥可以在控制台中 [API 产品 - API 密钥](https://console.ucloud.cn/uapi/apikey)，点击显示 API 密钥获取。将 public_key 和 private_key 分别赋值给相关变量后，SDK即可通过此密钥完成鉴权。请妥善保管好 API 密钥，避免泄露。

* token（令牌）是针对指定bucket授权的一对公私钥。可通过token进行授权bucket的权限控制和管理。可以在控制台中[对象存储US3-令牌管理](https://console.ucloud.cn/ufile/token)，点击创建令牌获取。

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

* 说明
  * 在上传文件（Object）到 US3 之前，您需要使用 createbucket来创建一个用于存储文件的存储空间（Bucket），存储空间具有各种配置属性，包括地域、访问权限以及其他元数据。
  * 必、删除存储空间中的所有文件和未完成的分片文件后，存储空间才能成功删除。如果存储空间不为空（存储空间中有文件或者是尚未完成的分片上传），则存储空间无法删除。
  
* demo程序

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

* 说明
  * 普通上传适用于一次HTTP请求交互即可完成上传的场景，比如小文件（小于1GB）的上传。
  * 大文件（大于1GB）的上传请使用分片上传。

* demo 程序

```python
public_key = ''         #账户公钥
private_key = ''        #账户私钥

bucket = ''             #空间名称
local_file = ''         #本地文件名
put_key = ''            #上传文件在空间中的名称

from ufile import filemanager

putufile_handler = filemanager.FileManager(public_key, private_key)

# 普通上传文件至空间
ret, resp = putufile_handler.putfile(bucket, put_key, local_file, header=None)
assert resp.status_code == 200

# 普通上传二进制数据流至空间
from io import BytesIO
bio = BytesIO(u'Do be a good man'.encode('utf-8'))  #二进制数据流
stream_key = ''                                     #上传数据流在空间中的名称
ret, resp = putufile_handler.putstream(bucket, stream_key, bio)
```

* HTTP 返回状态码

| 状态码 | 描述                 |
| ------ | -------------------- |
| 200    | 文件或者数据上传成功 |
| 400    | 上传到不存在的空间   |
| 403    | API公私钥错误        |
| 401    | 上传凭证错误         |

### 表单上传

* 说明
  * 适合嵌入在HTML网页中来上传Object，比较常见的场景是网站应用。
  * 上传的Object不能超过1GB。
* demo程序

```python
public_key = ''         #账户公钥
private_key = ''        #账户私钥

bucket = ''             #空间名称
local_file = ''         #本地文件名
post_key = ''           #上传文件在空间中的名称

from ufile import filemanager

postufile_handler = filemanager.FileManager(public_key, private_key)

# 表单上传文件至空间
ret, resp = postufile_handler.postfile(bucket, post_key, local_file)
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

* 说明
  * 先判断待上传文件的hash值，如果US3中可以查到此文件，则不必再传文件本身。

* demo程序

```python
public_key = ''         #账户公钥
private_key = ''        #账户私钥

bucket = ''             #空间名称
existkey = ''           #添加上传文件在空间中的名称
nonexistkey = ''        #添加上传文件在空间中的名称
existfile = ''          #本地文件名(空间存在该文件)
nonexistfile = ''       #本地文件名((空间不存在该文件))

from ufile import filemanager

uploadhitufile_handler = filemanager.FileManager(public_key, private_key)

# 秒传已存在文件
ret, resp = uploadhitufile_handler.uploadhit(bucket, existkey, existfile)
assert resp.status_code == 200

# 秒传不存在文件
ret, resp = uploadhitufile_handler.uploadhit(bucket, nonexistkey, nonexistfile)
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

* 说明
  * 将要上传的文件分成多个数据块（US3 里又称之为 Part）来分别上传，上传完成之后再调将这些 Part 组合成一个 Object 来达到断点续传的效果。
* 适用场景
  1. 大文件（大于1GB）的上传。
  2. 恶劣的网络环境：如果上传的过程中出现了网络错误，可以从失败的Part进行续传。其他上传方式则需要从文件起始位置上传。
  3. 流式上传：可以在需要上传的文件大小还不确定的情况下开始上传。这种场景在视频监控等行业应用中比较常见。
* demo程序

```python
public_key = ''         #账户公钥
private_key = ''        #账户私钥

bucket = ''             #空间名称
sharding_key = ''       #上传文件在空间中的名称
local_file = ''         #本地文件名

from ufile import multipartuploadufile

multipartuploadufile_handler = multipartuploadufile.MultipartUploadUFile(public_key, private_key)

# 分片上传一个全新的文件
ret, resp = multipartuploadufile_handler.uploadfile(bucket, sharding_key, local_file)
while True:
    if resp.status_code == 200:     # 分片上传成功
        break
    elif resp.status_code == -1:    # 网络连接问题，续传
        ret, resp = multipartuploadufile_handler.resumeuploadfile()
    else:                           # 服务或者客户端错误
        print(resp.error)
        break

# 分片上传一个全新的二进制数据流
from io import BytesIO
bio = BytesIO(u'你好'.encode('utf-8'))
ret, resp = multipartuploadufile_handler.uploadstream(bucket, sharding_key, bio)
while True:
    if resp.status_code == 200:     # 分片上传成功
        break
    elif resp.status_code == -1:    # 网络连接问题，续传
        ret, resp = multipartuploadufile_handler.resumeuploadstream()
    else:                           # 服务器或者客户端错误
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

* 说明
  * 下载UFile文件并且保存为本地文件。
  * 可以从 Object 指定的位置开始下载，在下载大的 Object 的时候，可以分多次下载。
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

* 说明
  * 删除存储空间（Bucket）中的文件。
* demo程序

```python
public_key = ''                 #账户公钥
private_key = ''                #账户私钥

bucket = ''                     #空间名称
delete_key = ''                 #文件在空间中的名称

from ufile import filemanager

deleteufile_handler = filemanager.FileManager(public_key, private_key)

# 删除空间的文件
ret, resp = deleteufile_handler.deletefile(bucket, delete_key)
assert resp.status_code == 204
```

* HTTP 返回状态码

| 状态码 | 描述                 |
| ------ | -------------------- |
| 204    | 文件或者数据删除成功 |
| 403    | API公私钥错误        |
| 401    | 签名错误             |

### 解冻

* 说明
  * 用于解冻归档类型的文件。
* demo 程序

```python
public_key = ''                 #账户公钥
private_key = ''                #账户私钥

bucket = ''                     #空间名称
local_file = ''                 #本地文件名
put_key = ''                    #上传文件在空间中的名称
ARCHIVE = 'ARCHIVE'             #冷存文件类型

from ufile import filemanager

putufile_handler = filemanager.FileManager(public_key, private_key)
restorefile_handler = filemanager.FileManager(public_key, private_key)

# 普通上传归档类型的文件至空间
header = dict()
header['X-Ufile-Storage-Class'] = ARCHIVE
ret, resp = putufile_handler.putfile(bucket, put_key, local_file,  header=header)
assert resp.status_code == 200

# 解冻归档类型的文件
ret, resp = restorefile_handler.restore_file(bucket, put_key)
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

* 说明
  * 用于转换文件的存储类型，可以任意转换文件为标准、低频、冷存三种存储类型。
  * 注意：冷存文件如果想转换为其他两种类型必须在解冻期内。
* demo 程序

```python
public_key = ''                 #账户公钥
private_key = ''                #账户私钥

bucket = ''                     #空间名称
local_file = ''                 #本地文件名
put_key = ''                    #上传文件在空间中的名称
STANDARD = 'STANDARD'           #标准文件类型
IA = 'IA'                       #低频文件类型

from ufile import filemanager

putufile_handler = filemanager.FileManager(public_key, private_key)
classswitch_handler = filemanager.FileManager(public_key, private_key)

# 普通上传文件至空间
header = dict()
header['X-Ufile-Storage-Class'] = STANDARD
ret, resp = putufile_handler.putfile(bucket, put_key, local_file, header=header)
assert resp.status_code == 200

# 标准文件类型转换为低频文件类型
ret, resp = classswitch_handler.class_switch_file(bucket, put_key, IA)
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

* 说明
  * 判断文件的完整性，用于判断文件上传、下载过程中是否发生丢失。
* demo 程序

```python
from ufile import filemanager

public_key = ''                 #账户公钥
private_key = ''                #账户私钥

bucket = ''                     #添加空间名称
put_key = ''                    #添加远程文件key
local_file=''                   #添加本地文件路径

compare_handler = filemanager.FileManager(public_key, private_key)
result=compare_handler.compare_file_etag(bucket,put_key,local_file)
if result==True:
    print('etag are the same!')
else:
    print('etag are different!')
```

### 获取文件列表

* 说明
  * 获取存储空间（Bucket）中指定文件前缀的文件列表。
* demo 程序

```python
public_key = ''                 #账户公钥
private_key = ''                #账户私钥

bucket = ''                     #空间名称

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

* 说明
  * 获取存储空间（Bucket）中指定目录下的文件列表。
* demo 程序

```python
public_key = ''                 #账户公钥
private_key = ''                #账户私钥

bucket = ''                     #空间名称

from ufile import filemanager

listobjects_hander = filemanager.FileManager(public_key, private_key)

prefix=''     #以prefix作为前缀的目录文件列表
maxkeys=100   #指定返回目录文件列表的最大数量
marker=''     #返回以字母排序后，大于marker的目录文件列表
delimiter='/' #delimiter是目录分隔符，当前只"/"和""，当Delimiter设置为"/"且prefiex以"/"结尾时，返回prefix目录下的子文件（不包含目录文件），当delimiter设置为""时，返回以prefix作为前缀的文件

ret, resp = listobjects_hander.listobjects(bucket, prefix=prefix, maxkeys=maxkeys, marker=marker, delimiter=delimiter)
assert resp.status_code == 200
```

### 拷贝

* 说明
  * 跨存储空间（Bucket）复制文件。
* demo 程序

```python
public_key = ''                 #账户公钥
private_key = ''                #账户私钥
bucket = ''                     #空间名称
key = ''                        #目的文件在空间中的名称
srcbucket = ''                  #源文件所在空间名称
srckey = ''                     #源文件名称

from ufile import filemanager

copyufile_handler = filemanager.FileManager(public_key, private_key)

# 拷贝文件
ret, resp = copyufile_handler.copy(bucket, key, srcbucket, srckey)
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

* 说明
  * 重命名存储空间（Bucket）中的文件。
* demo 程序

```python
public_key = ''                 #账户公钥
private_key = ''                #账户私钥

bucket = ''                     #空间名称
key = ''                        #源文件在空间中的名称
newkey = ''                     #目的文件在空间中的名称

from ufile import filemanager

renameufile_handler = filemanager.FileManager(public_key, private_key)

# 重命名文件
ret, resp = renameufile_handler.rename(bucket, key, newkey, 'true')
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

# 版本记录

[UFileSDK release history](https://github.com/ucloud/ufile-sdk-python/blob/master/CHANGELOG/CHANGELOG-3.2.md)

# 联系我们

- [UCloud官方网站: https://www.ucloud.cn/](https://www.ucloud.cn/)
- 如有任何问题，欢迎提交[issue](https://github.com/ucloud/ufile-sdk-python/issues)或联系我们的技术支持，我们会第一时间解决问题。