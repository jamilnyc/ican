import sys

sys.path.append('../src/api')
from s3 import S3


s = S3()

link = s.uploadData('/tmp/trash.jpg');
print link