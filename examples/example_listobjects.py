from ufile import filemanager

public_key = ''  # 账户公钥
private_key = ''  # 账户私钥

bucket = ''  # 空间名称

# 设置上传host后缀,外网可用后缀形如 .cn-bj.ufileos.com（cn-bj为北京地区，其他地区具体后缀可见控制台：对象存储-单地域空间管理-存储空间域名）
# 默认值为'.cn-bj.ufileos.com'，如果上传文件的bucket所在地域不在北京，请务必设置此项
upload_suffix = 'YOUR_UPLOAD_SUFFIX'
# 设置下载host后缀，普通下载后缀即上传后缀，CDN下载后缀为 .ufile.ucloud.com.cn
download_suffix = 'YOUR_DOWNLOAD_SUFFIX'

listobjects_hander = filemanager.FileManager(public_key, private_key, upload_suffix, download_suffix)

prefix = ''  # 以prefix作为前缀的目录文件列表
maxkeys = 100  # 指定返回目录文件列表的最大数量，默认值为100，不超过1000
marker = ''  # 返回以字母排序后，大于marker的目录文件列表
delimiter = '/'  # delimiter是目录分隔符，当前只支持"/"和""，当Delimiter设置为"/"且prefix以"/"结尾时，返回prefix目录下的子文件，当delimiter设置为""时，返回以prefix作为前缀的文件


# 普通使用(一次查询即可得到所有结果)
def once_list():
    ret, resp = listobjects_hander.listobjects(bucket, prefix=prefix, maxkeys=maxkeys, marker=marker,
                                               delimiter=delimiter)
    assert resp.status_code == 200

    for content in ret['Contents']:  # 子文件列表
        print(content)

    for common_prefix in ret['CommonPrefixes']:  # 子目录列表
        print(common_prefix)


# 因为一次查询返回数量存在最大限制，所以若一次查询无法获得所有结果，则根据返回值'NextMarker'循环遍历获得所有结果
def loop_list():
    global marker
    while True:
        ret, resp = listobjects_hander.listobjects(bucket, prefix=prefix, maxkeys=maxkeys, marker=marker,
                                                   delimiter=delimiter)
        assert resp.status_code == 200

        for content in ret['Contents']:  # 子文件列表
            print(content)

        for common_prefix in ret['CommonPrefixes']:  # 子目录列表
            print(common_prefix)
        marker = ret['NextMarker']
        if len(marker) <= 0 or maxkeys < len(ret['Contents']):
            break
