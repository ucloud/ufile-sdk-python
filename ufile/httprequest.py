# -*- coding: utf-8 -*-

import requests
import re
from . import config
from .logger import logger

def __return_wraper(response, content_consumed=False):
    """
    UCloud UFile 服务器响应的封装

    :param response: requests response object
    :param content_consumed: boolean类型, 如果响应内容被保存在文件中则为真
    :return: ret: 如果http状态码不为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
    :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
    """
    if response.status_code not in [200, 204, 206]:
        return None, ResponseInfo(response)
    content_type = response.headers.get('Content-Type')
    ret = {} if content_consumed else response.json() if isinstance(content_type, str) and content_type.startswith('application/json') else {}
    return ret, ResponseInfo(response, None, content_consumed)


def _put_file(url, header, uploadfile):
    """
    采用普通put方法上传文件到UFile空间

    :param url: string类型，上传的url
    :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
    :param uploadfile: 本地文件名称
    :return: ret: 如果http状态码不为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
    :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
    """
    with open(uploadfile, 'rb') as data:
        return _put_stream(url, header, data)


def _put_stream(url, header, data):
    """
    采用普通方法上传二进制流到UFile空间

    :param url: string类型，上传的url
    :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
    :param data: 二进制数据流
    :return: ret: 如果http状态码不为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
    :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
    """
    try:
        response = requests.put(url, headers=header, data=data, timeout=config.get_default('connection_timeout'))
    except requests.RequestException as e:
        return None, ResponseInfo(None, e)
    return __return_wraper(response)


def _post_file(url, header, data):
    """
    采用表单上传的方法上传文件到空间

    :param url:  string类型，上传的url
    :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
    :param data: 二进制数据流
    :return: ret: 如果http状态码不为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
    :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
    """

    try:
        response = requests.post(url, headers=header, data=data, timeout=config.get_default('connection_timeout'))
    except requests.RequestException as e:
        return None, ResponseInfo(None, e)
    return __return_wraper(response)

def _uploadhit_file(url, header, params):
    """
    秒传文件到空间

    :param url:string类型， 秒传文件的url
    :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
    :param params: dict类型，http 请求的查询参数，键值对类型分别为string类型
    :return: ret: return message, None if response status code not in [200, 204, 206] else a dict-like object with response body
    :return: ResponseInfo: UCloud UFile server response info
    """

    try:
        response = requests.post(url, params=params, headers=header, timeout=config.get_default('connection_timeout'))
    except requests.RequestException as e:
        return None, ResponseInfo(None, e)
    return __return_wraper(response)


def _delete_file(url, header):
    """
    删除文件

    :param url: string类型, 要删除文件的url
    :param header: dict 类型，键值对类型分别为string类型，HTTP请求头
    :return: ret: 如果http状态码不为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
    :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
    """
    try:
        response = requests.delete(url, headers=header, timeout=config.get_default('connection_timeout'))
    except requests.RequestException as e:
        return None, ResponseInfo(None, e)
    return __return_wraper(response)

def _head_file(url,header):
    """
    获取文件信息

    :param url: string类型, 要删除文件的url
    :param header: dict 类型，键值对类型分别为string类型，HTTP请求头
    :return: ret: 如果http状态码不为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
    :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
    """
    try:
        response=requests.head(url, headers=header, timeout=config.get_default('connection_timeout'))
    except requests.RequestException as e:
        return None, ResponseInfo(None, e)
    return __return_wraper(response)

def _initialsharding(url, header):
    """
    初始化分片请求

    :param url:  string类型, 初始化分片请求的url
    :param header: dict 类型，键值对类型分别为string类型，HTTP请求头
    :return: ret: 如果http状态码不为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
    :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
    """
    try:
        response = requests.post(url, headers=header, timeout=config.get_default('connection_timeout'))
    except requests.RequestException as e:
        return None, ResponseInfo(None, e)
    return __return_wraper(response)


