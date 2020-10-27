# -*- coding: utf-8 -*-


import os
import json
from .baseufile import BaseUFile
from .util import _check_dict, initialsharding_url, finishsharding_url, shardingupload_url, _file_iter, mimetype_from_file, mimetype_from_buffer
from .httprequest import ResponseInfo, _initialsharding, _finishsharding, _shardingupload
from .logger import logger
from .compact import s
from . import config
import time
import threading


class MultipartUploadUFile(BaseUFile):
    """
    分片上传UFile类

    Attributes:
    uploadid: string类型，初始化分片上传请求获得的uploadid
    etaglist: list 类型，已经成功上传分片的etag列表
    blocksize: integer类型，分片大小
    pausepartnumber: 第一个上传失败的分片编号（编号从0开始）
    """

    def __init__(self, public_key, private_key, upload_suffix=None):
        """
        初始化 MultipartUploadUFile 实例

        :param public_key: string类型, 账户API公私钥中的公钥
        :param private_key: string类型, 账户API公私钥中的私钥
        :param upload_suffix: string类型, 如果传入此参数, 则会忽略 config 中配置的 upload_suffix 字段
        :return: None，如果为非法的公私钥，则抛出ValueError异常
        """
        super(MultipartUploadUFile, self).__init__(public_key, private_key)
        self.uploadid = None
        self.blocksize = None
        self.etaglist = []
        self.__key = None
        self.__bucket = None
        self.__header = None
        self.__datastream = None
        self.__mimetype = None
        self.__upload_suffix = upload_suffix
        self.pausepartnumber = 0

    def uploadstream(self, bucket, key, stream, maxthread=4, retrycount=3, retryinterval=5, mime_type=None, header=None):
        """
        分片上传二进制数据流到UFile空间

        :param bucket: 空间名称
        :param key: 上传数据在空间中的名称
        :param stream: file-like 对象或者二进制数据流
        :param maxthread: 限制的最大线程数
        :param mime_type: 上传数据的MIME类型
        :param retrycount: integer 类型，分片重传次数
        :param retryinterval: integer 类型，同个分片失败重传间隔，单位秒
        :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        :return: ret: 如果http状态码为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
        :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
        """
        self.__bucket = bucket
        self.__key = key
        self.etaglist = []
        self.uploadid = None
        self.blocksize = None
        self.__header = header
        self.__stream = stream
        self.pausepartnumber = 0
        if self.__header is None:
            self.__header = dict()
        else:
            _check_dict(self.__header)
        if 'User-Agent' not in self.__header:
            self.__header['User-Agent'] = config.get_default('user_agent')

        # initial sharding request
        ret, resp = self.__initialsharding()
        if resp.ok():
            self.uploadid = ret.get('UploadId')
            self.blocksize = ret.get('BlkSize')
            logger.info('multipart upload id: {0}'.format(self.uploadid))
        else:
            logger.error('multipar upload init failed. error message: {0}'.format(resp.error))
            return ret, resp

        # mulitple sharding upload
        if mime_type is None:
            if hasattr(self.__stream, 'seek') and hasattr(self.__stream, 'read'):
                self.__mimetype = s(mimetype_from_buffer(self.__stream.read(1024)))
                self.__stream.seek(0, os.SEEK_SET)
            else:
                self.__mimetype = 'application/octec-stream'
        else:
            self.__mimetype = mime_type

        self.__header['Content-Type'] = self.__mimetype
        authorization = self.authorization('put', self.__bucket, self.__key, self.__header)
        self.__header['Authorization'] = authorization

        sem=threading.Semaphore(maxthread)
        for data in _file_iter(self.__stream, self.blocksize):
            self.etaglist.append("")
            thread1 = threading.Thread(target=self.__partthread, args=(sem, self.__bucket, self.__key, self.uploadid, self.pausepartnumber, self.__header, data, retrycount, retryinterval, self.etaglist, self.__upload_suffix))
            thread1.start()
            thread1.join()
            self.pausepartnumber += 1

        while threading.active_count()>1:
            time.sleep(5)

        logger.info('start finish sharding request.')
        ret, resp = self.__finishupload()
        if not resp.ok():
            logger.error('multipart upload failed. uploadid:{0}, pausepartnumber: {1}, key: {2} FAIL!!!'.format(self.uploadid, self.pausepartnumber, self.__key))
        else:
            logger.info('mulitpart upload succeed. uploadid: {0}, key: {1} SUCCEED'.format(self.uploadid, self.__key))
        return ret, resp

    def uploadfile(self, bucket, key, localfile, maxthread=4, retrycount=3, retryinterval=5, header=None):
        """
        分片上传本地文件到空间

        :param bucket: string类型，空间名称
        :param key: string类型，文件在空间中的名称
        :param localfile: string 类型，本地文件名称
        :param maxthread: 限制的最大线程数
        :param retrycount: integer 类型，分片重传次数
        :param retryinterval: integer 类型，同个分片失败重传间隔，单位秒
        :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        :return: ret: 如果http状态码为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
        :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
        """
        self.__localfile = localfile
        mime_type = s(mimetype_from_file(self.__localfile))
        with open(localfile, 'rb') as fd:
            return self.uploadstream(bucket, key, fd, maxthread, retrycount, retryinterval, mime_type, header)


    def __initialsharding(self):
        """
        初始化分片请求

        :return: ret: 如果http状态码为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
        :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
        """
        if self.__header is None:
            self.__header = {}
        else:
            _check_dict(self.__header)
        if 'User-Agent' not in self.__header:
            self.__header['User-Agent'] = config.get_default('user_agent')

        self.__header['Content-Length'] = str(0)
        self.__header['Content-Type'] = 'text/plain'
        authorization = self.authorization('post', self.__bucket, self.__key, self.__header)
        self.__header['Authorization'] = authorization

        url = initialsharding_url(self.__bucket, self.__key, upload_suffix=self.__upload_suffix)

        logger.info('start initialize sharding')
        logger.info('initial sharding url: {0}'.format(url))

        return _initialsharding(url, self.__header)

    def __finishupload(self):
        """
        完成分片上传的请求

        :return: ret: 如果http状态码为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
        :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
        """
        if self.__header is None:
            self.__header = dict()
        else:
            _check_dict(self.__header)
        if 'User-Agent' not in self.__header:
            self.__header['User-Agent'] = config.get_default('user_agent')

        self.__header['Content-Type'] = 'text/plain'
        logger.info(self.etaglist)
        data = ','.join(self.etaglist)
        logger.info(data)
        self.__header['Content-Length'] = str(len(data))

        authorization = self.authorization('post', self.__bucket, self.__key, self.__header)
        self.__header['Authorization'] = authorization
        logger.info(json.dumps(self.__header, indent=4))
        params = {'uploadId': self.uploadid}

        url = finishsharding_url(self.__bucket, self.__key, upload_suffix=self.__upload_suffix)

        logger.info('start finish sharding request')
        return _finishsharding(url, params, self.__header, data)

    def resumeuploadfile(self, retrycount=3, retryinterval=5, bucket=None, key=None, uploadid=None, blocksize=None, etaglist=None, localfile=None, pausepartnumber=None, mime_type=None, header=None):
        """
        断点续传失败的本地文件分片
        可以在调用uploadfile失败后重新续传，也可以通过传递所有需要的参数续传

        :param retrycount: integer 类型，分片重传次数
        :param retryinterval: integer 类型，同个分片失败重传间隔，单位秒
        :param bucket: string类型, 空间名称
        :param key: string类型，文件或数据在空间中的名称
        :param uploadid: string类型，初始化分片获得的uploadid
        :param blocksize: integer类型，分片大小
        :param etaglist: list类型，元素为已经上传成功的分片的etag
        :param pausepartnumber: integer类型，第一个失败分片的编号（编号从0开始）
        :param localfile: string类型，本地文件名称
        :param mime_type: string类型，上传数据的MIME类型
        :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        :return: ret: 如果http状态码为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
        :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
        """
        if localfile:
            self.__localfile = localfile
        if blocksize:
            self.blocksize = blocksize
        if pausepartnumber:
            self.pausepartnumber = pausepartnumber
        if mime_type:
            self.__mimetype = mime_type
        else:
            mime_type = s(mimetype_from_file(self.__localfile))
        with open(self.__localfile, 'rb') as fd:
            fd.seek(self.pausepartnumber * self.blocksize, os.SEEK_SET)
            return self.resumeuploadstream(retrycount, retryinterval, bucket, key, uploadid, blocksize, etaglist, fd, pausepartnumber, mime_type, header)

    def resumeuploadstream(self, retrycount=3, retryinterval=5, bucket=None, key=None, uploadid=None, blocksize=None, etaglist=None, stream=None, pausepartnumber=None, mime_type=None, header=None):
        """
        断点续传失败数据流的分片
        可以在调用uploadstream失败后重新续传，也可以通过传递所有需要的参数续传

        :param retrycount: integer 类型，分片重传次数
        :param retryinterval: integer 类型，同个分片失败重传间隔，单位秒
        :param bucket: string类型, 空间名称
        :param key: string类型，文件或数据在空间中的名称
        :param uploadid: string类型，初始化分片获得的uploadid
        :param blocksize: integer类型，分片大小
        :param etaglist: list类型，元素为已经上传成功的分片的etag
        :param pausepartnumber: integer类型，第一个失败分片的编号（编号从0开始）
        :param stream: file-like对象或者二进制数据流，需要重新上传的数据
        :param mime_type: string类型，上传数据的MIME类型
        :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        :return: ret: 如果http状态码为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
        :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
        """

        if bucket:
            self.__bucket = bucket
        if key:
            self.__key = key
        if uploadid:
            self.uploadid = uploadid
        if blocksize:
            self.blocksize = blocksize
        if stream:
            self.__stream = stream
        if etaglist:
            self.etaglist = etaglist
        if pausepartnumber:
            self.pausepartnumber = pausepartnumber
        if header:
            self.__header = header
        if mime_type is not None:
            self.__mimetype = mime_type
        elif self.__mimetype is None:
            self.__mimetype = 'application/octec-stream'

        if self.__header is None:
            self.__header = dict()
        else:
            _check_dict(self.__header)
        if 'User-Agent' not in self.__header:
            self.__header['User-Agent'] = config.get_default('user_agent')

        # initial sharding request
        if self.uploadid is None:
            ret, resp = self.__initialsharding()
            if resp.ok():
                self.uploadid = ret.get('UploadId')
                self.blocksize = ret.get('BlkSize')
                logger.info('multipart upload id: {0}'.format(self.uploadid))
            else:
                logger.error('multipar upload init failed. error message: {0}'.format(resp.error))
                return ret, resp

        self.__header['Content-Type'] = self.__mimetype
        authorization = self.authorization('put', self.__bucket, self.__key, self.__header)
        self.__header['Authorization'] = authorization

        for data in _file_iter(self.__stream, self.blocksize):
            url = shardingupload_url(self.__bucket, self.__key, self.uploadid, self.pausepartnumber)
            ret = None
            resp = None
            for index in range(retrycount):
                logger.info('retry {0} time sharding upload sharing {1}'.format(index + 1, self.pausepartnumber))
                logger.info('sharding url:{0}'.format(url))
                ret, resp = _shardingupload(url, data, self.__header)
                if not resp.ok():
                    logger.error('failed {0} time when retry upload sharding {1},error message: {2}, uploadid: {3}'.format(index + 1, self.pausepartnumber, resp.error, self.uploadid))
                    if index < retrycount - 1:
                        time.sleep(retryinterval)
                else:
                    break
            if not resp.ok():
                logger.error('retry upload sharding {0} failed, uploadid: {1}'.format(self.pausepartnumber, self.uploadid))
                return ret, resp
            logger.info('retry upload sharding {0} succeed. etag: {1}, uploadid: {2}'.format(self.pausepartnumber, resp.etag, self.uploadid))
            self.pausepartnumber += 1
            self.etaglist.append(resp.etag)
        # finish sharding upload
        logger.info('start finish upload request')
        ret, resp = self.__finishupload()
        if not resp.ok():
            logger.error('multipart upload failed. uploadid:{0}, pausepartnumber: {1}, key: {2} FAIL!!!'.format(self.uploadid, self.pausepartnumber, self.__key))
        else:
            logger.info('mulitpart upload succeed. uploadid: {0}, key: {1} SUCCEED!!!'.format(self.uploadid, self.__key))
        return ret, resp

    def __partthread(self, sem, bucket, key, uploadid, part_number, header, data, retrycount, retryinterval, etaglist, upload_suffix=None):
        with sem:
            url = shardingupload_url(bucket, key, uploadid, part_number, upload_suffix=upload_suffix)
            resp = None
            for index in range(retrycount):
                logger.info('try {0} time sharding upload sharding {1}'.format(index + 1, part_number))
                logger.info('sharding url:{0}'.format(url))
                _, resp = _shardingupload(url, data, header)
                if not resp.ok():
                    logger.error('failed {0} time when upload sharding {1}.error message: {2}, uploadid: {3}'.format(index + 1, part_number, resp.error, uploadid))
                    if index < retrycount - 1:
                        time.sleep(retryinterval)
                else:
                    break

            if not resp.ok():
                logger.error('upload sharding {0} failed. uploadid: {1}'.format(part_number, uploadid))
                exit("part upload failed!")
            logger.info('upload sharding {0} succeed.etag:{1}, uploadid: {2}'.format(part_number, resp.etag, uploadid))
            etaglist[part_number] = resp.etag
