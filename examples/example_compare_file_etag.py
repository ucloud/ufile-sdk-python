from ufile import filemanager

public_key = ''                 #账户公钥
private_key = ''                #账户私钥

bucket = ''                     #添加空间名称
put_key = ''                    #添加远程文件key
local_file=''                   #添加本地文件路径

compare_handler = filemanager.FileManager(public_key, private_key)
result=compare_handler.compare_file_etag(bucket,put_key,local_file)
if result==True:
    print('etag are the same!')
else:
    print('etag are different!')