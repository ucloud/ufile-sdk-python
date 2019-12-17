#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import sys
import os
import io
import codecs 
import json
sys.path.append(os.path.realpath(os.path.dirname(__file__)))

from ufile import filemanager
from ufile import multipartuploadufile 
from ufile import config
from ufile.logger import logger, set_log_file
#import argparse


set_log_file()

PUBLIC_KEY = ''
PRIVATE_KEY = ''
MPUT_THREADS = 4 

class UploadFailed(Exception):
    pass


class DownloadFailed(Exception):
    pass

class HeadFailed(Exception):
    pass


#上传小文件，支持本地标准输入作为输入，参数local_file 填入 - 号
def upload_put(bucket, key, local_file, header):
    # 构造上传对象，并设置公私钥
    handler = filemanager.FileManager(PUBLIC_KEY, PRIVATE_KEY)

    if local_file == '-':
        fileno = sys.stdin.fileno()
        with open(fileno, "rb", closefd=False) as input_stream:
            _, resp = handler.putstream(bucket, key, input_stream, header=header, mime_type='application/octec-stream')
    else:
        _, resp = handler.putfile(bucket, key, local_file, header=header)
    if resp.status_code != 200:
        print(resp.error)
        raise UploadFailed()

    print("Success: ", bucket, key, resp)


#上传大文件，支持本地标准输入作为输入，参数local_file 填入 - 号
def upload_mput(bucket, key, local_file, header,maxthread):
    # 构造上传对象，并设置公私钥
    handler = multipartuploadufile.MultipartUploadUFile(PUBLIC_KEY, PRIVATE_KEY)

    if local_file == '-':
        fileno = sys.stdin.fileno()
        _, resp = handler.uploadfile(bucket, key, fileno, maxthread=maxthread, header=header, mime_type='application/octec-stream')
    else:
        _, resp = handler.uploadfile(bucket, key, local_file, maxthread=maxthread, header=header)
    if resp.status_code != 200:
        print(resp.error)
        raise UploadFailed()

    print("Success: ", bucket, key, resp)


#下载文件
def download(bucket, key, local_file, header):
    # 构造下载对象，并设置公私钥
    handler = filemanager.FileManager(PUBLIC_KEY, PRIVATE_KEY)

    if local_file == '-':
        local_file = '/dev/stdout'
    _, resp = handler.download_file(bucket, key, local_file, header=header)
    if resp.status_code != 200:
        print(resp.error)
        raise DownloadFailed()

    if local_file != "/dev/stdout":
        print("Success: ", bucket, key, resp)


#head文件
def head(bucket, key, header):
    # 构造下载对象，并设置公私钥
    handler = filemanager.FileManager(PUBLIC_KEY, PRIVATE_KEY)

    _, resp = handler.head_file(bucket, key, header=header)
    if resp.status_code != 200:
        print(resp.error)
        raise HeadFailed()
    print("Success: ", bucket, key, resp)

def usage():
    print('Usage:')
    print('''
python ./ufile_op.py [upload_put| upload_mput| download| head] [domain] [key] [file]

NOTE:
    if file is "-", it means:
    - stdin for upload
    - stdout for download
''')


def main():
    if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv)<4:
        usage()
        sys.exit(1)

    global PUBLIC_KEY
    global PRIVATE_KEY
    
    #读取配置文件
    if os.path.exists('config.cfg'):		
        f = open('config.cfg','r')
        text = f.read()
        f.close()
        paras = json.loads(text)
        #PUBLIC_KEY = paras['public_key'].encode('unicode-escape').decode('string_escape')
        PUBLIC_KEY = paras['public_key']
        #PRIVATE_KEY = paras['private_key'].encode('unicode-escape').decode('string_escape')
        PRIVATE_KEY = paras['private_key']
    else:
        print("config.cfg not exists!")
        sys.exit(1)
		
    if PUBLIC_KEY=="" or PRIVATE_KEY=="":
        print("please set config.cfg keys!")
        sys.exit(1)

		#解析参数和处理
    action = sys.argv[1]
    domain = sys.argv[2]
    key = sys.argv[3]
    local_file = ""
    if(len(sys.argv)>4):
        local_file = sys.argv[4]

    if len(domain.split("."))<2:
    	print('domain error!')
    	sys.exit(1)
    bucket = domain.split(".")[0]
    suffix = domain.split(bucket)[1]
    
    sys.stderr.write("{0} {1} {2} {3} {4}\n".format(os.path.realpath(__file__), action, domain, key, local_file ))
    header = {
        'Host':
        '{0}'.format(domain)
    }

    config.set_default(uploadsuffix=suffix, downloadsuffix=suffix)

    if action == 'upload_put':
        upload_put(bucket, key, local_file, header)
    elif action == 'upload_mput':
        upload_mput(bucket, key, local_file, header,maxthread=MPUT_THREADS)
    elif action == 'download':
        download(bucket, key, local_file, header)
    elif action == 'head':
        head(bucket, key, header)
    else:
        print("err cmd!")


if __name__ == '__main__':
    main()
