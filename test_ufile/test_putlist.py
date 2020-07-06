# -*- coding: utf-8 -*-

import unittest
import os
from ufile import filemanager
from ufile.compact import b
from ufile.logger import logger, set_log_file
from ufile.config import BLOCKSIZE, get_default
from ufile.compact import BytesIO,b

set_log_file()
public_key = '<your public key>'              #添加自己的账户公钥
private_key = '<your private key>'            #添加自己的账户私钥
bucket = '<your public bucket name>'   #添加公共空间名称
maxthreads = 5  #最大线程数

local_file_list = ['test1', 'test2', 'test3'] #本地待上传文件列表
put_key_prefix = 'prefix_' #上传文件key

class PutListTestCase(unittest.TestCase):
    putufile_handler = filemanager.FileManager(public_key, private_key)

    def test_putlist(self):
        self.putufile_handler.set_keys(public_key, private_key)
        # put small file to bucket
        logger.info('\nput small file to bucket')

        sem = threading.Semaphore(maxthreads)
        for local_file in local_file_list:
            thread = threading.Thread(target=self.putufile_handler.putfile_thread, args=(sem, bucket, put_key_prefix + local_file, local_file))
            thread.start()

if __name__ == '__main__':
    unittest.main()
