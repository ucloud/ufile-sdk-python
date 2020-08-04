# -*- coding: utf-8 -*-

import string
from .auth import Auth
from .util import _check_dict


class BaseUFile(object):
    """
    UCloud UFile 内容管理的基类，主要包括不同操作的公共方法
    """
    def __init__(self, public_key, private_key):
        """
        初始化 BaseUFile 对象

        :param public_key: string类型， 账户API公私钥的公钥
        :param private_key: string类型，账户API公私钥的私钥
        :return: None，如果为非法的公私钥则抛出ValueError异常
        """
        self.__auth = Auth(public_key, private_key)

    def set_keys(self, public_key, private_key):
        """
        重新设置账户API公私钥

        :param public_key: string类型， 账户API公私钥的公钥
        :param private_key: string类型，账户API公私钥的私钥
        :return: None，如果为非法的公私钥则抛出ValueError异常
        """
        self.__auth.set_keys(public_key, private_key)

    def authorization(self, method, bucket, key, header=None, mime_type=None, action=None, url_param=None):
        """
        根据不同的上传方法和HTTP请求头获得上传凭证

        :param method: string类型，文件上传方法，为'put'或'post'
        :param bucket: string类型，上传的空间名称
        :param key: string类型，文件在上传空间中的名称
        :param header: dict类型，键值对类型分别为string类型，HTTP请求的header
        :param mime_type: string类型，上传文件的MIME，如果提供则采用其计算文件上传凭证
        :param action: string类型，请求动作
        :param url_param: dict类型，键值对分别为string类型，HTTP请求url参数
        :return: string类型，本次文件上传的上传凭证
        """
        if header is None:
            header = dict()
        else:
            _check_dict(header)
        if action is None:
            action = ''
        if url_param is None:
            url_param = dict()
        data = self.__digest_authorization_data(method, bucket, key, header, mime_type, action, url_param)
        return self.__auth.ufile_authorization(data)

    def signature(self, bucket, key, method="get", header=None, mime_type=None):
        """
        根据不同的HTTP请求headers获得文件下载凭证

        :param bucket: string类型, 下载文件所在空间名称
        :param key:    string类型，现在文件在空间中名称
        :param method: string类型，为'get'
        :param header: dict类型，键值对类型分别为string类型，HTTP请求的header
        :param mime_type: string类型，上传文件的MIME，如果提供则采用其计算文件上传凭证
        :return: string类型，本次文件下载的下载签名
        """

        if header is None:
            header = dict()
        else:
            _check_dict(header)
        data = self.__digest_signature_data(bucket, key, method, header, mime_type)
        return self.__auth.ufile_signature(data)

    def __digest_authorization_data(self, method, bucket, key, header=None, mime_type=None, action=None, url_param=None):
        """
        获得进行认证的字符串

        :param method: string类型, 为'put','post'和 'delete'
        :param bucket: string类型，空间名称
        :param key:    string类型，文件在空间中的名称
        :param header: dict类型，键值对类型分别为string类型，HTTP请求的header
        :param mime_type: string类型，上传文件的MIME，如果提供则采用其计算文件上传凭证
        :param action: string类型，请求动作
        :param url_param: dict类型，键值对分别为string类型，HTTP请求url参数
        :return: string类型，将要进行认证的字符串
        """
        if header is None:
            header = dict()
        else:
            _check_dict(header)
        data = ''.join([method.upper(), '\n'])
        data += ''.join(['' if 'Content-MD5' not in header else header['Content-MD5'], '\n'])
        data += ''.join([mime_type if mime_type is not None else '' if 'Content-Type' not in header else header['Content-Type'], '\n'])
        data += ''.join(['' if 'Date' not in header else header['Date'], '\n'])
        data += ''.join([self.__canonicalize_ucloud_headers(header), self.__canonicalize_resource(bucket, key), self.__canonicalize_url_params(action, url_param)])
        return data


    def __digest_signature_data(self, bucket, key, method='get', header=None, mime_type=None):
        """
        获得进行下载签名的字符串

        :param bucket: string类型， 空间名称
        :param key: string类型， 文件在空间中的名称
        :param method: string类型，'get'
        :param header: dict类型，键值对类型分别为string类型，HTTP请求的header
        :param mime_type: string类型，上传文件的MIME，如果提供则采用其计算文件上传凭证
        :return: string类型，将要进行签名的字符串
        """
        data = ''.join([method.upper(), '\n'])
        data += ''.join(['' if 'Content-MD5' not in header else header['Content-MD5'], '\n'])
        data += ''.join([mime_type if mime_type is not None else '' if 'Content-Type' not in header else header['Content-Type'], '\n'])
        data += ''.join(['' if 'Expires' not in header else header['Expires'], '\n'])
        data += ''.join([self.__canonicalize_ucloud_headers(header), self.__canonicalize_resource(bucket, key)])
        return data

    def __canonicalize_ucloud_headers(self, header):
        """
        字符串化UCloud附加标头

        :param header: dict类型，键值对类型分别为string类型，UCloud附加标头，键名以'X-UCloud-'开头
        :return: string类型
        """
        # 以下语法不适用于Python 2.6
        # ucloud_headers_map = {string.lower(x).strip(): x for x in header if string.lower(x).strip().startswith('x-ucloud-')}
        ucloud_headers_map = dict([(x.lowerx.strip(), x) for x in header if x.lower().strip().startswith('x-ucloud-')])
        ucloud_keys = sorted(ucloud_headers_map)
        return '\n'.join([x+':'+header[ucloud_headers_map[x]].strip() for x in ucloud_keys])

    def __canonicalize_url_params(self, action, url_param):
        """
        字符串化url中的参数

        :param action: string类型，请求动作
        :param url_param: dict类型，键值对分别为string类型，HTTP请求url参数
        :return: string类型
        """
        if action == 'listobjects':
            return ''.join('\nlistobjects\ndelimiter:{0}\nmarker:{1}\nmax-keys:{2}\nprefix:{3}'.format(url_param['delimiter'], url_param['marker'], url_param['max-keys'],  url_param['prefix']))
        return ''

    def __canonicalize_resource(self, bucket, key):
        """
        获得UFile 资源字符串

        :param bucket: string类型, 空间名称
        :param key: string类型，文件在空间中的名称
        :return: string类型，UFile资源字符串
        """
        return '/{0}/{1}'.format(bucket, key)

    def _public_key(self):
        """
        返回账户公私钥中的公钥

        :return: string类型，公钥
        """
        return self.__auth._public_key()