def _shardingupload(url, data, header):
    """
    分片上传数据

    :param url: string类型，分片上传数据的url
    :param data: bytes 类型，分片上传的二进制数据
    :param header: dict 类型，键值对类型分别为string类型，HTTP请求头
    :return: ret: 如果http状态码不为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
    :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
    """
    try:
        response = requests.put(url, headers=header, data=data, timeout=config.get_default('connection_timeout'))
    except requests.RequestException as e:
        return None, ResponseInfo(None, e)
    return __return_wraper(response)


def _finishsharding(url, param, header, data):
    """
    结束分片上传请求

    :param url:  string类型, 初始化分片请求的url
    :param header: dict 类型，键值对类型分别为string类型，HTTP请求头
    :return: ret: 如果http状态码不为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
    :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
    """
    try:
        response = requests.post(url, headers=header, params=param, data=data, timeout=config.get_default('connection_timeout'))
    except requests.RequestException as e:
        return None, ResponseInfo(None, e)
    return __return_wraper(response)


def _download_file(url, header, localfile):
    """
    下载文件

    :param url: string类型, 下载UFile资源的url
    :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
    :param localfile: string类型, 保存文件的本地名称
    :return: ret: 如果http状态码不为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
    :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
    """
    try:
        response = requests.get(url, headers=header, stream=True)
    except requests.RequestException as e:
        return None, ResponseInfo(None, e)
    if response.status_code in [200, 206]:
        with open(localfile, 'wb') as fd:
            for block in response.iter_content(config.BLOCKSIZE):
                fd.write(block)
    else:
        return __return_wraper(response)
    return __return_wraper(response, True)

def _getfilelist(url, header, param):
    """
    获取文件列表

    :param url: string 类型，获取文件列表的url
    :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
    :return: ret: 如果http状态码不为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
    :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
    """

    try:
        response = requests.get(url, headers=header, params=param, timeout=config.get_default('connection_timeout'))
    except requests.RequestException as e:
        logger.error('send request error:{0}'.format(e))
        return None, ResponseInfo(None, e)
    return __return_wraper(response)

def _listobjects(url, header, param):
    """
    获取目录文件列表

    :param url: string 类型，获取目录文件列表的url
    :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
    :return: ret: 如果http状态码不为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
    :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
    """

    try:
        response = requests.get(url, headers=header, params=param, timeout=config.get_default('connection_timeout'))
    except requests.RequestException as e:
        logger.error('send request error:{0}'.format(e))
        return None, ResponseInfo(None, e)
    return __return_wraper(response)

def _restore_file(url, header):
    """
    解冻冷存文件请求

    :param url:  string类型, 解冻请求的url
    :param header: dict 类型，键值对类型分别为string类型，HTTP请求头
    :return: ret: 如果http状态码不为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
    :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
    """

    try:
        response = requests.put(url, headers=header, timeout=config.get_default('connection_timeout'))
    except requests.RequestException as e:
        return None, ResponseInfo(None, e)
    return __return_wraper(response)

def _classswitch_file(url, header, params):
    """
    文件存储类型转换请求

    :param url:string类型，文件存储类型转换的url
    :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
    :param params: dict类型，http 请求的查询参数，键值对类型分别为string类型
    :return: ret: return message, None if response status code not in [200, 204, 206] else a dict-like object with response body
    :return: ResponseInfo: UCloud UFile server response info
    """

    try:
        response = requests.put(url, params=params, headers=header, timeout=config.get_default('connection_timeout'))
    except requests.RequestException as e:
        return None, ResponseInfo(None, e)
    return __return_wraper(response)

def _copy_file(url, header):
    """
    拷贝文件到空间

    :param url:string类型， 拷贝文件的url
    :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
    :return: ret: return message, None if response status code not in [200, 204, 206] else a dict-like object with response body
    :return: ResponseInfo: UCloud UFile server response info
    """

    try:
        response = requests.put(url, headers=header, timeout=config.get_default('connection_timeout'))
    except requests.RequestException as e:
        return None, ResponseInfo(None, e)
    return __return_wraper(response)

