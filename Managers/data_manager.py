import boto3
from botocore.exceptions import ClientError


class SessionDataManager:
    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('Gold')

    def update_gold(self, user, gold_earned):
        name = str(user)
        try:
            self.table.update_item(
                Key = {'username': name},
                UpdateExpression = 'SET gold = gold + :val',
                ExpressionAttributeValues = {':val': gold_earned}
            )
        except ClientError:
            self.table.put_item(
                Item = {
                    'username': name,
                    'gold': gold_earned
                }
            )

    def get_gold(self, user):
        name = str(user)

        try:
            response = self.table.get_item(Key={'username': name})
            item = response['Item']
            if item is not None:
                return item['gold']
        except KeyError:
            return 0
