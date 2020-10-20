# -*- coding: utf-8 -*-

import unittest
import os
from ufile import filemanager
from ufile.compact import b
from ufile.logger import logger, set_log_file
from ufile.config import BLOCKSIZE, get_default
from ufile.compact import BytesIO,b
from common import PUBLIC_BUCKET, PRIVATE_BUCKET, PUBLIC_KEY, PRIVATE_KEY

set_log_file()

small_local_file = './example.jpg'
put_small_key = 'put_small'
bio = BytesIO(u'Do be a good man'.encode('utf-8'))
put_stream_key = 'put_stream'

class PutUFileTestCase(unittest.TestCase):
    putufile_handler = filemanager.FileManager(PUBLIC_KEY, PRIVATE_KEY)

    def test_putufile(self):
        self.putufile_handler.set_keys(PUBLIC_KEY, PRIVATE_KEY)
        # put small file to public bucket
        logger.info('\nput small file to public bucket')
        ret, resp = self.putufile_handler.putfile(PUBLIC_BUCKET, put_small_key, small_local_file)
        assert resp.status_code == 200
        # put small file to private bucket
        logger.info('\nput small file to private bucket')
        ret, resp = self.putufile_handler.putfile(PRIVATE_BUCKET, put_small_key, small_local_file)
        assert resp.status_code == 200

    def test_putstream(self):
        self.putufile_handler.set_keys(PUBLIC_KEY, PRIVATE_KEY)
        logger.info('\nput stream to public bucket')
        ret, resp = self.putufile_handler.putstream(PUBLIC_BUCKET, put_stream_key, bio)
        assert resp.status_code == 200

        bio.seek(0, os.SEEK_SET)
        logger.info('\nput stream to private bucket')
        ret, resp = self.putufile_handler.putstream(PRIVATE_BUCKET, put_stream_key, bio)
        logger.info('response code:{0}'.format(resp.status_code))
        assert resp.status_code == 200

    def test_compareetag(self):
        result=self.putufile_handler.compare_file_etag(PUBLIC_BUCKET,put_small_key,small_local_file)
        if result==True:
            logger.info('\netag are the same!')
        else:
            logger.info('\netag are different!')

if __name__ == '__main__':
    unittest.main()
