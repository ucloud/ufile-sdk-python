# -*- coding: utf-8 -*-

"""
test bucket
"""

from ufile import bucketmanager

public_key = '<your public key>'              #添加自己的账户公钥(UCloud账户的API密钥公钥,此密钥权限较高，仅bucket操作使用)
private_key = '<your private key>'            #添加自己的账户私钥(UCloud账户的API密钥私钥,此密钥权限较高，仅bucket操作使用)
public_bucket = '<your public bucket name>'   #添加公共空间名称
private_bucket = '<your private bucket name>' #添加私有空间名称
region = '<your region>'                      #添加bucket所在的地理区域

# create public bucket
bucketmanager = bucketmanager.BucketManager(public_key, private_key)
ret, resp = bucketmanager.createbucket(public_bucket, region,'public')
print(ret)
# create private bucket
ret, resp = bucketmanager.createbucket(private_bucket, region,'private')
print(ret)
# delete public bucket
ret, resp = bucketmanager.deletebucket(public_bucket)
print(ret)
# delete private bucket
ret, resp = bucketmanager.deletebucket(private_bucket)
print(ret)
# describle public bucket
ret, resp = bucketmanager.describebucket(public_bucket)
print(ret)
# describe private bucket
ret, resp = bucketmanager.describebucket(private_bucket)
print(ret)
# get a list of files from a bucket
ret, resp = bucketmanager.getfilelist(public_bucket)
print(ret)
