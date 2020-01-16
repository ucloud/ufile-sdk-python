## 工具用途：
ufile 文件上传下载工具, 支持 mysql 备份不落地流式上传 ufile
## 安装依赖：
1. python3 及以上版本
2. 安装python requests 库 

安装参考：https://github.com/ucloud/ufile-sdk-python


## 说明：
1. 支持put 小文件（10M以内）上传；
2. 支持mput 大文件（10M以上）上传；
3. 支持下载文件到本地；


## 使用方法：
1. 配置config.cfg， 把bucket 对应的公私钥，或者token 配置进去；
```
config.cfg:
{
        "public_key":"<$你的Bucket公钥>",
        "private_key":"<$你的Bucket私钥>"
}
```


2. 调用方法：
```
python ufile_op.py [upload_put|upload_mput|download] [domain] [key] [file]

NOTE:
    if file is "-", it means:
    - stdin for upload
    - stdout for download


例子：python ufile_op.py upload mybucket.cn-bj.ufileos.com s.php s.php
```

## 高级用法：
*支持标准输入作为输入源，可以用来做 mysql dump 的不落地备份到ufile*

例子：
```
备份本地文件到ufile:
python ufile_op.py upload_put testecho.cn-bj.ufileos.com s3.php  - < s2.php
python ufile_op.py upload_mput testecho.cn-bj.ufileos.com s3.php - < s2.php


备份mysql dump文件到ufile:
mysqldump -h 127.0.0.1 my_dbs my_table | python ufile_op.py upload_mput testecho.cn-bj.ufileos.com mysql_bak/20190507.sql -

下载mysql 备份文件到本地：
python ufile_op.py download testecho.cn-bj.ufileos.com mysql_bak/20190507.sql local_fname.sql
```
