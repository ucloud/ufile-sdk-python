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