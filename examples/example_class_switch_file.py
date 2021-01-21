public_key = ''                 #账户公钥
private_key = ''                #账户私钥

bucket = ''                     #空间名称
local_file = ''                 #本地文件名
put_key = ''                    #上传文件在空间中的名称
STANDARD = 'STANDARD'           #标准文件类型
IA = 'IA'                       #低频文件类型

from ufile import filemanager

putufile_handler = filemanager.FileManager(public_key, private_key)
classswitch_handler = filemanager.FileManager(public_key, private_key)

# 普通上传文件至空间
header = dict()
header['X-Ufile-Storage-Class'] = STANDARD
ret, resp = putufile_handler.putfile(bucket, put_key, local_file, header=header)
assert resp.status_code == 200

# 标准文件类型转换为低频文件类型
ret, resp = classswitch_handler.class_switch_file(bucket, put_key, IA)
assert resp.status_code == 200