# -*- coding: utf-8 -*-

import logging


LOG_FILE = 'ufile.log'
_formatter = logging.Formatter('[%(asctime)s, %(levelname)s]: %(filename)s-%(lineno)s: %(message)s')

_ch = logging.StreamHandler()
_ch.setLevel(logging.INFO)
_ch.setFormatter(_formatter)

logger = logging.getLogger("UCLOUD")
logger.setLevel(logging.INFO)
logger.addHandler(_ch)


def set_log_file(localfile=None):
    """
    设置日志的存放文件

    :param localfile: 存放日志文件名
    :return: None
    """
    global LOG_FILE
    if localfile is not None:
        LOG_FILE = localfile
    _fh = logging.FileHandler(LOG_FILE)
    _fh.setLevel(logging.INFO)
    _fh.setFormatter(_formatter)
    logger.addHandler(_fh)
