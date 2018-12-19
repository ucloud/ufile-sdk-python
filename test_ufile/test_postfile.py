# -*- coding: utf-8 -*-

import unittest
import os
from ufile import filemanager
from ufile.compact import b
from ufile.logger import logger, set_log_file
from ufile.config import BLOCKSIZE, get_default
from ufile.compact import BytesIO

set_log_file()
public_key = '<your public key>'                   #添加自己的账户公钥
private_key = '<your private key>'                 #添加自己的账户私钥
public_bucket = '<your public bucket name>'        #添加公共空间名称
private_bucket = '<your private bucket name>'      #添加私有空间名称

small_local_file = './example.jpg'         
post_small_key = 'post_small'            
bio = BytesIO(u'Do be a good man'.encode('utf-8')) 
post_stream_key = 'post_stream'    

class PostUFileTestCase(unittest.TestCase):
    postfile_handler = filemanager.FileManager(public_key, private_key)

    def test_postufile(self):
        self.postfile_handler.set_keys(public_key, private_key)
        # post small file to public bucket
        logger.info('\nstart post small file to public bucket')
        ret, resp = self.postfile_handler.postfile(public_bucket, post_small_key, small_local_file)
        assert resp.status_code == 200
        # post small file to private bucket
        logger.info('\nstart post small file to private bucket')
        ret, resp = self.postfile_handler.postfile(private_bucket, post_small_key, small_local_file)
        assert resp.status_code == 200

if __name__ == '__main__':
    unittest.main()
