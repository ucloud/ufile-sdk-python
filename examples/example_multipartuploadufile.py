from common import *
from ufile import config, multipartuploadufile

# 运行时, 请自行修改
BUCKET_BJ = 'lovecrazy-private'
BJ_UPLOAD_SUFFIX = '.cn-bj.ufileos.com'

BUCKET_SH2 = 'lovecrazy'
SH2_UPLOAD_SUFFIX = '.cn-sh2.ufileos.com'

# 待上传文件路径，最好填绝对路径
UPLOAD_FILE_PATH = './example.jpg'

# 设置默认参数
config.set_default(uploadsuffix=BJ_UPLOAD_SUFFIX)
config.set_default(downloadsuffix=BJ_UPLOAD_SUFFIX)
config.set_default(connection_timeout=60)
config.set_default(expires=60)
config.set_default(md5=True)

# 上传到北京的bucket
mup_bj = multipartuploadufile.MultipartUploadUFile(PUBLIC_KEY, PRIVATE_KEY)
_, resp = mup_bj.uploadfile(BUCKET_BJ, 'python-sdk/examples/multipartput-key', UPLOAD_FILE_PATH)
assert resp.status_code == 200

# 上传到上海的bucket
mup_sh = multipartuploadufile.MultipartUploadUFile(PUBLIC_KEY, PRIVATE_KEY, upload_suffix=SH2_UPLOAD_SUFFIX)
_, resp = mup_sh.uploadfile(BUCKET_SH2, 'python-sdk/examples/multipartput-key', UPLOAD_FILE_PATH)
assert resp.status_code == 200
