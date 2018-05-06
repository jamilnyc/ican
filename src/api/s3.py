import os

from botocore.exceptions import ClientError

import aws


class S3(object):
    """
    Cloud Storage service that communicates with the Amazon Simple Storage Service to upload objects.

    Public Methods:
        uploadData()
        getPublicLink()
    """

    # CONSTANTS
    S3 = None
    S3_BUCKET_NAME = 'iot-ican'
    S3Bucket = None

    def __init__(self):
        # Get s3 resource , function for this is in utils/aws
        self.S3 = aws.getResource('s3', 'us-east-1')

    def uploadData(self, filePath):
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
        return self.uploadToS3(filePath)

    def uploadToS3(self, filePath):
        """
        Write the given file to the S3 bucket as a publicly readable object.
        :param filePath: The absolute path to the file as a string
        :return: The public URL to the object as a string
        """
        with open(filePath, 'rb') as data:
            fileName = os.path.basename(filePath)
            self.S3Bucket.Object(fileName).put(Body=data, ACL='public-read')
            return self.getPublicLink(fileName)

    def getPublicLink(self, fileName):
        """
        Get the public URL to an object in S3, given its filename.
        :param fileName: filename with extension of S3 object
        :return: string URL
        """
        objectUrl = "https://s3.amazonaws.com/{1}/{2}".format(
            'us-east-1',  # TODO: acquire from the bucket
            self.S3_BUCKET_NAME,
            fileName)
        return objectUrl

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
