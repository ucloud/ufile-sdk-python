# -*- coding: utf-8 -*-

import hmac
import hashlib

from .compact import b, s
from .util import standard_b64encode, _check_dict
from .logger import logger
from functools import reduce


class Auth(object):
    """
    UCloud API 认证类
    对UCloud UFile 上传认证、下载签名和API调用签名接口的具体实现
    """

    def __init__(self, public_key, private_key):
        """
        初始化 Auth 实例

        :param public_key: string类型, 账户公私钥中的公钥
        :param private_key: string类型，账户公私钥中的私钥
        :return 无，当采用非法的公私钥会抛出异常
        """

        self.__checkkey(public_key, private_key)
        self.__public_key = public_key
        self.__private_key = private_key

    def set_keys(self, public_key, private_key):
        """
        重新设置账户API的公私钥

        :param public_key:  string类型, 账户公私钥中的公钥
        :param private_key: string类型, 账户公私钥中的私钥
        :return: 无，当采用非法的公私钥会抛出异常
        """

        self.__checkkey(public_key, private_key)
        self.__public_key = public_key
        self.__private_key = b(private_key)

    def bucket_signature(self, query):
        """
        UCloud UFile 空间管理签名

        :param query: 一个键值对类型为'string: string'字典类型的HTTP请求参数，比如{'Action': 'CreateBucket', 'BucketName': 'bucket'}
        :return: string 类型，UCloud UFile空间管理签名
        """

        _check_dict(query)
        query['PublicKey'] = self.__public_key
        sign_string = reduce(lambda y, x: ''.join([x, query[x], y]), sorted(query.keys(), reverse=True), self.__private_key)
        hashstr = hashlib.sha1(b(sign_string))
        return s(hashstr.hexdigest())

    def ufile_signature(self, data):
        """
        UCloud UFile 下载签名

        :param data: String 类型，待授权签名的字符串
        :return: string类型，采用standard_b64encode编码的UCloud UFile下载签名字符串
        """

        hashstr = hmac.new(b(self.__private_key), b(data), hashlib.sha1)
        return standard_b64encode(hashstr.digest())

    def ufile_authorization(self, data):
        """
        UCloud UFile 上传凭证

        :param data: string 类型，待计算上传凭证的字符串
        :return: string类型，UCloud UFile上传凭证的字符串
        """

        signature = self.ufile_signature(data)
        return '{0} {1}:{2}'.format('UCloud', self.__public_key, signature)

    def _public_key(self):
        """
        获得UCloud 账户API公钥

        :return: string类型，UCloud账户API中的公钥
        """

        return self.__public_key

    @staticmethod
    def __checkkey(public_key, private_key):
        if not (public_key and private_key) or not isinstance(public_key, str) or not isinstance(private_key, str):
            raise ValueError('invalid API keys')