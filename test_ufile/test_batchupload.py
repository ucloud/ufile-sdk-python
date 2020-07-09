# -*- coding: utf-8 -*-

import unittest
import os
from ufile import filemanager
from ufile.compact import b
from ufile.logger import logger, set_log_file
from ufile.config import BLOCKSIZE, get_default
from ufile.compact import BytesIO,b
import threading
import time

set_log_file()
public_key = ''              #添加自己的账户公钥
private_key = ''            #添加自己的账户私钥
bucket = ''   #添加公共空间名称
maxthreads = 30  #最大线程数

put_key_prefix = 'prefix_' #上传文件key

class BatchUploadUFileTestCase(unittest.TestCase):
    putufile_handler = filemanager.FileManager(public_key, private_key)

    def putfile_thread(self, sem, bucket, key, local_file, header=None):
        for i in range(1, 4):
            try:
                ret, resp = self.putufile_handler.putfile(bucket, key, local_file, header)
                if resp.status_code != 200:
                    logger.error('put file {0} failed. err: {1}, retry {2}'.format(key, resp, i))
                    continue
                else:
                    logger.info('put file {0} succeed.'.format(key))
                    break
            except Exception as e:
                    logger.error('put file {0} failed. exception: {1}'.format(key, e))
        sem.release()

    def test_batchupload(self):
        self.putufile_handler.set_keys(public_key, private_key)

        path = "/home/temp/"
        dirs = os.listdir(path)
        sem = threading.Semaphore(maxthreads)
        for root, dirs, files in os.walk(path):
            for file in files:
                sem.acquire()
                local_file = os.path.join(root, file)

                thread = threading.Thread(target=self.putfile_thread, args=(sem, bucket, put_key_prefix + local_file, local_file))
                thread.start()

        while threading.active_count() > 1:
            time.sleep(1)

if __name__ == '__main__':
    unittest.main()
