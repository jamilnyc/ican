import json

import aws


class ICanItems:
    """
    Database service that creates a DynamoDB table and allows uploading of records.

    Public Methods:
        addRecord()
    """

    # CONSTANTS
    TABLE_NAME = 'iCanItems'

    def __init__(self):
        """
        Acquires a DynamoDB resource and creates the table if it doesn't already exist.
        """
        self.dynamodb = aws.getResource('dynamodb', 'us-east-1')
        self.table = None
        self.createTable()

    def createTable(self):
        """
        Create the table in DynamoDB if it doesn't already exist and set the reference.
        :return: None
        """
        print 'Creating table ' + self.TABLE_NAME
        try:
            table = self.dynamodb.create_table(
                TableName=self.TABLE_NAME,
                KeySchema=[
                    {
                        'AttributeName': 'timestamp',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'timestamp',
                        'AttributeType': 'N'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            table.meta.client.get_waiter('table_exists').wait(TableName=self.TABLE_NAME)
        except Exception as e:
            # print e.message
            print 'Table already exists, not creating again.'

        self.table = self.dynamodb.Table(self.TABLE_NAME)

    def addRecord(self, record):
        """
        Add the given record to the DynamoDB table and print the response.
        :param record: Dictionary of column values
        :return: Response to save request from database
        """
        print 'Adding record to table ' + self.TABLE_NAME
        response = self.table.put_item(
            Item=record
        )
        return json.dumps(response, indent=4)

