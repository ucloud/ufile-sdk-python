from ufile import multipartuploadufile

public_key = ''  # 账户公钥
private_key = ''  # 账户私钥

bucket = ''  # 空间名称
sharding_key = ''  # 上传文件在空间中的名称
local_file = ''  # 本地文件名

# 设置上传host后缀,外网可用后缀形如 .cn-bj.ufileos.com（cn-bj为北京地区，其他地区具体后缀可见控制台：对象存储-单地域空间管理-存储空间域名）
# 默认值为'.cn-bj.ufileos.com'，如果上传文件的bucket所在地域不在北京，请务必设置此项
upload_suffix = 'YOUR_UPLOAD_SUFFIX'

multipartuploadufile_handler = multipartuploadufile.MultipartUploadUFile(public_key, private_key, upload_suffix)

# 分片上传一个全新的文件
ret, resp = multipartuploadufile_handler.uploadfile(bucket, sharding_key, local_file)
while True:
    if resp.status_code == 200:  # 分片上传成功
        break
    elif resp.status_code == -1:  # 网络连接问题，续传
        ret, resp = multipartuploadufile_handler.resumeuploadfile()
    else:  # 服务或者客户端错误
        print(resp.error)
        break

# 分片上传一个全新的二进制数据流
from io import BytesIO

bio = BytesIO(u'你好'.encode('utf-8'))
ret, resp = multipartuploadufile_handler.uploadstream(bucket, sharding_key, bio)
while True:
    if resp.status_code == 200:  # 分片上传成功
        break
    elif resp.status_code == -1:  # 网络连接问题，续传
        ret, resp = multipartuploadufile_handler.resumeuploadstream()
    else:  # 服务器或者客户端错误
        print(resp.error)
        break
