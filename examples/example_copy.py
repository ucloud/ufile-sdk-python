public_key = ''                 #账户公钥
private_key = ''                #账户私钥
bucket = ''                     #空间名称
key = ''                        #目的文件在空间中的名称
srcbucket = ''                  #源文件所在空间名称
srckey = ''                     #源文件名称

from ufile import filemanager

copyufile_handler = filemanager.FileManager(public_key, private_key)

# 拷贝文件
ret, resp = copyufile_handler.copy(bucket, key, srcbucket, srckey)
assert resp.status_code == 200