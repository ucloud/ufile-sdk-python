from ufile import filemanager

public_key = ''  # 账户公钥
private_key = ''  # 账户私钥

bucket = ''  # 空间名称
local_file = ''  # 本地文件名
put_key = ''  # 上传文件在空间中的名称

# 设置上传host后缀,外网可用后缀形如 .cn-bj.ufileos.com（cn-bj为北京地区，其他地区具体后缀可见控制台：对象存储-单地域空间管理-存储空间域名）
# 默认值为'.cn-bj.ufileos.com'，如果上传文件的bucket所在地域不在北京，请务必设置此项
upload_suffix = 'YOUR_UPLOAD_SUFFIX'
# 设置下载host后缀，普通下载后缀即上传后缀，CDN下载后缀为 .ufile.ucloud.com.cn
download_suffix = 'YOUR_DOWNLOAD_SUFFIX'

putufile_handler = filemanager.FileManager(public_key, private_key, upload_suffix, download_suffix)

# 普通上传文件至空间
ret, resp = putufile_handler.putfile(bucket, put_key, local_file, header=None)
assert resp.status_code == 200

# 普通上传二进制数据流至空间
from io import BytesIO

bio = BytesIO(u'Do be a good man'.encode('utf-8'))  # 二进制数据流
stream_key = ''  # 上传数据流在空间中的名称
ret, resp = putufile_handler.putstream(bucket, stream_key, bio)
assert resp.status_code == 200

# 普通上传文件到所在region为上海二的空间
SH2_bucket = ''
SH2_UPLOAD_SUFFIX = '.cn-sh2.ufileos.com'

filemgr_sh = filemanager.FileManager(public_key, private_key, upload_suffix=SH2_UPLOAD_SUFFIX)
ret, resp = filemgr_sh.putfile(SH2_bucket, put_key, local_file, header=None)
assert resp.status_code == 200
