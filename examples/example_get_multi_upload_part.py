# !/usr/bin/env python
# -*- encoding: utf-8 -*-

from ufile import multipartuploadufile, filemanager

public_key = ''  # 账户公钥
private_key = ''  # 账户私钥

bucket = ''  # 空间名称
upload_id = ''  # 上传分片ID
max_parts = None  # 最大分片数目
part_number_marker = None  # 起始分片编号

# 设置上传host后缀,外网可用后缀形如 .cn-bj.ufileos.com（cn-bj为北京地区，其他地区具体后缀可见控制台：对象存储-单地域空间管理-存储空间域名）
# 默认值为'.cn-bj.ufileos.com'，如果上传文件的bucket所在地域不在北京，请务必设置此项
upload_suffix = '.cn-bj.ufileos.com'

multi_part_upload_ufile_handler = multipartuploadufile.MultipartUploadUFile(public_key, private_key, upload_suffix)

ret, resp = multi_part_upload_ufile_handler.get_multi_upload_part(bucket, upload_id, max_parts, part_number_marker,
                                                                  upload_suffix=upload_suffix)
assert resp.status_code == 200, print(
    "status: %d error: %s" % (resp.status_code, resp.error if resp.error else resp.content))

print("list parts success")
print(resp.content)
