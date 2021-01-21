public_key = ''                 #账户公钥
private_key = ''                #账户私钥

bucket = ''                     #空间名称

from ufile import filemanager

getfilelist_hander = filemanager.FileManager(public_key, private_key)

prefix='' #文件前缀
limit=10  #文件列表数目
marker='' #返回以字母排序后，大于marker的文件列表
ret, resp = getfilelist_hander.getfilelist(bucket, prefix=prefix, limit=limit, marker=marker)
assert resp.status_code == 200
for object in ret["DataSet"]:
    print(object)

# 根据返回值'NextMarker'循环遍历获得所有结果（若一次查询无法获得所有结果）
while True:
    ret, resp = getfilelist_hander.getfilelist(bucket, prefix=prefix, limit=limit, marker=marker)
    assert resp.status_code == 200

    for object in ret["DataSet"]:#
        print(object)

    marker = ret['NextMarker']
    if  len(marker) <= 0 or len(ret['DataSet']) < limit:
        break