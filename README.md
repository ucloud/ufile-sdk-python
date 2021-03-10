# UCloud 对象存储 Python-SDK

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
   * [版本记录](#版本记录)
   * [更多使用](#更多使用)
   * [联系我们](#联系我们)

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

[回到目录](#table-of-contents)

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

#卸载
$ pip uninstall ufile
```

**注意：在国内的 pip 源会由于网络问题无法更新，建议加上国内的 python 源。**

## 开发文档生成

源码中的docs文件夹包含基于sphinx的开发文档生成文件，下载相应的SDK包后，进入此文件夹，然后执行命令`make html`命令可生成build目录，build/html目录即为开发文档。

注：Windows下可使用`.\make.bat html`命令生成build目录

[回到目录](#table-of-contents)

# 快速使用

```python
# 密钥可在https://console.ucloud.cn/uapi/apikey中获取
public_key = ''              #账户公钥
private_key = ''             #账户私钥

bucket = ''                  #空间名称
local_file = ''              #本地文件名
put_key = ''                 #上传文件在空间中的名称
save_file = ''               #下载文件保存的文件名

from ufile import config,filemanager

#以下两项如果不设置，则默认设为'.cn-bj.ufileos.com'，如果上传、下载文件的bucket所在地域不在北京，请务必设置以下两项。
#设置上传host后缀,外网可用后缀形如 .cn-bj.ufileos.com（cn-bj为北京地区，其他地区具体后缀可见控制台：对象存储-单地域空间管理-存储空间域名）
config.set_default(uploadsuffix='YOUR_UPLOAD_SUFFIX')
#设置下载host后缀，普通下载后缀即上传后缀，CDN下载后缀为 .ufile.ucloud.com.cn
config.set_default(downloadsuffix='YOUR_DOWNLOAD_SUFFIX')

ufile_handler = filemanager.FileManager(public_key, private_key)

# 上传文件
ret, resp = ufile_handler.putfile(bucket, put_key, local_file, header=None)
assert resp.status_code == 200

# 下载文件
_, resp = ufile_handler.download_file(bucket, put_key, save_file)
assert resp.status_code == 200

# 遍历空间里文件(默认数目为20)
ret, resp = ufile_handler.getfilelist(bucket)
assert resp.status_code == 200
for object in ret["DataSet"]:
    print(object)

# 删除文件
ret, resp = ufile_handler.deletefile(bucket, put_key)
assert resp.status_code == 204
```
[回到目录](#table-of-contents)

# 参数设置


## 设置公共参数

```python
public_key = ''         #公钥或token
private_key = ''        #私钥或token
```

* 密钥可以在控制台中 [API 产品 - API 密钥](https://console.ucloud.cn/uapi/apikey)，点击显示 API 密钥获取。将 public_key 和 private_key 分别赋值给相关变量后，SDK即可通过此密钥完成鉴权。请妥善保管好 API 密钥，避免泄露。
* token（令牌）是针对指定bucket授权的一对公私钥。可通过token进行授权bucket的权限控制和管理。可以在控制台中[对象存储US3-令牌管理](https://console.ucloud.cn/ufile/token)，点击创建令牌获取。
* 管理 bucket 创建和删除必须要公私钥，如果只做文件上传和下载用 TOEKN 就够了，为了安全，强烈建议只使用 TOKEN 做文件管理

## 设置默认参数

```python
from ufile import config

#设置上传host后缀,外网可用后缀形如 .cn-bj.ufileos.com（cn-bj为北京地区，其他地区具体后缀可见控制台：对象存储-单地域空间管理-存储空间域名）
#默认值为'.cn-bj.ufileos.com'，如果上传文件的bucket所在地域不在北京，请务必设置此项
config.set_default(uploadsuffix='YOUR_UPLOAD_SUFFIX')
#设置下载host后缀，普通下载后缀即上传后缀，CDN下载后缀为 .ufile.ucloud.com.cn
config.set_default(downloadsuffix='YOUR_DOWNLOAD_SUFFIX')
#设置请求连接超时时间，单位为秒
config.set_default(connection_timeout=60)
#设置私有bucket下载链接有效期,单位为秒
config.set_default(expires=60)
#设置上传文件是否进行数据完整性校验（现仅支持putifle和putstream）
config.set_default(md5=True)
```

* 如果在实例化 FileManager 和 MultipartUploadUFile 实例时传入相关参数，则生成的实例会使用传入的值，而不是此处设置的默认值。

## 设置日志文件

```python
from ufile import logger

locallogname = '' #完整本地日志文件名
logger.set_log_file(locallogname)
```

[回到目录](#table-of-contents)

# 版本记录

[UFileSDK release history](https://github.com/ucloud/ufile-sdk-python/blob/master/CHANGELOG/CHANGELOG-3.2.md)

# 更多使用

* [更多例子](https://github.com/ucloud/ufile-sdk-python/tree/master/examples)
* UCloud US3 [开发者文档](https://ucloud-us3.github.io/python-sdk/概述.html)

# 联系我们

- UCloud US3 [UCloud官方网站](https://www.ucloud.cn/)
- UCloud US3 [官方文档中心](https://docs.ucloud.cn/ufile/README)
- UCloud 官方技术支持：[提交工单](https://accountv2.ucloud.cn/work_ticket/create)
- 提交[issue](https://github.com/ucloud/ufile-sdk-python/issues)

