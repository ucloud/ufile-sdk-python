public_key = ''                 #账户公钥
private_key = ''                #账户私钥

bucket = ''                     #空间名称
delete_key = ''                 #文件在空间中的名称

from ufile import filemanager

deleteufile_handler = filemanager.FileManager(public_key, private_key)

# 删除空间的文件
ret, resp = deleteufile_handler.deletefile(bucket, delete_key)
assert resp.status_code == 204