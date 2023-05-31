from ufile import filemanager

public_key = ''  # 账户公钥
private_key = ''  # 账户私钥

bucket = ''  # 空间名称
key = ''  # 源文件在空间中的名称
newkey = ''  # 目的文件在空间中的名称
force = 'true'  # string类型, 是否强行覆盖文件，值为'true'会覆盖，其他值则不会,默认值为'true'

# 设置上传host后缀,外网可用后缀形如 .cn-bj.ufileos.com（cn-bj为北京地区，其他地区具体后缀可见控制台：对象存储-单地域空间管理-存储空间域名）
# 默认值为'.cn-bj.ufileos.com'，如果上传文件的bucket所在地域不在北京，请务必设置此项
upload_suffix = 'YOUR_UPLOAD_SUFFIX'
# 设置下载host后缀，普通下载后缀即上传后缀，CDN下载后缀为 .ufile.ucloud.com.cn
download_suffix = 'YOUR_DOWNLOAD_SUFFIX'

renameufile_handler = filemanager.FileManager(public_key, private_key, upload_suffix, download_suffix)

# 重命名文件
ret, resp = renameufile_handler.rename(bucket, key, newkey, force)
assert resp.status_code == 200
