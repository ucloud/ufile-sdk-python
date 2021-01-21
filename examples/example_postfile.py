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