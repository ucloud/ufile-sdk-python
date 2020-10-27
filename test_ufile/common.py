import random
import string
from ufile.compact import *

PUBLIC_KEY = '<your public key>'              #添加自己的账户公钥
PRIVATE_KEY = '<your private key>'            #添加自己的账户私钥
PUBLIC_BUCKET = '<your public bucket name>'   #添加公共空间名称
PRIVATE_BUCKET = '<your private bucket name>' #添加私有空间名称

def random_string(n):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(n))

def random_bytes(n):
    return b(random_string(n))