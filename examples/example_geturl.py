# !/usr/bin/env python
# -*- encoding: utf-8 -*-
from ufile import filemanager

public_key = ''  # 账户公钥
private_key = ''  # 账户私钥

bucket = ''  # 空间名称
key = ''  # 文件在空间中的名称

# 设置上传host后缀,外网可用后缀形如 .cn-bj.ufileos.com（cn-bj为北京地区，其他地区具体后缀可见控制台：对象存储-单地域空间管理-存储空间域名）
# 默认值为'.cn-bj.ufileos.com'，如果上传文件的bucket所在地域不在北京，请务必设置此项
upload_suffix = '.cn-bj.ufileos.com'
# 设置下载host后缀，普通下载后缀即上传后缀，CDN下载后缀为 .ufile.ucloud.com.cn
download_suffix = '.cn-bj.ufileos.com'

getufile_handler = filemanager.FileManager(public_key, private_key, upload_suffix, download_suffix)

# 判断文件是否存在
_, resp = getufile_handler.head_file(bucket, key)
assert resp.status_code == 200, "status: %d error: %s" % (resp.status_code, resp.error)

# 获取公有空间下载url
url = getufile_handler.public_download_url(bucket, key)
print("公有云空间下载URL: %s" % url)

# 获取私有空间下载url, expires为下载链接有效期，单位为秒
url = getufile_handler.private_download_url(bucket, key, expires=60)
print("私有云空间下载URL: %s" % url)
