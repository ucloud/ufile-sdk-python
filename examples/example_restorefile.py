from ufile import filemanager

public_key = ''  # 账户公钥
private_key = ''  # 账户私钥

bucket = ''  # 空间名称
local_file = ''  # 本地文件名
put_key = ''  # 上传文件在空间中的名称
ARCHIVE = 'ARCHIVE'  # 归档文件类型

# 设置上传host后缀,外网可用后缀形如 .cn-bj.ufileos.com（cn-bj为北京地区，其他地区具体后缀可见控制台：对象存储-单地域空间管理-存储空间域名）
# 默认值为'.cn-bj.ufileos.com'，如果上传文件的bucket所在地域不在北京，请务必设置此项
upload_suffix = 'YOUR_UPLOAD_SUFFIX'
# 设置下载host后缀，普通下载后缀即上传后缀，CDN下载后缀为 .ufile.ucloud.com.cn
download_suffix = 'YOUR_DOWNLOAD_SUFFIX'

putufile_handler = filemanager.FileManager(public_key, private_key, upload_suffix, download_suffix)
restorefile_handler = filemanager.FileManager(public_key, private_key, upload_suffix, download_suffix)

# 普通上传归档类型的文件至空间
header = dict()
header['X-Ufile-Storage-Class'] = ARCHIVE
ret, resp = putufile_handler.putfile(bucket, put_key, local_file, header=header)
assert resp.status_code == 200

# 解冻归档类型的文件
ret, resp = restorefile_handler.restore_file(bucket, put_key)
assert resp.status_code == 200

# 文件解冻一般在10s以内
time.sleep(10)

# 查看归档文件解冻状态
ret, resp = restorefile_handler.getfilelist(bucket, put_key)
assert resp.status_code == 200
print(ret['DataSet'][0]['RestoreStatus'])  # 'Frozen'说明解冻还未完成，'Restored'说明解冻成功