def _rename_file(url, header, params):
    """
    重命名文件到空间

    :param url:string类型， 重命名文件的url
    :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
    :param params: dict类型，http 请求的查询参数，键值对类型分别为string类型
    :return: ret: return message, None if response status code not in [200, 204, 206] else a dict-like object with response body
    :return: ResponseInfo: UCloud UFile server response info
    """

    try:
        response = requests.put(url, params=params, headers=header, timeout=config.get_default('connection_timeout'))
    except requests.RequestException as e:
        return None, ResponseInfo(None, e)
    return __return_wraper(response)

def _bucket_request(url, param, header):
    """
    UCloud UFile 空间管理请求

    :param url: String类型，空间管理请求的url
    :param param: dict类型，键值对类型分别为string类型，HTTP请求的查询参数
    :param header: dict类型，键值对类型分别为string类型，HTTP请求头信息
    :return: ret: 如果http状态码不为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
    :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
    """
    try:
        response = requests.get(url, headers=header, params=param)
    except requests.RequestException as e:
        return None, ResponseInfo(None, e)
    return __return_wraper(response)


class ResponseInfo(object):
    """
    UCloud UFile 服务器返回信息,解析UCloud UFile服务器返回信息以及网络连接问题

    Attributes:
        content: 服务器返回信息的二级制数据块，如果出现网络连接问题则为None
        status_code: Integer类型，服务器返回信息状态码，如果出现网络连接问题则为-1
        error:       string类型，服务器返回错误信息或者网络连接问题
        x_session_id: String类型，UFile服务器处理请求失败响应的会话ID，如果正常或出现网络连接问题则为None
        content_type: string，UFile服务器返回信息的类型，如果出现网络连接问题则为None
        content_length: integer类型，服务器返回信息长度，如果出现网络连接问题则为None
        content_range: 文件下载的数据范围，None或者元素为两个整数的元组
        ret_code:       Integer类型, UCloud UFile 服务内部错误码,正确服务或者网络连接则为0
        etag:           string类型,文件的etag，无则为None
    """
    def __init__(self, response, exception=None, content_consumed=False):
        """
        初始化 ResponseInfo 实例

        :param response: requests response object
        :param exception: exception object
        :param content_consumed: boolean 类型, 如果响应内容被保存则为True
        :return: None
        """
        self.__response = response
        self.exception = exception

        if response is None:
            self.status_code = -1
            self.error = str(exception)
            self.x_session_id = None
            self.etag = None
            self.content_type = None
            self.content_length = None
            self.content_range = None
            self.ret_code = None
            self.content = None
            self.md5 = None
        else:
            self.status_code = response.status_code
            self.x_session_id = response.headers.get('X-SessionId')
            self.content_type = response.headers.get('Content-Type')
            self.md5 = response.headers.get('Content-MD5')
            self.content_length = response.headers.get('Content-Length')
            content_length = response.headers.get('content-range')
            self.content = None if content_consumed else response.content
            if content_length is not None:
                byteslist = re.split('[- /]', content_length)
                self.content_range = (int(byteslist[1]), int(byteslist[2]))
            else:
                self.content_range = None
            self.etag = response.headers.get('Etag')
            if self.status_code not in [200, 204, 206]:
                ret = response.json() if response.headers.get('Content-Type') == 'application/json' and len(response.text) > 0 else None
                if ret is None:
                    self.error = 'unknown error'
                    self.ret_code = -1
                else:
                    self.ret_code = ret['RetCode']
                    self.error = ret['ErrMsg']
            else:
                self.error = None
                self.ret_code = None

    def ok(self):
        """
        返回请求是否成功

        :return: boolean类型, 请求成功则返回True
        """
        return self.status_code in [200, 204, 206]

    def need_retry(self):
        """
        返回是否由于网络连接异常需要重新请求

        :return: boolean 类型
        """
        return self.__response is None

    def __str__(self):
        """

        :return: string类型，Response的信息
        """

        return ', '.join(['{0}: {1}'.format(key, value) for (key, value) in self.__dict__.items() if key != 'content'])

    def __repr__(self):
        """
        The response info

        :return:: string
        """
        return self.__str__
