from ufile import filemanager

public_key = ''  # 账户公钥
private_key = ''  # 账户私钥

bucket = ''  # 空间名称
local_file = ''  # 本地文件名
put_key = ''  # 上传文件在空间中的名称
STANDARD = 'STANDARD'  # 标准文件类型
IA = 'IA'  # 低频文件类型

# 设置上传host后缀,外网可用后缀形如 .cn-bj.ufileos.com（cn-bj为北京地区，其他地区具体后缀可见控制台：对象存储-单地域空间管理-存储空间域名）
# 默认值为'.cn-bj.ufileos.com'，如果上传文件的bucket所在地域不在北京，请务必设置此项
upload_suffix = 'YOUR_UPLOAD_SUFFIX'
# 设置下载host后缀，普通下载后缀即上传后缀，CDN下载后缀为 .ufile.ucloud.com.cn
download_suffix = 'YOUR_DOWNLOAD_SUFFIX'

putufile_handler = filemanager.FileManager(public_key, private_key, upload_suffix, download_suffix)
classswitch_handler = filemanager.FileManager(public_key, private_key, upload_suffix, download_suffix)

# 普通上传文件至空间
header = dict()
header['X-Ufile-Storage-Class'] = STANDARD
ret, resp = putufile_handler.putfile(bucket, put_key, local_file, header=header)
assert resp.status_code == 200

# 标准文件类型转换为低频文件类型
ret, resp = classswitch_handler.class_switch_file(bucket, put_key, IA)
assert resp.status_code == 200
