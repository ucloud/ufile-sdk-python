# -*- coding: utf-8 -*-

import unittest
from ufile import filemanager
from ufile.logger import logger, set_log_file
from ufile.config import BLOCKSIZE, get_default
from common import *

set_log_file()
public_key = PUBLIC_KEY              #添加自己的账户公钥
private_key = PRIVATE_KEY              #添加自己的账户私钥
public_bucket = PUBLIC_BUCKET   #添加公共空间名称
private_bucket = PRIVATE_BUCKET #添加私有空间名称
delete_key = '<delete_key>'              #添加delete_key，必须存在于空间中，否则返回404错误

class DeleteUFileTestCase(unittest.TestCase):
    deleteufile_handler = filemanager.FileManager(public_key, private_key)

    def test_deleteufile(self):
        self.deleteufile_handler.set_keys(public_key, private_key)
        # delete file from public bucket
        logger.info('\ndelete file from public bucket')
        ret, resp = self.deleteufile_handler.deletefile(public_bucket, delete_key)
        logger.info(resp.error)
        logger.info(resp.status_code)
        #assert resp.status_code == 204
        # delete file from private bucket
        logger.info('\ndelete file from private bucket')
        ret, resp = self.deleteufile_handler.deletefile(private_bucket, delete_key)
        logger.info(resp.error)
        logger.info(resp.status_code)
        #assert resp.status_code == 204

if __name__ == '__main__':
    unittest.main()
