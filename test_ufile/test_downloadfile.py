# -*- coding: utf-8 -*-

import unittest
from ufile import filemanager
from ufile.logger import logger, set_log_file
from ufile.config import BLOCKSIZE, get_default

public_key = '<your public key>'                 #添加自己的账户公钥
private_key = '<your private key>'               #添加自己的账户私钥
public_bucket = '<your public bucket name>'      #添加公共空间名称
private_bucket = '<your private bucket name>'    #添加私有空间名称

put_key = 'put_small'                           
put_range_key = 'put_stream'                     
public_download = 'public_download'        
public_range_download = 'public_range_download'  
private_download = 'private_download'       
private_range_download = 'private_range_download' 

set_log_file()


class DownloadUFileTestCase(unittest.TestCase):
    downloadufile_handler = filemanager.FileManager(public_key, private_key)

    def test_downloadpublic(self):
        self.downloadufile_handler.set_keys(public_key, private_key)
        # download the small file
        logger.info('\nstart download small file from public bucket')
        ret, resp = self.downloadufile_handler.download_file(public_bucket, put_key, public_download, isprivate=False)
        assert resp.status_code == 200

    def test_downloadprivate(self):
        self.downloadufile_handler.set_keys(public_key, private_key)
        # download the small file
        logger.info('start download small file from private bucket')
        ret, resp = self.downloadufile_handler.download_file(private_bucket, put_key, private_download)
        assert resp.status_code == 200

    def test_downloadwithrange(self):
        self.downloadufile_handler.set_keys(public_key, private_key)
        logger.info('start download with range condition from public bucket')
        ret, resp = self.downloadufile_handler.download_file(public_bucket, put_range_key, public_range_download, isprivate=False, expires=get_default('expires'), content_range=(0, 15), header=None)
        assert resp.status_code == 206
        logger.info('start download with range condition from private bucket')
        ret, resp = self.downloadufile_handler.download_file(private_bucket, put_range_key, private_range_download, isprivate=True, expires=get_default('expires'), content_range=(0, 15), header=None)
        assert resp.status_code == 206

if __name__ == '__main__':
    unittest.main()
