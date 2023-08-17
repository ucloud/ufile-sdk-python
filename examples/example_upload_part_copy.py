# !/usr/bin/env python
# -*- encoding: utf-8 -*-
from ufile import multipartuploadufile, filemanager

public_key = ''  # 账户公钥
private_key = ''  # 账户私钥

source_bucket = ''  # 空间名称
source_key = ''  # 源文件
dest_bucket = ''  # 空间名称
dest_key = ''  # 目的文件名
mime_type = ''  # 上传数据的MIME类型

# 设置上传host后缀,外网可用后缀形如 .cn-bj.ufileos.com（cn-bj为北京地区，其他地区具体后缀可见控制台：对象存储-单地域空间管理-存储空间域名）
# 默认值为'.cn-bj.ufileos.com'，如果上传文件的bucket所在地域不在北京，请务必设置此项
upload_suffix = '.cn-bj.ufileos.com'

# 获取源文件信息
file_manager = filemanager.FileManager(public_key, private_key, upload_suffix=upload_suffix,
                                       download_suffix=upload_suffix)
rest, resp = file_manager.head_file(source_bucket, source_key)
assert resp.status_code == 200, print("status: %d error: %s" % (resp.status_code, resp.content))

# 获取源文件etag和size
etag = resp.etag
file_size = int(resp.content_length)

multi_part_upload_ufile_handler = multipartuploadufile.MultipartUploadUFile(public_key, private_key, upload_suffix)

# 初始化分片上传
ret, resp = multi_part_upload_ufile_handler.init_multipart_upload(dest_bucket, dest_key, upload_suffix=upload_suffix)
assert resp.status_code == 200

block_size = ret.get("BlkSize")  # 分片大小
part_number = 0
offset = 0

# 上传分片
while offset < file_size:
    end_size = offset + block_size if offset + block_size < file_size else file_size
    ret, resp = multi_part_upload_ufile_handler.upload_part_copy(source_bucket, source_key, mime_type, offset, end_size,
                                                                 part_number, upload_suffix)
    assert resp.status_code == 200, print("status: %d error: %s" % (resp.status_code, resp.error))
    offset += block_size
    part_number += 1

# 完成分片上传
ret, resp = multi_part_upload_ufile_handler.finish_upload()
assert resp.status_code == 200, print("status: %d error: %s" % (resp.status_code, resp.content))

# 对比etag
assert etag == resp.etag, print("etag不一致")

print("upload part copy success")