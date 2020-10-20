# -*- coding: utf-8 -*-


import os
import time
import hashlib
import json
from .baseufile import BaseUFile
from .httprequest import _put_stream, _put_file, _post_file, ResponseInfo, _uploadhit_file, _download_file, _delete_file, _getfilelist,_head_file, _restore_file, _classswitch_file, _copy_file, _rename_file, _listobjects
from .util import _check_dict, ufile_put_url, ufile_post_url, file_etag, ufile_uploadhit_url, ufile_getfilelist_url, mimetype_from_file, ufile_restore_url, ufile_classswitch_url, ufile_copy_url, ufile_rename_url, ufile_listobjects_url
from .logger import logger
from .compact import b, s, u, url_parse
from . import config
from .config import BLOCKSIZE
import string


class FileManager(BaseUFile):
    """
    UCloud UFile普通上传文件类
    """
    def __init__(self, public_key, private_key, upload_suffix=None, download_suffix=None):
        """
        初始化 PutUFile 实例

        :param public_key: string类型, 账户API公私钥中的公钥
        :param private_key: string类型, 账户API公私钥中的私钥
        :param upload_suffix: string类型, 如果传入此参数, 则会忽略 config 中配置的 upload_suffix 字段
        :param download_suffix: string类型, 如果传入此参数, 则会忽略 config 中配置的 download_suffix 字段
        :return: None，如果为非法的公私钥，则抛出ValueError异常
        """
        super(FileManager, self).__init__(public_key, private_key)
        self.__upload_suffix = upload_suffix
        self.__download_suffix = download_suffix

    def _get_download_domain(self, bucket):
        return 'http://{0}{1}'.format(bucket, self.__download_suffix or config.get_default('download_suffix'))

    def putstream(self, bucket, key, stream, mime_type=None, header=None):
        """
        上传二进制流到空间

        :param bucket: string类型，上传空间名称
        :param key:  string 类型，上传文件在空间中的名称
        :param stream: 二进制数据流,从文件指针位置开始发送数据,在调用时需调用者自己调整文件指针位置
        :param mime_type: 二进制数据流的MIME类型
        :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        :return: ret: 如果http状态码为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
        :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
        """
        if header is None:
            header = dict()
        else:
            _check_dict(header)
        if 'User-Agent' not in header:
            header['User-Agent'] = config.get_default('user_agent')

        if mime_type is None:
            mime_type = 'application/octet-stream'
        header['Content-Type'] = mime_type
        if config.get_default('md5') == True:
            m = hashlib.md5()
            m.update(stream.getvalue())
            header['Content-MD5'] = m.hexdigest()
            stream.seek(0, os.SEEK_SET)
        authorization = self.authorization('put', bucket, key, header)
        header['Authorization'] = authorization
        url = ufile_put_url(bucket, key, upload_suffix=self.__upload_suffix)
        logger.info('start put stream to bucket {0} as {1}'.format(bucket, key))
        logger.info('put UFile url: {0}'.format(url))
        logger.info('request header:\n{0}'.format(json.dumps(header, indent=4)))
        return _put_stream(url, header, stream)

    def putfile(self, bucket, key, localfile, header=None):
        """
        upload localfile to bucket as key

        :param bucket: string类型，上传空间名称
        :param key:  string 类型，上传文件在空间中的名称
        :param localfile: string类型，本地文件名称
        :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        :return: ret: 如果http状态码为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
        :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
        """
        if header is None:
            header = dict()
        else:
            _check_dict(header)
        if 'User-Agent' not in header:
            header['User-Agent'] = config.get_default('user_agent')
        mime_type = s(mimetype_from_file(localfile))
        file_size = os.path.getsize(localfile)
        header['Content-Type'] = mime_type
        if config.get_default('md5') == True:
            with open(localfile, 'rb') as data:
                m = hashlib.md5()
                m.update(data.read())
                header['Content-MD5'] = m.hexdigest()
                data.seek(0, os.SEEK_SET)
        authorization = self.authorization('put', bucket, key, header)
        header['Authorization'] = authorization
        if file_size!=0:
            header['Content-Length'] = str(file_size)
        url = ufile_put_url(bucket, key, upload_suffix=self.__upload_suffix)
        logger.info('start put file {0} to bucket {1} as {2}'.format(localfile, bucket, key))
        logger.info('put UFile url: {0}'.format(url))
        logger.info('request header:\n{0}'.format(json.dumps(header, indent=4)))
        return _put_file(url, header, localfile)

    def postfile(self, bucket, key, localfile, header=None):
        """
        表单上传文件到UFile空间

        :param bucket: string类型，上传空间名称
        :param key:  string 类型，上传文件在空间中的名称
        :param localfile: string类型，本地文件名称
        :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        :return: ret: 如果http状态码为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
        :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
        """
        if header is None:
            header = dict()
        _check_dict(header)
        if 'User-Agent' not in header:
            header['User-Agent'] = config.get_default('user_agent')
        mime_type = s(mimetype_from_file(localfile))

        # update the request header content-type
        boundary = self.__make_boundary()
        header['Content-Type'] = 'multipart/form-data; boundary={0}'.format(boundary)

        # form fields
        authorization = self.authorization('post', bucket, key, header, mime_type)
        fields = dict()
        fields['FileName'] = key
        fields['Authorization'] = authorization
        with open(localfile, 'rb') as stream:
            postdata = self.__make_postbody(boundary, fields, stream, mime_type, localfile)

        # update the request header content-length
        header['Content-Length'] = str(len(postdata))

        # post url
        url = ufile_post_url(bucket, upload_suffix=self.__upload_suffix)

        # start post file
        logger.info('start post file {0} to bucket {1} as {2}'.format(localfile, bucket, key))
        logger.info('post url is {0}'.format(url))

        return _post_file(url, header, postdata)

    def __make_boundary(self):
        """
        生成post内容主体的限定字符串

        :return:: string类型
        """
        t = time.time()
        m = hashlib.md5()
        m.update(b(str(t)))
        return m.hexdigest()

    def __make_postbody(self, boundary, fields, stream, mime_type, localfile):
        """
        生成post请求内容主体

        :param boundary: string类型，post内容主体的限定字符串
        :param fields: ditc类型，键值对类型分别为string类型
        :param stream: 可读的file-like object(file object 或者BytesIO)
        :param mime_type: string类型，上传文件或数据的MIME类型
        :param localfile: string类型，上传文件或数据的本地名称
        :return: 二进制数据流
        """

        binarystream = b''
        for (key, value) in fields.items():
            binarystream += b('--{0}\r\n'.format(boundary))
            binarystream += b('Content-Disposition: form-data; name="{0}"\r\n'.format(key))
            binarystream += b('\r\n')
            binarystream += b('{0}\r\n'.format(value))

        binarystream += b('--{0}\r\n'.format(boundary))
        binarystream += b('Content-Disposition: form-data; name="file"; filename="{0}"\r\n'.format(localfile))
        binarystream += b('Content-Type: {0}\r\n'.format(mime_type))
        binarystream += b('\r\n')

        binarystream += stream.read()
        binarystream += b('\r\n')
        binarystream += b('--{0}\r\n'.format(boundary))

        return binarystream

    def uploadhit(self, bucket, key, localfile, header=None):
        """
        尝试秒传文件到UFile空间

        :param bucket: string类型，上传空间名称
        :param key:  string 类型，上传文件在空间中的名称
        :param localfile: string类型，本地文件名称
        :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        :return: ret: 如果http状态码为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
        :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
        """

        if header is None:
            header = dict()
        _check_dict(header)
        if 'User-Agent' not in header:
            header['User-Agent'] = config.get_default('user_agent')

        filesize = os.path.getsize(localfile)
        fileetags = file_etag(localfile, BLOCKSIZE)
        mimetype = s(mimetype_from_file(localfile))

        # update request header
        header['Content-Type'] = mimetype
        header['Content-Length'] = str(0)
        authorization = self.authorization('post', bucket, key, header)
        header['Authorization'] = authorization

        # parameter
        params = {'Hash': fileetags,
                  'FileName': key,
                  'FileSize': filesize}

        url = ufile_uploadhit_url(bucket, upload_suffix=self.__upload_suffix)

        logger.info('start upload hit localfile {0} as {1} in bucket {2}'.format(localfile, key, bucket))
        logger.info('request url: {0}'.format(url))

        return _uploadhit_file(url, header, params)

    def download_file(self, bucket, key, localfile, isprivate=True, expires=None, content_range=None, header=None):
        """
        下载UFile文件并且保存为本地文件

        :param bucket: string类型, UFile空间名称
        :param key: string类型， 下载文件在空间中的名称
        :param localfile: string类型，要保存的本地文件名称
        :param isprivate: boolean类型，如果为私有空间则为True
        :param expires: integer类型，私有文件链接有效时间
        :param content_range: tuple类型，元素为两个整型
        :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        :return: ret: 如果http状态码为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
        :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
        """
        if header is None:
            header = dict()
        else:
            _check_dict(header)

        if expires is None:
            expires = config.get_default('expires')

        if 'User-Agent' not in header:
            header['User-Agent'] = config.get_default('user_agent')

        if isinstance(content_range, tuple) and len(content_range) == 2:
            header['Range'] = 'bytes=' + '-'.join(map(lambda x: str(x), content_range))

        if not isprivate:
            url = self.public_download_url(bucket, key)
        else:
            url = self.private_download_url(bucket, key, expires, header, True)

        logger.info('get ufile url:{0}'.format(url))

        return _download_file(url, header, localfile)

    def public_download_url(self, bucket, key):
        """
        从公共空间下载文件的url

        :param bucket: string类型, 空间名称
        :param key: string类型，下载数据在空间中的名称
        :return: string类型，下载数据的url
        """
        return self._get_download_domain(bucket) + '/' + key

    def private_download_url(self, bucket, key, expires=None, header=None, internal=False):
        """
        从私有空间下载文件的url

        :param bucket: string类型, 空间名称
        :param key: string类型，下载数据在空间中的名称
        :param expires:  integer类型, 下载链接有效时间，单位为秒
        :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        :return: string, 从私有空间下载文件和数据的url
        """
        if header is None:
            header = dict()
        else:
            _check_dict(header)
        if 'User-Agent' not in header:
            header['User-Agent'] = config.get_default('user_agent')

        if expires is None:
            expires = config.get_default('expires')
        expires += int(time.time())
        header['Expires'] = s(str(expires))

        signature = self.signature(bucket, key, 'get', header)
        query = { 'UCloudPublicKey': self._public_key(),
                  'Expires': str(expires),
                  'Signature': signature }
        query_str = url_parse(query)

        url = self._get_download_domain(bucket) + '/' + key
        if internal:
            return url + '?' + query_str
        return url + '?UCloudPublicKey={0}&Expires={1}&Signature={2}'.format(self._public_key(), str(expires), signature)

    def private_head_url(self, bucket, key, expires=None, header=None):
        """
        从私有空间下载文件的url

        :param bucket: string类型, 空间名称
        :param key: string类型，下载数据在空间中的名称
        :param expires:  integer类型, 下载链接有效时间，单位为秒
        :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        :return: string, 从私有空间下载文件和数据的url
        """
        if header is None:
            header = dict()
        else:
            _check_dict(header)
        if 'User-Agent' not in header:
            header['User-Agent'] = config.get_default('user_agent')

        if expires is None:
            expires = config.get_default('expires')
        expires += int(time.time())
        header['Expires'] = s(str(expires))

        signature = self.signature(bucket, key, 'head', header)
        return self._get_download_domain(bucket) + '/' + key + '?UCloudPublicKey={0}&Expires={1}&Signature={2}'.format(self._public_key(), str(expires), signature)

    def deletefile(self, bucket, key, header=None):
        """
        删除空间中文件方法

        :param bucket: string类型, 空间名称
        :param key:  string类型, 被删除文件在空间中的名称
        :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        :return: ret: 如果http状态码为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
        :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
        """
        if header is None:
            header = dict()
        else:
            _check_dict(header)
        if 'User-Agent' not in header:
            header['User-Agent'] = config.get_default('user_agent')

        authorization = self.authorization('delete', bucket, key, header)
        header['Authorization'] = authorization

        logger.info('start delete file {0} in bucket {1}'.format(key, bucket))
        url = ufile_put_url(bucket, key, upload_suffix=self.__upload_suffix)

        return _delete_file(url, header)

    def getfilelist(self, bucket, prefix=None, marker=None, limit=None, header=None):
        """
        获取bucket下的文件列表

        :param bucket: string 类型，空间名称
        :param prefix: string 类型，文件前缀, 默认为空字符串
        :param marker: string 类型，文件列表起始位置, 默认为空字符串
        :param limit: integer 类型，文件列表数目, 默认为20
        :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        :return: ret: 如果http状态码为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
        :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
        """
        if header is None:
            header = dict()
        else:
            _check_dict(header)
        if 'User-Agent' not in header:
            header['User-Agent'] = config.get_default('user_agent')

        header['Content-Length'] = str(0)
        authorization = self.authorization('get', bucket, '', header)
        header['Authorization'] = authorization
        param = dict()
        if marker is not None and isinstance(marker, str):
            param['marker'] = s(marker)
        if prefix is not None and isinstance(prefix, str):
            param['prefix'] = s(prefix)
        if limit is not None and isinstance(limit, int):
            param['limit'] = s(str(limit))
        info_message = ''.join(['start get file list from bucket {0}'.format(bucket), '' if marker is None else ', marker: {0}'.format(marker if isinstance(marker, str) else marker.encode('utf-8')), '' if limit is None else ', limit: {0}'.format(limit), '' if prefix is None else ', prefix: {0}'.format(prefix)])
        logger.info(info_message)
        url = ufile_getfilelist_url(bucket, upload_suffix=self.__upload_suffix)
        return _getfilelist(url, header, param)

    def head_file(self, bucket, key, header=None):
        """
        获取空间中文件信息方法

        :param bucket: string类型, 空间名称
        :param key:  string类型, 文件在空间中的名称
        :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        :return: ret: 如果http状态码为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
        :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
        """
        if header is None:
            header=dict()
        else:
            _check_dict(header)
        if 'User-Agent' not in header:
            header['User-Agent'] = config.get_default('user_agent')

        authorization = self.authorization('head', bucket, key, header)
        header['Authorization'] = authorization

        logger.info('start head file {0} in bucket {1}'.format(key, bucket))
        url = ufile_put_url(bucket, key, upload_suffix=self.__upload_suffix)

        return _head_file(url, header)

    def compare_file_etag(self, bucket, remotekey, localfile):
        """
        比对空间文件和本地文件方法

        :param bucket: string类型, 空间名称
        :param remotekey:  string类型, 文件在空间中的名称
        :param localfile: string类型，本地文件的路径
        :return:True为比对一致，False为不一致
        """
        ret,resp=self.head_file(bucket, remotekey)
        remote_etag=resp.etag.strip('\"')
        local_etag=file_etag(localfile, BLOCKSIZE)
        return (remote_etag==local_etag)

    def restore_file(self, bucket, key, header=None):
        """
        解冻冷存文件方法

        :param bucket: string类型, 空间名称
        :param key:  string类型, 文件在空间中的名称
        :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        :return: ret: 如果http状态码为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
        :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
        """
        if header is None:
            header=dict()
        else:
            _check_dict(header)
        if 'User-Agent' not in header:
            header['User-Agent'] = config.get_default('user_agent')

        authorization = self.authorization('put', bucket, key, header)
        header['Authorization'] = authorization

        logger.info('start restore file {0} in bucket {1}'.format(key, bucket))
        url = ufile_restore_url(bucket, key, upload_suffix=self.__upload_suffix)

        return _restore_file(url, header)

    def class_switch_file(self, bucket, key, storageclass, header=None):
        """
        文件存储类型转换方法

        :param bucket: string类型, 空间名称
        :param key:  string类型, 文件在空间中的名称
        :param storageclass:  string类型
        尝试拷贝文件到UFile空间, 文件目标存储类型
        :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        :return: ret: 如果http状态码为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
        :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
        """
        if header is None:
            header=dict()
        else:
            _check_dict(header)
        if 'User-Agent' not in header:
            header['User-Agent'] = config.get_default('user_agent')

        authorization = self.authorization('put', bucket, key, header)
        header['Authorization'] = authorization

        # parameter
        params = {'storageClass': storageclass}

        logger.info('start switch file {0} storage class in bucket {1}'.format(key, bucket))
        url = ufile_classswitch_url(bucket, key, upload_suffix=self.__upload_suffix)

        return _classswitch_file(url, header, params)

    def copy(self, bucket, key, srcbucket, srckey, header=None):
        """
        尝试拷贝文件到UFile空间

        :param bucket: string类型，上传空间名称
        :param key:  string 类型，新文件在空间中的名称
        :param srcbucket: string类型，源文件所在空间名称
        :param srckey: string类型，源文件名称
        :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        :return: ret: 如果http状态码为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
        :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
        """

        if header is None:
            header = dict()
        _check_dict(header)
        if 'User-Agent' not in header:
            header['User-Agent'] = config.get_default('user_agent')

        # update request header
        header['X-Ufile-Copy-Source'] = "/" + srcbucket + "/" + srckey
        header['Content-Length'] = str(0)
        authorization = self.authorization('put', bucket, key, header)
        header['Authorization'] = authorization

        url = ufile_copy_url(bucket, key, upload_suffix=self.__upload_suffix)

        logger.info('start copy {0} in {1} to {2} in {3}'.format(srckey, srcbucket, key, bucket))
        logger.info('request url: {0}'.format(url))

        return _copy_file(url, header)

    def rename(self, bucket, key, newkey, force='true', header=None):
        """
        重命名文件方法

        :param bucket: string类型, 空间名称
        :param key:  string类型, 源文件在空间中的名称
        :param newkey:  string类型, 文件重命名后的新名称
        :param force:  string类型, 是否强行覆盖文件，值为'true'会覆盖，其他值则不会
        :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        :return: ret: 如果http状态码为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
        :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
        """
        if header is None:
            header=dict()
        else:
            _check_dict(header)
        if 'User-Agent' not in header:
            header['User-Agent'] = config.get_default('user_agent')

        authorization = self.authorization('put', bucket, key, header)
        header['Authorization'] = authorization

        # parameter
        params = {'newFileName': newkey,
                  'force': force}

        logger.info('start rename {0} in bucket {1}'.format(key, bucket))
        url = ufile_rename_url(bucket, key, upload_suffix=self.__upload_suffix)

        return _rename_file(url, header, params)

    def listobjects(self, bucket, prefix=None, marker=None, maxkeys=None, delimiter=None, header=None):
        """
        获取bucket下的文件列表

        :param bucket: string 类型，空间名称
        :param prefix: string 类型，返回以prefix作为前缀的目录文件列表
        :param marker: string 类型，返回以字母排序后，大于marker的目录文件列表
        :param maxkeys: integer 类型，指定返回目录文件列表的最大数量，默认值为100
        :param delimiter: stringr 类型，目录分隔符，当前只支持"/"和""，当delimiter设置为"/"时，返回目录形式的文件列表，当delimiter设置为""时，返回非目录层级文件列表
        :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        :return: ret: 如果http状态码为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
        :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
        """
        if header is None:
            header = dict()
        else:
            _check_dict(header)
        if maxkeys is None:
            maxkeys = 100
        if 'User-Agent' not in header:
            header['User-Agent'] = config.get_default('user_agent')

        header['Content-Length'] = str(0)
        param = dict()
        if marker is not None and isinstance(marker, str):
            param['marker'] = s(marker)
        if prefix is not None and isinstance(prefix, str):
            param['prefix'] = s(prefix)
        if maxkeys is not None and isinstance(maxkeys, int):
            param['max-keys'] = s(str(maxkeys))
        if delimiter is not None and isinstance(delimiter, str):
            param['delimiter'] = s(delimiter)

        authorization = self.authorization('get', bucket, '', header, '', 'listobjects', param)
        header['Authorization'] = authorization

        info_message = ''.join(['start list objects from bucket {0}'.format(bucket), '' if marker is None else ', marker: {0}'.format(marker if isinstance(marker, str) else marker.encode('utf-8')), '' if maxkeys is None else ', maxkeys: {0}'.format(maxkeys), '' if prefix is None else ', prefix: {0}'.format(prefix), '' if delimiter is None else ', delimiter: {0}'.format(delimiter)])
        logger.info(info_message)
        url = ufile_listobjects_url(bucket, upload_suffix=self.__upload_suffix)
        return _listobjects(url, header, param)

