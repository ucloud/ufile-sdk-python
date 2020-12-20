public_key = ''         #账户公钥
private_key = ''        #账户私钥

from ufile import bucketmanager

bucketmanager_handler = bucketmanager.BucketManager(public_key, private_key)

# 创建新的bucket
bucketname = '' #创建的空间名称,命名规范参见https://docs.ucloud.cn/api/ufile-api/create_bucket
region = 'cn-bj'#空间所在的地理区域，详细信息见https://docs.ucloud.cn/ufile/introduction/region
ret, resp = bucketmanager_handler.createbucket(bucketname, region,'public')
print(ret)

# 删除bucket
bucketname = '' #待删除的空间名称
ret, resp = bucketmanager_handler.deletebucket(bucketname)
print(ret)

# 获取bucket信息
bucketname = '' # 待查询的空间名称
ret, resp = bucketmanager_handler.describebucket(bucketname)
print(ret)

# 更改bucket属性
bucketname = '' # 待更改的私有空间名称
ret, resp = bucketmanager_handler.updatebucket(bucketname, 'public')
print(ret)