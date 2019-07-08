# -*- coding: utf-8 -*-

import unittest
import os
from ufile import filemanager, multipartuploadufile
from ufile.compact import b
from ufile.logger import logger, set_log_file
from ufile.config import BLOCKSIZE, get_default
from ufile.compact import BytesIO,b
from common import *

set_log_file()
public_key = '<your public key>'              #添加自己的账户公钥
private_key = '<your private key>'            #添加自己的账户私钥
public_bucket = '<your public bucket name>'   #添加公共空间名称
private_bucket = '<your private bucket name>' #添加私有空间名称
STANDARD = 'STANDARD'
IA = 'IA'
ARCHIVE = 'ARCHIVE'

#自动生成随机txt文档,文件设置较大时随机数生成效率较低，也可自定义本地大文档测试
big_local_file =  './sharding.txt'
content = random_bytes(5*1024*1024)                #此处设置文件大小
with open(big_local_file, 'wb') as fileobj:
    fileobj.write(content)

small_local_file = './example.jpg'
post_standard_key = 'post_st_small'
put_ia_key = 'put_ia_small'
mput_archive_key = 'mput_ar_big'


class ArchiveOperateTestCase(unittest.TestCase):
    """
        目前支持三种存储类型：STANDARD(标准)、IA(低频)、ARCHIVE(冷存)
        上传时需要携带 X-Ufile-Storage-Class http请求头指定上传文件的存储类型
    """

    putufile_handler = filemanager.FileManager(public_key, private_key)
    multipartuploadufile_handler = multipartuploadufile.MultipartUploadUFile(public_key, private_key)
    postfile_handler = filemanager.FileManager(public_key, private_key)
    restorefile_handler = filemanager.FileManager(public_key, private_key)
    classswitch_handler = filemanager.FileManager(public_key, private_key)

    def test_upload_ia_ufile(self):
        #使用put方式上传低频文件
        self.putufile_handler.set_keys(public_key, private_key)
        #设置header
        header = dict()
        header['X-Ufile-Storage-Class'] = IA

        # upload file to public bucket
        logger.info('\nstart put small file to public bucket')
        ret, resp = self.putufile_handler.putfile(public_bucket, put_ia_key, small_local_file, header)
        assert resp.status_code == 200
        # put small file to private bucket
        logger.info('\nstart put small file to private bucket')
        ret, resp = self.putufile_handler.putfile(private_bucket, put_ia_key, small_local_file, header)
        assert resp.status_code == 200

    def test_upload_archive_ufile(self):
        #使用分片上传方式上传冷存文件
        self.multipartuploadufile_handler.set_keys(public_key, private_key)
        #设置header
        header = dict()
        header['X-Ufile-Storage-Class'] = ARCHIVE

        # upload big file to public bucket
        logger.info('start sharding upload big file to public bucket')
        ret, resp = self.multipartuploadufile_handler.uploadfile(public_bucket, mput_archive_key, big_local_file, header=header)
        print(resp.error)
        assert resp.status_code == 200
        # upload big file to private bucket
        logger.info('start sharding upload big file to private bucket')
        ret, resp = self.multipartuploadufile_handler.uploadfile(private_bucket, mput_archive_key, big_local_file, header=header)
        print(resp.error)
        assert resp.status_code == 200

    def test_upload_standard_ufile(self):
        #使用post方式上传标准文件
        self.postfile_handler.set_keys(public_key, private_key)
        #设置header
        header = dict()
        header['X-Ufile-Storage-Class'] = STANDARD

        # post small file to public bucket
        logger.info('\nstart post small file to public bucket')
        ret, resp = self.postfile_handler.postfile(public_bucket, post_standard_key, small_local_file, header)
        assert resp.status_code == 200
        # post small file to private bucket
        logger.info('\nstart post small file to private bucket')
        ret, resp = self.postfile_handler.postfile(private_bucket, post_standard_key, small_local_file, header)
        assert resp.status_code == 200

    def test_restore_file(self):
        #解冻冷存文件
        self.restorefile_handler.set_keys(public_key, private_key)
        # restore archive file in public bucket
        logger.info('start restore archive file to public bucket')
        ret, resp = self.restorefile_handler.restore_file(public_bucket, mput_archive_key)
        print(resp.error)
        assert resp.status_code == 200

    def test_classswitch_file(self):
        #转换文件存储类型
        self.classswitch_handler.set_keys(public_key, private_key)
        # file storage class switch to IA in private bucket
        logger.info('start switch file storage class in private bucket')
        ret, resp = self.classswitch_handler.class_switch_file(private_bucket, post_standard_key, IA)
        print(resp.error)
        assert resp.status_code == 200

if __name__ == '__main__':
    unittest.main()
