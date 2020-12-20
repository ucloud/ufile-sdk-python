public_key = ''                 #账户公钥
private_key = ''                #账户私钥

bucket = ''                     #空间名称

from ufile import filemanager

listobjects_hander = filemanager.FileManager(public_key, private_key)

prefix=''     #以prefix作为前缀的目录文件列表
maxkeys=100   #指定返回目录文件列表的最大数量，默认值为100，不超过1000
marker=''     #返回以字母排序后，大于marker的目录文件列表
delimiter='/' #delimiter是目录分隔符，当前只支持"/"和""，当Delimiter设置为"/"且prefiex以"/"结尾时，返回prefix目录下的子文件，当delimiter设置为""时，返回以prefix作为前缀的文件

ret, resp = listobjects_hander.listobjects(bucket, prefix=prefix, maxkeys=maxkeys, marker=marker, delimiter=delimiter)
assert resp.status_code == 200

for object in ret['Contents']:#子文件列表
    print(object)

for object in ret['CommonPrefixes']:#子目录列表
    print(object)

# 根据返回值'NextMarker'循环遍历获得所有结果（若一次查询无法获得所有结果）
while True:
    ret, resp = listobjects_hander.listobjects(bucket, prefix=prefix, maxkeys=maxkeys, marker=marker, delimiter=delimiter)
    assert resp.status_code == 200

    for object in ret['Contents']:#子文件列表
        print(object)

    for object in ret['CommonPrefixes']:#子目录列表
        print(object)
    
    marker = ret['NextMarker']
    if  len(marker) <= 0 or maxkeys < len(ret['Contents']):
        break