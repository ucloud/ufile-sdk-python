import random
import string
from ufile.compact import *

def random_string(n):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(n))

def random_bytes(n):
    return b(random_string(n))