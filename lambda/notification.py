import boto3


class Notification:
    """
    Service that communicates with Amazon Simple Notification Service (SNS) to deliver messages to subscribers.

    Public Methods:
        sendNotification()
        setTopic()
    """

    topicName = 'iCanAlerts'
    topicArn = None
    snsClient = None

    def __init__(self):
        self.snsClient = boto3.client('sns', 'us-east-1')
        self.setTopic(self.topicName)

    def setTopic(self, topicName):
        """
        Set the current notification Topic to publish to.
        :param topicName: Name of the topic (string)
        :return: None
        """
        self.topicName = topicName
        topicResponse = self.snsClient.create_topic(Name=topicName)
        self.topicArn = topicResponse['TopicArn']

    def sendNotification(self, message):
        """
        Send the notification to all subscribers of the topic.
        :param message: Message string to send to subscribers
        :return: None
        """
        if self.topicArn is None:
            print 'ERROR: Notification topic not set!'
            return

        publishResponse = self.snsClient.publish(
            TopicArn=self.topicArn,
            Message=message
        )
