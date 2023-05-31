from ufile import config, filemanager

# 密钥可在https://console.ucloud.cn/uapi/apikey中获取
public_key = ''  # 账户公钥
private_key = ''  # 账户私钥

bucket = ''  # 空间名称
local_file = ''  # 本地文件名
put_key = ''  # 上传文件在空间中的名称
save_file = ''  # 下载文件保存的文件名

# 以下两项如果不设置，则默认设为'.cn-bj.ufileos.com'，如果上传、下载文件的bucket所在地域不在北京，请务必设置以下两项。
# 设置上传host后缀,外网可用后缀形如 .cn-bj.ufileos.com（cn-bj为北京地区，其他地区具体后缀可见控制台：对象存储-单地域空间管理-存储空间域名）
config.set_default(uploadsuffix='YOUR_UPLOAD_SUFFIX')
# 设置下载host后缀，普通下载后缀即上传后缀，CDN下载后缀为 .ufile.ucloud.com.cn
config.set_default(downloadsuffix='YOUR_DOWNLOAD_SUFFIX')

ufile_handler = filemanager.FileManager(public_key, private_key)

# 上传文件
ret, resp = ufile_handler.putfile(bucket, put_key, local_file, header=None)
assert resp.status_code == 200

# 下载文件
_, resp = ufile_handler.download_file(bucket, put_key, save_file)
assert resp.status_code == 200

# 遍历空间里文件(默认数目为20)
ret, resp = ufile_handler.getfilelist(bucket)
assert resp.status_code == 200
for object in ret["DataSet"]:
    print(object)

# 删除文件
ret, resp = ufile_handler.deletefile(bucket, put_key)
assert resp.status_code == 204
