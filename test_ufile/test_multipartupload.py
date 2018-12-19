# -*- coding: utf-8 -*-

import unittest
import os
from ufile import multipartuploadufile
from ufile.compact import b
from ufile.logger import logger, set_log_file
from ufile.config import BLOCKSIZE, get_default
from ufile.compact import BytesIO
from common import *

set_log_file()
public_key = '<your public key>'                   #添加自己的账户公钥
private_key = '<your private key>'                 #添加自己的账户私钥
public_bucket = '<your public bucket name>'        #添加公共空间名称
private_bucket = '<your private bucket name>'      #添加私有空间名称

#自动生成随机txt文档,文件设置较大时随机数生成效率较低，也可自定义本地大文档测试
local_file =  './sharding.txt'
content = random_bytes(5*1024*1024)                #此处设置文件大小
with open(local_file, 'wb') as fileobj:
    fileobj.write(content)
sharding_file_key = 'sharding'                     

bio = BytesIO(u'Do be a good man'.encode('utf-8')) #待上传的stream
sharding_stream_key = 'sharding_stream'            

class MultipartUploadUFileTestCase(unittest.TestCase):
    multipartuploadufile_handler = multipartuploadufile.MultipartUploadUFile(public_key, private_key)

    def test_uploadfile(self):
        self.multipartuploadufile_handler.set_keys(public_key, private_key)

        # upload big file to public bucket
        logger.info('start sharding upload big file to public bucket')
        ret, resp = self.multipartuploadufile_handler.uploadfile(public_bucket, sharding_file_key, local_file)
        print(resp.error)
        assert resp.status_code == 200
        # upload big file to private bucket
        logger.info('start sharding upload big file to private bucket')
        ret, resp = self.multipartuploadufile_handler.uploadfile(private_bucket, sharding_file_key, local_file)
        print(resp.error)
        assert resp.status_code == 200

    def test_uploadstream(self):
        self.multipartuploadufile_handler.set_keys(public_key, private_key)

        # upload binary data stream to public bucket
        logger.info('start upload stream to public bucket')
        ret, resp = self.multipartuploadufile_handler.uploadstream(public_bucket, sharding_stream_key, bio)
        print(resp.error)
        assert resp.status_code == 200
        # upload binary data stream to private bucket
        logger.info('start upload stream to private bucket')
        bio.seek(0, os.SEEK_SET)
        ret, resp = self.multipartuploadufile_handler.uploadstream(private_bucket, sharding_stream_key, bio)
        print(resp.error)
        assert resp.status_code == 200

if __name__ == '__main__':
    unittest.main()
