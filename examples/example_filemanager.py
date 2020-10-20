from common import *
from ufile import config, filemanager
import os

# 运行时, 请自行修改
BUCKET_BJ = 'lovecrazy-private'
BJ_UPLOAD_SUFFIX = '.cn-bj.ufileos.com'

BUCKET_SH2 = 'lovecrazy'
SH2_UPLOAD_SUFFIX = '.cn-sh2.ufileos.com'

# 待上传文件路径，最好填绝对路径
UPLOAD_FILE_PATH = './example.jpg'
# 下载文件保存的文件路径
SAVE_FILE_PATH = './download.jpg'

# 设置默认参数
config.set_default(uploadsuffix=BJ_UPLOAD_SUFFIX)
config.set_default(downloadsuffix=BJ_UPLOAD_SUFFIX)
config.set_default(connection_timeout=60)
config.set_default(expires=60)
config.set_default(md5=True)


filemgr_bj = filemanager.FileManager(PUBLIC_KEY, PRIVATE_KEY)
filemgr_sh = filemanager.FileManager(PUBLIC_KEY, PRIVATE_KEY, upload_suffix=SH2_UPLOAD_SUFFIX, download_suffix=SH2_UPLOAD_SUFFIX)

# 上传 文件 UPLOAD_FILE_PATH 到 BUCKET_BJ 上传后的文件名为 python-sdk/examples/putfile-key
_, resp = filemgr_bj.putfile(BUCKET_BJ, 'python-sdk/examples/putfile-key', UPLOAD_FILE_PATH)
assert resp.status_code == 200

# 上传 文件 UPLOAD_FILE_PATH 到 BUCKET_SH2 上传后的文件名为 python-sdk/examples/putfile-key
_, resp = filemgr_sh.putfile(BUCKET_SH2, 'python-sdk/examples/putfile-key', UPLOAD_FILE_PATH)
assert resp.status_code == 200


# 下载
_, resp = filemgr_bj.download_file(BUCKET_BJ, 'python-sdk/examples/putfile-key', SAVE_FILE_PATH)
assert resp.status_code == 200
os.remove(SAVE_FILE_PATH)

_, resp = filemgr_sh.download_file(BUCKET_SH2, 'python-sdk/examples/putfile-key', SAVE_FILE_PATH)
assert resp.status_code == 200
os.remove(SAVE_FILE_PATH)

################### 其他更多方法请查阅 SDK
