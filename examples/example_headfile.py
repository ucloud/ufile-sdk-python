public_key = ''                 #账户公钥
private_key = ''                #账户私钥

bucket = ''                     #空间名称
head_key = ''                   #文件在空间中的名称

from ufile import filemanager

headfile_handler = filemanager.FileManager(public_key, private_key)

# 查询文件基本信息
ret, resp = headfile_handler.head_file(bucket, head_key)
assert resp.status_code == 200
print(resp)