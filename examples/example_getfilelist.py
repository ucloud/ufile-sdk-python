from ufile import filemanager

public_key = ''  # 账户公钥
private_key = ''  # 账户私钥

bucket = ''  # 空间名称

# 设置上传host后缀,外网可用后缀形如 .cn-bj.ufileos.com（cn-bj为北京地区，其他地区具体后缀可见控制台：对象存储-单地域空间管理-存储空间域名）
# 默认值为'.cn-bj.ufileos.com'，如果上传文件的bucket所在地域不在北京，请务必设置此项
upload_suffix = 'YOUR_UPLOAD_SUFFIX'
# 设置下载host后缀，普通下载后缀即上传后缀，CDN下载后缀为 .ufile.ucloud.com.cn
download_suffix = 'YOUR_DOWNLOAD_SUFFIX'

getfilelist_hander = filemanager.FileManager(public_key, private_key, upload_suffix, download_suffix)

prefix = ''  # 文件前缀
limit = 10  # 文件列表数目
marker = ''  # 返回以字母排序后，大于marker的文件列表
ret, resp = getfilelist_hander.getfilelist(bucket, prefix=prefix, limit=limit, marker=marker)
assert resp.status_code == 200
for object in ret["DataSet"]:
    print(object)

# 根据返回值'NextMarker'循环遍历获得所有结果（若一次查询无法获得所有结果）
while True:
    ret, resp = getfilelist_hander.getfilelist(bucket, prefix=prefix, limit=limit, marker=marker)
    assert resp.status_code == 200

    for object in ret["DataSet"]:  #
        print(object)

    marker = ret['NextMarker']
    if len(marker) <= 0 or len(ret['DataSet']) < limit:
        break
