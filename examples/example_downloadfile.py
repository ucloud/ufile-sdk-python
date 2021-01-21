public_key = ''                 #账户公钥
private_key = ''                #账户私钥

public_bucket = ''              #公共空间名称
private_bucket = ''             #私有空间名称
public_savefile = ''            #保存文件名
private_savefile = ''           #保存文件名
range_savefile = ''             #保存文件名
put_key = ''                    #文件在空间中的名称
stream_key = ''                 #文件在空间中的名称

from ufile import filemanager

downloadufile_handler = filemanager.FileManager(public_key, private_key)

# 从公共空间下载文件
ret, resp = downloadufile_handler.download_file(public_bucket, put_key, public_savefile, isprivate=False)
assert resp.status_code == 200

# 从私有空间下载文件
ret, resp = downloadufile_handler.download_file(private_bucket, put_key, private_savefile)
assert resp.status_code == 200

# 下载包含文件范围请求的文件
ret, resp = downloadufile_handler.download_file(public_bucket, put_key, range_savefile, isprivate=False, expires=300, content_range=(0, 15))
assert resp.status_code == 206

# 从所在region为上海二的私有空间下载文件
SH2_bucket = ''
SH2_put_key = ''                         
SH2_private_savefile = ''
SH2_DOWNLOAD_SUFFIX = '.cn-sh2.ufileos.com'

filemgr_sh = filemanager.FileManager(public_key, private_key, download_suffix=SH2_DOWNLOAD_SUFFIX )
ret, resp = filemgr_sh.download_file(SH2_bucket, SH2_put_key, SH2_private_savefile)
assert resp.status_code == 200