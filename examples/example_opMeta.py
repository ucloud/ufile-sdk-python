# !/usr/bin/env python
# -*- encoding: utf-8 -*-
from ufile import filemanager

bucket = ''  # 空间名称
key = ''  # 文件名称
public_key = ''  # 账户公钥
private_key = ''  # 账户私钥
metakey = 'mimetype'  # 自定义元数据键
metavalue = 'text/plain'  # 自定义元数据值

# 设置上传host后缀,外网可用后缀形如 .cn-bj.ufileos.com（cn-bj为北京地区，其他地区具体后缀可见控制台：对象存储-单地域空间管理-存储空间域名）
# 默认值为'.cn-bj.ufileos.com'，如果上传文件的bucket所在地域不在北京，请务必设置此项
upload_suffix = 'YOUR_UPLOAD_SUFFIX'

file = filemanager.FileManager(public_key, private_key, upload_suffix)

# 设置文件元数据
ret, resp = file.setfilemetakey(bucket, key, metakey, metavalue)
assert resp.status_code == 200, resp.error
print('setfilemetakey success')
