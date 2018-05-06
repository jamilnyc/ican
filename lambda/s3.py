import boto3
from botocore.exceptions import ClientError


class S3Service:
    """
    Class that abstracts the S3 interface allowing uploading of files.

    Public Methods:
        uploadData()
    """

    S3 = None
    S3_BUCKET_NAME = 'iot-ican'
    S3Bucket = None

    def __init__(self):
        self.S3 = boto3.resource('s3', region_name='us-east-1')

    def bucketExists(self):
        """
        Return whether or not the S3 bucket currently exists.
        :return: Boolean of whether or not the S3 bucket exists
        """
        try:
            # Get S3 bucket related details
            self.S3.meta.client.head_bucket(Bucket=self.S3_BUCKET_NAME)
            return True
        except ClientError:
            return False

    def uploadData(self, data, fileName):
        """
        Create an S3 bucket if needed and upload the given file to it.
        :param filePath: Absolute path to the file as a string
        :return: The public URL to the file on S3 as a string
        """
        # if the given bucket exist get the bucket or create one
        if self.bucketExists():
            self.S3Bucket = self.S3.Bucket(self.S3_BUCKET_NAME)
        else:
            self.S3Bucket = self.S3.create_bucket(Bucket=self.S3_BUCKET_NAME)

        # Upload data to S3
        return self.uploadToS3(data, fileName)

    def uploadToS3(self, data, fileName):
        """
        Write the given file to the S3 bucket as a publicly readable object.
        :param data: The file data to write
        :param fileName: Name of object when stored in S3
        :return: The public URL to the object as a string
        """
        self.S3Bucket.Object(fileName).put(Body=data, ACL='public-read')
        return self.getPublicLink(fileName)

    def getPublicLink(self, fileName):
        """
        Get the public URL to an object in S3, given its filename.
        :param fileName: filename with extension of S3 object
        :return: string URL
        """
        objectUrl = "https://s3.amazonaws.com/{0}/{1}".format(
            self.S3_BUCKET_NAME,
            fileName)
        return objectUrl
