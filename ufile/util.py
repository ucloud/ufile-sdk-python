# -*- coding: utf-8 -*-

from .compact import *
from . import config

import base64
import hashlib
import os
import struct

import mimetypes
from os import path

_EXTRA_TYPES_MAP = {
    ".js": "application/javascript",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".xltx": "application/vnd.openxmlformats-officedocument.spreadsheetml.template",
    ".potx": "application/vnd.openxmlformats-officedocument.presentationml.template",
    ".ppsx": "application/vnd.openxmlformats-officedocument.presentationml.slideshow",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".sldx": "application/vnd.openxmlformats-officedocument.presentationml.slide",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".dotx": "application/vnd.openxmlformats-officedocument.wordprocessingml.template",
    ".xlam": "application/vnd.ms-excel.addin.macroEnabled.12",
    ".xlsb": "application/vnd.ms-excel.sheet.binary.macroEnabled.12",
    ".apk": "application/vnd.android.package-archive",
    ".ipa": "application/vnd.ios.package-archive"
}


def urlsafe_b64encode(data):
    """
    urlsafe base64 encode

    :param data: string类型，待编码的字符串
    :return: string类型，编码的字符串
    """
    return s(base64.urlsafe_b64encode(b(data)))


def urlsafe_b64decode(data):
    """
    urlsafe base64 decode

    :param data: string类型，待解码的字符串
    :return: string类型，解码的字符串
    """
    return b(base64.urlsafe_b64decode(s(data)))


def standard_b64encode(data):
    """
    standard base64 encode

    :param data: string类型，待编码的字符串
    :return: string类型，编码的字符串
    """
    return s(base64.standard_b64encode(b(data)))


def standard_b64decode(data):
    """
    standard base64 decode

    :param data: string类型，待解码的字符串
    :return: string类型，解码的字符串
    """
    return b(base64.standard_b64decode(s(data)))


def _file_iter(input_stream, size):
    """
    二进制流迭代器

    :param input_stream: 二进制流
    :param size: integer类型，每次读取的块的大小
    :return: 指定大小的二进制块，如果读取失败会抛出IOError的异常
    """
    d = input_stream.read(size)
    while d:
        yield d
        d = input_stream.read(size)


def file_etag(localfile, size):
    """
    计算本地文件的etag

    :param localfile: string类型, 本地文件名
    :param size: integer类型, 分块大小
    :return: string类型, 本地文件的etag
    """

    filesize = os.path.getsize(localfile)
    blockcnt = filesize // size if filesize % size == 0 else filesize // size + 1

    hashstr = b''
    with open(localfile, 'rb') as input_stream:
        for block in _file_iter(input_stream, size):
            sha = hashlib.new('sha1')
            sha.update(b(block))
            hashstr += sha.digest()

    if blockcnt > 1:
        sha = hashlib.sha1()
        sha.update(hashstr)
        hashstr = sha.digest()

    return urlsafe_b64encode(struct.pack('@I', blockcnt) + hashstr)


def _check_dict(data):
    """
    check the type of data

    :param data: 键值对类型分别为string类型的dict类型
    :return: boolean类型，如果类型正确则返回True，否则抛出ValueError异常
    """
    if data is not None and isinstance(data, dict):
        return True
    raise ValueError('The input is not a dict-like object')


def ufile_put_url(bucket, key, upload_suffix=None):
    """
    采用普通上传方法上传UCloud UFile文件的url

    :param bucket: string类型, 待创建的空间名称
    :param key:  string类型, 在空间中的文件名
    :return: string类型, 普通上传UFile的url
    """
    return 'http://{0}{1}/{2}'.format(bucket, upload_suffix or config.get_default('upload_suffix'), key)


def ufile_post_url(bucket, upload_suffix=None):
    """
    采用表单上传方法上传UCloud UFile文件的url

    :param bucket: string类型, 待创建的空间名称
    :return: string类型, 表单上传UFile的url
    """
    return 'http://{0}{1}/'.format(bucket, upload_suffix or config.get_default('upload_suffix'))


def ufile_uploadhit_url(bucket, upload_suffix=None):
    """
    秒传UCloud UFile文件的url

    :param bucket: string类型, 待创建的空间名称
    :return: string类型, 秒传UFile的url
    """
    return 'http://{0}{1}/uploadhit'.format(bucket, upload_suffix or config.get_default('upload_suffix'))


