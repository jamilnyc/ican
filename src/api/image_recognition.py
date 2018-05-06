import aws


class ImageRecognition:
    """
    Image Recognition Service that describes images with Amazon Rekognition.

    Public Methods:
        getImageIdentifiers()
        getTextIdentifiers()
    """

    rek = None

    def __init__(self):
        self.rek = aws.getClient('rekognition', 'us-east-1')

    def getImageIdentifiers(self, filePath):
        """
        Return a list of identifiers from the Image Recognition Service of the given image (top 10 sorted by confidence).
        :param filePath: The absolute path to the image file, as a string
        :return: A string list of the top ten identifiers for the given image
        """
        with open(filePath, 'rb') as f:
            pic = f.read()
        res = self.rek.detect_labels(Image={"Bytes": pic})
        label = res["Labels"]
        label.sort(reverse=True, key=lambda x: x['Confidence'])
        labellst = []
        for item in label:
            if item != '':
                labellst.append(item["Name"])
        return labellst[:10]

    def getTextIdentifiers(self, filePath):
        """
        Return a list of the top ten pieces of text recognized in the given image, sorted by confidence.
        :param filePath: Absolute path to the image file as a string
        :return: String list of recognized text labels in the image, up to 10
        """
        with open(filePath, 'rb') as f:
            pic = f.read()
        res = self.rek.detect_text(Image={"Bytes": pic})
        text = res["TextDetections"]
        text.sort(reverse=True, key=lambda x: x['Confidence'])
        txt = []
        for item in text:
            if item != '' and item["DetectedText"].lower() not in txt:
                txt.append(item["DetectedText"].lower())
        return txt[:10]