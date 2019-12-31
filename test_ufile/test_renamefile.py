# -*- coding: utf-8 -*-

import unittest
from ufile import filemanager
from ufile.logger import logger, set_log_file
from ufile.config import BLOCKSIZE, get_default

set_log_file()
public_key = '<your public key>'             #添加自己的账户公钥
private_key = '<your private key>'           #添加自己的账户私钥
public_bucket = '<your public bucket name>'  #添加公共空间名称
newkey = '<your new key>'                    #目标文件名称
key = '<your source key>'                    #源文件名称


class RenameUFileTestCase(unittest.TestCase):
    renameufile_handler = filemanager.FileManager(public_key, private_key)

    def test_renamefile(self):
        self.renameufile_handler.set_keys(public_key, private_key)
        logger.info('start rename file')
        ret, resp = self.renameufile_handler.rename(public_bucket, key, newkey, 'true')
        assert resp.status_code == 200

if __name__ == '__main__':
    unittest.main()
