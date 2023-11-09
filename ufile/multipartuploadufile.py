# -*- coding: utf-8 -*-

import json
import math
import os
import threading
import time

from . import config
from .baseufile import BaseUFile
from .compact import s
from .httprequest import ResponseInfo, _initialsharding, _finishsharding, _shardingupload, _get_multi_upload_part
from .logger import logger
from .util import _check_dict, initialsharding_url, finishsharding_url, shardingupload_url, _file_iter, \
    mimetype_from_file, mimetype_from_buffer, deprecated, ufile_listparts_url


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

    def uploadstream(self, bucket, key, stream, maxthread=4, retrycount=3, retryinterval=5, mime_type=None,
                     header=None):
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

        self.__threaddict = {}  # 线程字典，用于保证finish前等待运行中的uploadpart线程
        self.__errresp = None  # 用于主函数返回的errresp

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
            logger.error('multipart upload init failed. error message: {0}'.format(resp.error))
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

        sem = threading.Semaphore(maxthread)
        partnumber = 0
        for data in _file_iter(self.__stream, self.blocksize):
            sem.acquire()  # 控制最大并发线程数
            if self.__errresp:  # 如果有分片上传失败，停止后续分片上传
                sem.release()
                break
            self.etaglist.append("")
            thread1 = threading.Thread(target=self.__partthread, args=(
                sem, self.__bucket, self.__key, self.uploadid, partnumber, self.__header, data, retrycount,
                retryinterval,
                self.etaglist, self.__upload_suffix))
            self.__threaddict[partnumber] = thread1
            thread1.start()
            partnumber += 1

        for thread in list(self.__threaddict.values()):  # 转为list是因为遍历字典时长度变化会报错
            thread.join()

        if self.__errresp:
            self.pausepartnumber = self.etaglist.index("")
            logger.error(
                'multipart upload failed. uploadid:{0}, pausepartnumber: {1}, key: {2} , error message{3}. FAIL!!!'.format(
                    self.uploadid, self.pausepartnumber, self.__key, self.__errresp.error))
            return None, self.__errresp
        else:
            self.pausepartnumber = len(self.etaglist)

        logger.info('start finish sharding request.')
        ret, resp = self.__finishupload()
        if not resp.ok():
            logger.error(
                'multipart upload failed. uploadid:{0}, pausepartnumber: {1}, key: {2}, error message: {3}. FAIL!!!'.format(
                    self.uploadid, self.pausepartnumber, self.__key, resp.error))
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

    @deprecated("Deprecated since version 3.2.6")
    def resumeuploadfile(self, retrycount=3, retryinterval=5, bucket=None, key=None, uploadid=None, blocksize=None,
                         etaglist=None, localfile=None, pausepartnumber=None, mime_type=None, header=None):
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
            return self.resumeuploadstream(retrycount, retryinterval, bucket, key, uploadid, blocksize, etaglist, fd,
                                           pausepartnumber, mime_type, header)

    def resumeuploadstream(self, retrycount=3, retryinterval=5, bucket=None, key=None, uploadid=None, blocksize=None,
                           etaglist=None, stream=None, pausepartnumber=None, mime_type=None, header=None):
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
                    logger.error(
                        'failed {0} time when retry upload sharding {1},error message: {2}, uploadid: {3}'.format(
                            index + 1, self.pausepartnumber, resp.error, self.uploadid))
                    if index < retrycount - 1:
                        time.sleep(retryinterval)
                else:
                    break
            if not resp.ok():
                logger.error(
                    'retry upload sharding {0} failed, uploadid: {1}'.format(self.pausepartnumber, self.uploadid))
                return ret, resp
            logger.info(
                'retry upload sharding {0} succeed. etag: {1}, uploadid: {2}'.format(self.pausepartnumber, resp.etag,
                                                                                     self.uploadid))
            self.pausepartnumber += 1
            self.etaglist.append(resp.etag)
        # finish sharding upload
        logger.info('start finish upload request')
        ret, resp = self.__finishupload()
        if not resp.ok():
            logger.error(
                'multipart upload failed. uploadid:{0}, pausepartnumber: {1}, key: {2} FAIL!!!'.format(self.uploadid,
                                                                                                       self.pausepartnumber,
                                                                                                       self.__key))
        else:
            logger.info(
                'mulitpart upload succeed. uploadid: {0}, key: {1} SUCCEED!!!'.format(self.uploadid, self.__key))
        return ret, resp

    def __partthread(self, sem, bucket, key, uploadid, part_number, header, data, retrycount, retryinterval, etaglist,
                     upload_suffix=None):
        url = shardingupload_url(bucket, key, uploadid, part_number, upload_suffix=upload_suffix)
        resp = None
        for index in range(retrycount):
            logger.info('try {0} time sharding upload sharding {1}'.format(index + 1, part_number))
            logger.info('sharding url:{0}'.format(url))
            _, resp = _shardingupload(url, data, header)
            if not resp.ok():
                logger.error(
                    'failed {0} time when upload sharding {1}.error message: {2}, uploadid: {3}'.format(index + 1,
                                                                                                        part_number,
                                                                                                        resp.error,
                                                                                                        uploadid))
                if index < retrycount - 1:
                    time.sleep(retryinterval)
            else:
                break

        if not resp.ok():
            logger.error('upload sharding {0} failed. uploadid: {1}'.format(part_number, uploadid))
            self.__errresp = resp
        else:
            logger.info('upload sharding {0} succeed.etag:{1}, uploadid: {2}'.format(part_number, resp.etag, uploadid))
            etaglist[part_number] = resp.etag
        self.__threaddict.pop(part_number)
        sem.release()

    def init_multipart_upload(self, bucket, key, header=None, upload_suffix=None):
        """
        初始化分片请求

        :param bucket: string类型，空间名称
        :param key: string类型，文件或数据在空间中的名称
        :param header: dict类型，HTTP请求头部
        :param upload_suffix: string类型, 如果传入此参数, 则会忽略 config 中配置的 upload_suffix 字段
        :return: (dict, ResponseInfo) tuple类型，dict为返回的json信息，ResponseInfo为请求的返回信息
        """
        self.__bucket = bucket
        self.__key = key
        self.__header = header if header else dict()
        if 'User-Agent' not in self.__header:
            self.__header['User-Agent'] = config.get_default('user_agent')
        self.__upload_suffix = upload_suffix if upload_suffix else config.get_default('upload_suffix')
        ret, resp = self.__initialsharding()
        if resp.ok:
            self.uploadid = ret.get('UploadId')
            self.blocksize = ret.get('BlkSize')
        return ret, resp

    def finish_upload(self):
        """
        完成分片请求

        :return: (dict, ResponseInfo) tuple类型，dict为返回的json信息，ResponseInfo为请求的返回信息
        """
        return self.__finishupload()

    def upload_part_copy(self, source_bucket, source_key, mime_type, offset, size, part_number, upload_suffix=None):
        """
        分片COPY上传

        :param source_bucket: string类型, 空间名称
        :param source_key: string类型，文件或数据在空间中的名称
        :param mime_type: string类型，上传数据的MIME类型
        :param offset: int类型, copy文件的起始位置
        :param size: int类型, copy文件的大小, 不能大于源文件大小
        :param part_number: int类型, 分片号
        :param upload_suffix: string类型, 如果传入此参数, 则会忽略 config 中配置的 upload_suffix 字段
        :return: ret: 如果http状态码为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
        :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
        """
        self.__mimetype = mime_type
        self.__upload_suffix = config.get_default("upload_suffix") if upload_suffix is None else upload_suffix
        self.__header.update({"X-Ufile-Copy-Source": "/%s/%s" % (source_bucket, source_key)})
        self.__header.update({"Content-Type": self.__mimetype})
        self.__header.update({"X-Ufile-Copy-Source-Range": "bytes=%d-%d" % (offset, size - 1)})
        if 'User-Agent' not in self.__header:
            self.__header['User-Agent'] = config.get_default('user_agent')
        authorization = self.authorization('put', self.__bucket, self.__key, self.__header)
        self.__header.update({"Authorization": authorization})

        url = shardingupload_url(self.__bucket, self.__key, self.uploadid, part_number,
                                 upload_suffix=self.__upload_suffix)
        ret, resp = _shardingupload(url, None, self.__header)
        if resp.ok:
            self.etaglist.append(resp.etag)
        return ret, resp

    def get_multi_upload_part(self, bucket, upload_id, max_parts=None, part_number_marker=None, header=None, upload_suffix=None):
        """
        获取未完成分片上传的对象的已上传成功的分片列表。

        :param bucket: string类型，空间名称
        :param upload_id: string类型，初始化分片上传时返回的uploadid
        :param max_parts: int类型，返回的最大条目数，默认为1000
        :param part_number_marker: int类型，返回的起始条目，默认为0
        :param header: dict类型，HTTP请求头部
        :param upload_suffix: string类型, 如果传入此参数, 则会忽略 config 中配置的 upload_suffix 字段
        :return: (dict, ResponseInfo) tuple类型，dict为返回的json信息，ResponseInfo为请求的返回信息
        """
        self.__header = header if header else dict()
        if 'User-Agent' not in self.__header:
            self.__header['User-Agent'] = config.get_default('user_agent')
        if upload_suffix is not None:
            self.__upload_suffix = upload_suffix
        authorization = self.authorization('get', bucket, "", self.__header, action='muploadpart')
        self.__header.update({"Authorization": authorization})
        url = ufile_listparts_url(bucket, self.__upload_suffix, upload_id, max_parts, part_number_marker)
        return _get_multi_upload_part(url, self.__header)
