# -*- coding: utf-8

import unittest
from ufile import filemanager
from ufile.logger import logger, set_log_file
from ufile.config import get_default
  
public_key = '<your public key>'    #添加自己的账户公钥
private_key = '<your private key>'  #添加自己的账户私钥
bucket = '<your bucket name>'       #添加自己的空间名称

class ListObjectsTestCase(unittest.TestCase):
    listobjects_hander = filemanager.FileManager(public_key, private_key)

    def test_listobjects(self):
        self.listobjects_hander.set_keys(public_key, private_key)
        prefix = ''
        marker = ''
        maxkeys = 100
        ret, resp = self.listobjects_hander.listobjects(bucket, prefix=prefix, maxkeys=maxkeys, marker=marker, delimiter='/')
        assert resp.status_code == 200
        logger.info('Contents:')
        for item in ret['Contents']:
            key = item['Key'].encode('utf-8')
            logger.info('key: {0}'.format(key))
        logger.info('CommonPrefixes: ')
        for item in ret['CommonPrefixes']:
            pre = item['Prefix'].encode('utf-8')
            logger.info('prefix: {0}'.format(pre))
        nextMarker = ret['NextMarker']
        logger.info('NextMarker is {0}'.format(nextMarker))

if __name__ == '__main__':
    unittest.main()
