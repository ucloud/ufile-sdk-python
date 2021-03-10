# -*- coding: utf-8 -*-

from .compact import *
from . import config

import base64
import hashlib
import os
import struct

import mimetypes
from os import path
import warnings
from .config import BLOCKSIZE 

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
    ".ipa": "application/vnd.ios.package-archive",
    ".323": "text/h323",
    ".3gp": "video/3gpp",
    ".3gpp": "video/3gpp",
    ".7z": "application/x-7z-compressed",
    ".acx": "application/internet-property-stream",
    ".ai": "application/postscript",
    ".aif": "audio/x-aiff",
    ".aifc": "audio/x-aiff",
    ".aiff": "audio/x-aiff",
    ".asf": "video/x-ms-asf",
    ".asr": "video/x-ms-asf",
    ".asx": "video/x-ms-asf",
    ".atom": "application/atom+xml",
    ".au": "audio/basic",
    ".avi": "video/x-msvideo",
    ".axs": "application/olescript",
    ".bas": "text/plain",
    ".bcpio": "application/x-bcpio",
    ".bin": "application/octet-stream",
    ".bmp": "image/bmp",
    ".c": "text/plain",
    ".cat": "application/vnd.ms-pkiseccat",
    ".cco": "application/x-cocoa",
    ".cdf": "application/x-cdf",
    ".cer": "application/x-x509-ca-cert",
    ".class": "application/octet-stream",
    ".clp": "application/x-msclip",
    ".cmx": "image/x-cmx",
    ".cod": "image/cis-cod",
    ".cpio": "application/x-cpio",
    ".crd": "application/x-mscardfile",
    ".crl": "application/pkix-crl",
    ".crt": "application/x-x509-ca-cert",
    ".csh": "application/x-csh",
    ".css": "text/css",
    ".dcr": "application/x-director",
    ".der": "application/x-x509-ca-cert",
    ".dir": "application/x-director",
    ".dll": "application/octet-stream",
    ".dms": "application/octet-stream",
    ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".dot": "application/msword",
    ".dvi": "application/x-dvi",
    ".dxr": "application/x-director",
    ".ear": "application/java-archive",
    ".eot": "application/vnd.ms-fontobject",
    ".eps": "application/postscript",
    ".etx": "text/x-setext",
    ".evy": "application/envoy",
    ".exe": "application/octet-stream",
    ".fif": "application/fractals",
    ".flr": "x-world/x-vrml",
    ".flv": "video/x-flv",
    ".gif": "image/gif",
    ".gtar": "application/x-gtar",
    ".gz": "application/x-gzip",
    ".h": "text/plain",
    ".hdf": "application/x-hdf",
    ".hlp": "application/winhlp",
    ".hqx": "application/mac-binhex40",
    ".hta": "application/hta",
    ".htc": "text/x-component",
    ".htm": "text/html",
    ".html": "text/html",
    ".htt": "text/webviewhtml",
    ".ico": "image/x-icon",
    ".ief": "image/ief",
    ".iii": "application/x-iphone",
    ".ins": "application/x-internet-signup",
    ".isp": "application/x-internet-signup",
    ".jad": "text/vnd.sun.j2me.app-descripto",
    ".jar": "application/java-archive",
    ".jardiff": "application/x-java-archive-diff",
    ".jfif": "image/pipeg",
    ".jng": "image/x-jng",
    ".jnlp": "application/x-java-jnlp-file",
    ".jpe": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".js": "application/x-javascript",
    ".json": "application/json",
    ".kar": "audio/midi",
    ".kml": "application/vnd.google-earth.kml+xml",
    ".kmz": "application/vnd.google-earth.kmz",
    ".latex": "application/x-latex",
    ".lha": "application/octet-stream",
    ".lsf": "video/x-la-asf",
    ".lsx": "video/x-la-asf",
    ".lzh": "application/octet-stream",
    ".m13": "application/x-msmediaview",
    ".m14": "application/x-msmediaview",
    ".m3u": "audio/x-mpegurl",
    ".m3u8": "application/vnd.apple.mpegurl",
    ".m4a": "audio/x-m4a",
    ".m4v": "video/x-m4v",
    ".man": "application/x-troff-man",
    ".mdb": "application/x-msaccess",
    ".me": "application/x-troff-me",
    ".mht": "message/rfc822",
    ".mhtml": "message/rfc822",
    ".mid": "audio/midi",
    ".midi": "audio/midi",
    ".mml": "text/mathml",
    ".mng": "video/x-mng",
    ".mny": "application/x-msmoney",
    ".mov": "video/quicktime",
    ".movie": "video/x-sgi-movie",
    ".mp2": "video/mpeg",
    ".mp3": "audio/mpeg",
    ".mp4": "video/mp4",
    ".mpa": "video/mpeg",
    ".mpe": "video/mpeg",
    ".mpeg": "video/mpeg",
    ".mpg": "video/mpeg",
    ".mpp": "application/vnd.ms-project",
    ".mpv2": "video/mpeg",
    ".ms": "application/x-troff-ms",
    ".mvb": "application/x-msmediaview",
    ".nws": "message/rfc822",
    ".oda": "application/oda",
    ".ogg": "audio/ogg",
    ".p10": "application/pkcs10",
    ".p12": "application/x-pkcs12",
    ".p7b": "application/x-pkcs7-certificates",
    ".p7c": "application/x-pkcs7-mime",
    ".p7m": "application/x-pkcs7-mime",
    ".p7r": "application/x-pkcs7-certreqresp",
    ".p7s": "application/x-pkcs7-signature",
    ".pbm": "image/x-portable-bitmap",
    ".pdb": "application/x-pilot",
    ".pdf": "application/pdf",
    ".pem": "application/x-x509-ca-cert",
    ".pfx": "application/x-pkcs12",
    ".pgm": "image/x-portable-graymap",
    ".pko": "application/ynd.ms-pkipko",
    ".pl": "application/x-perl",
    ".pm": "application/x-perl",
    ".pma": "application/x-perfmon",
    ".pmc": "application/x-perfmon",
    ".pml": "application/x-perfmon",
    ".pmr": "application/x-perfmon",
    ".pmw": "application/x-perfmon",
    ".png": "image/png",
    ".pnm": "image/x-portable-anymap",
    ".pot,": "application/vnd.ms-powerpoint",
    ".ppm": "image/x-portable-pixmap",
    ".pps": "application/vnd.ms-powerpoint",
    ".ppt": "application/vnd.ms-powerpoint",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".prc": "application/x-pilot",
    ".prf": "application/pics-rules",
    ".ps": "application/postscript",
    ".pub": "application/x-mspublisher",
    ".qt": "video/quicktime",
    ".ra": "audio/x-pn-realaudio",
    ".ram": "audio/x-pn-realaudio",
    ".rar": "application/x-rar-compressed",
    ".ras": "image/x-cmu-raster",
    ".rgb": "image/x-rgb",
    ".rmi": "audio/mid",
    ".roff": "application/x-troff",
    ".rpm": "application/x-redhat-package-manager",
    ".rss": "application/rss+xml",
    ".rtf": "application/rtf",
    ".rtx": "text/richtext",
    ".run": "application/x-makeself",
    ".scd": "application/x-msschedule",
    ".sct": "text/scriptlet",
    ".sea": "application/x-sea",
    ".setpay": "application/set-payment-initiation",
    ".setreg": "application/set-registration-initiation",
    ".sh": "application/x-sh",
    ".shar": "application/x-shar",
    ".shtml": "text/html",
    ".sit": "application/x-stuffit",
    ".snd": "audio/basic",
    ".spc": "application/x-pkcs7-certificates",
    ".spl": "application/futuresplash",
    ".src": "application/x-wais-source",
    ".sst": "application/vnd.ms-pkicertstore",
    ".stl": "application/vnd.ms-pkistl",
    ".stm": "text/html",
    ".sv4cpio": "application/x-sv4cpio",
    ".sv4crc": "application/x-sv4crc",
    ".svg": "image/svg+xml",
    ".svgz": "image/svg+xml",
    ".swf": "application/x-shockwave-flash",
    ".t": "application/x-troff",
    ".tar": "application/x-tar",
    ".tcl": "application/x-tcl",
    ".tex": "application/x-tex",
    ".texi": "application/x-texinfo",
    ".texinfo": "application/x-texinfo",
    ".tgz": "application/x-compressed",
    ".tif": "image/tiff",
    ".tiff": "image/tiff",
    ".tk": "application/x-tcl",
    ".tr": "application/x-troff",
    ".trm": "application/x-msterminal",
    ".ts": "video/mp2t",
    ".tsv": "text/tab-separated-values",
    ".txt": "text/plain",
    ".uls": "text/iuls",
    ".ustar": "application/x-ustar",
    ".vcf": "text/x-vcard",
    ".vrml": "x-world/x-vrml",
    ".war": "application/java-archive",
    ".wav": "audio/x-wav",
    ".wbmp": "image/vnd.wap.wbmp",
    ".wcm": "application/vnd.ms-works",
    ".wdb": "application/vnd.ms-works",
    ".webm": "video/webm",
    ".webp": "image/webp",
    ".wks": "application/vnd.ms-works",
    ".wmf": "application/x-msmetafile",
    ".wml": "text/vnd.wap.wml",
    ".wmlc": "application/vnd.wap.wmlc",
    ".wmv": "video/x-ms-wmv",
    ".woff": "application/font-woff",
    ".wps": "application/vnd.ms-works",
    ".wri": "application/x-mswrite",
    ".wrl": "x-world/x-vrml",
    ".wrz": "x-world/x-vrml",
    ".xaf": "x-world/x-vrml",
    ".xbm": "image/x-xbitmap",
    ".xhtml": "application/xhtml+xml",
    ".xla": "application/vnd.ms-excel",
    ".xlc": "application/vnd.ms-excel",
    ".xlm": "application/vnd.ms-excel",
    ".xls": "application/vnd.ms-excel",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".xlt": "application/vnd.ms-excel",
    ".xlw": "application/vnd.ms-excel",
    ".xml": "text/xml",
    ".xof": "x-world/x-vrml",
    ".xpi": "application/x-xpinstall",
    ".xpm": "image/x-xpixmap",
    ".xspf": "application/xspf+xml",
    ".xwd": "image/x-xwindowdump",
    ".z": "application/x-compress",
    ".zip": "application/zip",
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


def file_etag(localfile, size=BLOCKSIZE):
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

def deprecated(message):
  def deprecated_decorator(func):
      def deprecated_func(*args, **kwargs):
          warnings.warn("Call to deprecated function {} . -- {}".format(func.__name__, message),
                        category=DeprecationWarning,
                        stacklevel=2)
          warnings.simplefilter('default', DeprecationWarning)
          return func(*args, **kwargs)
      return deprecated_func
  return deprecated_decorator