# -*- coding: utf-8 -*-

import unittest
import os
from ufile import filemanager
from ufile.compact import b
from ufile.logger import logger, set_log_file
from ufile.config import BLOCKSIZE, get_default
from ufile.compact import BytesIO

set_log_file()
public_key = '<your public key>'             #添加自己的账户公钥
private_key = '<your private key>'           #添加自己的账户私钥
public_bucket = '<your public bucket name>'  #添加公共空间名称
existfile = '<your local file>'              #添加本地文件(空间已存在)
nonexistfile = '<your local file>'           #添加本地文件(空间不存在)

existkey = 'instead'  
nonexistkey = 'instead_non'  


class UploadHitUFileTestCase(unittest.TestCase):
    uploadhitufile_handler = filemanager.FileManager(public_key, private_key)

    def test_uploadhitexistfile(self):
        self.uploadhitufile_handler.set_keys(public_key, private_key)
        logger.info('start uploadhit existfile')
        ret, resp = self.uploadhitufile_handler.uploadhit(public_bucket, existkey, existfile)
        assert resp.status_code == 200

    def test_uploadhitnonexistfile(self):
        self.uploadhitufile_handler.set_keys(public_key, private_key)
        logger.info('start uploadhit existfile')
        ret, resp = self.uploadhitufile_handler.uploadhit(public_bucket, nonexistkey, nonexistfile)
        assert resp.status_code == 404

if __name__ == '__main__':
    unittest.main()
