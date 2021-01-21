public_key = ''                 #账户公钥
private_key = ''                #账户私钥

bucket = ''                     #空间名称
key = ''                        #源文件在空间中的名称
newkey = ''                     #目的文件在空间中的名称
force = 'true'                  #string类型, 是否强行覆盖文件，值为'true'会覆盖，其他值则不会,默认值为'true'

from ufile import filemanager

renameufile_handler = filemanager.FileManager(public_key, private_key)

# 重命名文件
ret, resp = renameufile_handler.rename(bucket, key, newkey, force)
assert resp.status_code == 200