# -*- coding: utf-8 -*-


import platform
from . import __version__

_sys_info = '{0}: {1}'.format(platform.system(), platform.machine())
_python_ver = platform.python_version()

USER_AGENT = 'UCloud UFile Python SDK {0} ({1} : Python/{2})'.format(__version__, _sys_info, _python_ver)
UCLOUD_PROXY_SUFFIX = '.cn-bj.ufileos.com'
UCLOUD_DOWNLOAD_SUFFIX = '.cn-bj.ufileos.com'
UCLOUD_API_URL = 'http://api.ucloud.cn'
BLOCKSIZE = 1024 * 1024 * 4

_config = {
    'connection_timeout': None,
    'expires': 300,
    'upload_suffix': UCLOUD_PROXY_SUFFIX,
    'download_suffix': UCLOUD_DOWNLOAD_SUFFIX,
    'user_agent': USER_AGENT,
    # 调用上传接口时，是否计算 md5
    'md5': False,
}


def get_default(key):
    """
    返回默认配置
    """
    global _config
    return None if key not in _config else _config[key]

def set_default(connection_timeout=None, expires=None, user_agent=None, uploadsuffix=None, downloadsuffix=None, md5=None):
    """
    设置默认配置

    :param connection_timeout: integer类型，网络请求超时时间
    :param expires: integer类型，文件下载链接失效时间
    :user_agent: string类型
    :uploadsuffix: string类型，上传地址后缀
    :downloadsuffix: string类型，下载地址后缀
    :md5: 布尔类型，上传文件是否携带MD5
    """
    global _config
    if connection_timeout:
        _config['connection_timeout'] = connection_timeout
    if expires:
        _config['expires'] = expires
    if user_agent:
        _config['user_agent'] = user_agent
    if uploadsuffix and isinstance(uploadsuffix, str):
        _config['upload_suffix'] = uploadsuffix
    if downloadsuffix and isinstance(downloadsuffix, str):
        _config['download_suffix'] = downloadsuffix
    if md5 != None:
        _config['md5'] = md5