def initialsharding_url(bucket, key, upload_suffix=None):
    """
    初始化分片上传UCloud UFile的url

    :param bucket: string类型, 待创建的空间名称
    :param key:  string类型, 在空间中的文件名
    :return: string类型, 初始化分片上传UFile的url
    """
    return 'http://{0}{1}/{2}?uploads'.format(bucket, upload_suffix or config.get_default('upload_suffix'), key)


def finishsharding_url(bucket, key, upload_suffix=None):
    """
    结束分片上传UCloud UFile的url

    :param bucket: string类型, 待创建的空间名称
    :param key:  string类型, 在空间中的文件名
    :return: string类型, 结束分片上传UFile的url
    """
    return ufile_put_url(bucket, key, upload_suffix=upload_suffix)


def shardingupload_url(bucket, key, uploadid, part_number, upload_suffix=None):
    """
    分片上传UCloud UFile的url

    :param bucket: string类型, 待创建的空间名称
    :param key:  string类型, 在空间中的文件名
    :param uploadid: string类型, 初始化分片上传获得的uploadid字符串
    :param part_number: integer类型, 分片上传的编号,从0开始
    :return: string类型, 结束分片上传UFile的url
    """
    return 'http://{0}{1}/{2}?uploadId={3}&partNumber={4}'.format(bucket, upload_suffix or config.get_default('upload_suffix'), key, uploadid, s(str(part_number)))

def ufile_getfilelist_url(bucket, upload_suffix=None):
    """
    获取文件列表的url

    :param bucket: string 类型，获取的空间名称
    :return: string类型，获取文件列表的url
    """
    return 'http://{0}{1}/?list'.format(bucket, upload_suffix or config.get_default('upload_suffix'))

def mimetype_from_file(file):
    """
    获取文件的mimetype

    :param bucket: string 类型，获取的文件名称
    :return: string类型，获取文件的mimetype
    """
    ext = path.splitext(file)[1].lower()
    if ext in _EXTRA_TYPES_MAP:
        return _EXTRA_TYPES_MAP[ext]
    elif mimetypes.guess_type(file)[0] is not None:
        return mimetypes.guess_type(file)[0]

    return 'application/unknowntype'

def mimetype_from_buffer(stream):
    """
    获取流对象的mimetype

    :param bucket: string 类型，获取的流对象名称
    :return: string类型，获取流对象的mimetype
    """
    return 'application/octet-stream'

def ufile_restore_url(bucket, key, upload_suffix=None):
    """
    解冻冷存文件的url

    :param bucket: string类型, 待创建的空间名称
    :param key:  string类型, 在空间中的文件名
    :return: string类型, 解冻文件的url
    """
    return 'http://{0}{1}/{2}?restore'.format(bucket, upload_suffix or config.get_default('upload_suffix'), key)

def ufile_classswitch_url(bucket, key, upload_suffix=None):
    """
    文件存储类型转换的url

    :param bucket: string类型, 待创建的空间名称
    :param key:  string类型, 在空间中的文件名
    :return: string类型, 类型转换的url
    """
    return 'http://{0}{1}/{2}'.format(bucket, upload_suffix or config.get_default('upload_suffix'), key)

def ufile_copy_url(bucket, key, upload_suffix=None):
    """
    拷贝文件的url

    :param bucket: string类型, 待创建的空间名称
    :param key:  string类型, 在空间中的目标文件名
    :return: string类型, 拷贝文件的url
    """
    return 'http://{0}{1}/{2}'.format(bucket, upload_suffix or config.get_default('upload_suffix'), key)

def ufile_rename_url(bucket, key, upload_suffix=None):
    """
    重命名文件的url

    :param bucket: string类型, 待创建的空间名称
    :param key:  string类型, 在空间中的源文件名
    :param newkey:  string类型, 在空间中的目标文件名
    :return: string类型, 重命名文件的url
    """
    return 'http://{0}{1}/{2}'.format(bucket, upload_suffix or config.get_default('upload_suffix'), key)

def ufile_listobjects_url(bucket, upload_suffix=None):
    """
    获取目录文件列表的url

    :param bucket: string 类型，获取的空间名称
    :return: string类型，获取目录文件列表的url
    """
    return 'http://{0}{1}/?listobjects'.format(bucket, upload_suffix or config.get_default('upload_suffix'))

