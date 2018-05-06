from __future__ import print_function

import boto3
from boto3.dynamodb.conditions import Key


class DynamoService:
    """
    Class to abstract functions to read data from DynamoDB

    Public Methods:
        getItemIdentifiersAfterTimestamp()
    """
    dynamodb = None
    table = None
    
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = self.dynamodb.Table('iCanItems')
        
    def getItemsAfterTimestamp(self, ts):
        """
        Return all records with a timestamp field value greater than the given timestamp.

        :param ts: UNIX timestamp integer
        :return: DynamoDB response items list
        """
        fe = Key('timestamp').gt(ts)
        response = self.table.scan(FilterExpression=fe)
        return response['Items']
        
    def getItemIdentifiersAfterTimestamp(self, ts):
        """
        Return a list of all identifiers for items in the database older than the given timestamp.

        :param ts: UNIX timestamp integer
        :return: list of identifiers (each is a list of strings)
        """
        items = self.getItemsAfterTimestamp(ts)
        identifiers = []
        for item in items:
            # Convert the comma separated string of names to a list of strings
            names = item['item_name'].split(',')
            names = [name.strip() for name in names]
            identifiers.append(names)

        return identifiers
