# -*- coding: utf-8 -*-

import unittest
from ufile import filemanager
from ufile.logger import logger, set_log_file
from ufile.config import BLOCKSIZE, get_default
from common import *

set_log_file()
public_key = PUBLIC_KEY             #添加自己的账户公钥
private_key = PRIVATE_KEY           #添加自己的账户私钥
public_bucket = PUBLIC_BUCKET  #添加公共空间名称
key = '<your new key>'                       #目标文件名称
srcbucket = '<source bucket>'                #源文件所在空间
srckey = '<source key>'                      #源文件名称

class CopyUFileTestCase(unittest.TestCase):
    copyufile_handler = filemanager.FileManager(public_key, private_key)

    def test_copyfile(self):
        self.copyufile_handler.set_keys(public_key, private_key)
        logger.info('start copy file')
        ret, resp = self.copyufile_handler.copy(public_bucket, key, srcbucket, srckey)
        assert resp.status_code == 200

if __name__ == '__main__':
    unittest.main()
