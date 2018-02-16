import boto3
from botocore.exceptions import ClientError

from Managers.user_profile import get_default_profile


class RemoteDataManager:
    def __init__(self, bot):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('RollbotGold')
        self.bot = bot
        self.refresh_rollbot()

    def refresh_rollbot(self):
        try:
            self.table.update_item(
                Key={'id': self.bot.user.id},
                UpdateExpression='SET gold = :val',
                ExpressionAttributeValues={':val': 1000000}
            )
        except ClientError:
            self.create_profile(self.bot.user, 1000000)

    def batch_transfer(self, payouts: dict):
        for payout in payouts:
            self.__transfer_gold(payout['to_user'],
                                 payout['gold_difference'],
                                 payout['from_user'])

    def single_transfer(self, to_user, amount, from_user):
        self.__transfer_gold(to_user, amount, from_user)

    def __get_final_gold_difference(self, gold_difference, from_user) -> int:
        """
        When transferring gold, users can't lose more gold than they have.
        """
        gold = self.get_gold(from_user)

        if not gold:
            return 0
        elif gold - gold_difference < 0:
            return gold
        else:
            return gold_difference

    def __transfer_gold(self, to_user, amount, from_user):
        final_amount = self.__get_final_gold_difference(amount, from_user)
        self.update_gold(to_user, final_amount)
        self.update_gold(from_user, -final_amount)  # Subtract from the giver
        self.update_gold_stats(to_user, final_amount, from_user)

    def update_gold(self, user, amount):
        try:
            self.table.update_item(
                Key={'id': user.id},
                UpdateExpression='SET gold = gold + :val',
                ExpressionAttributeValues={':val': amount}
            )
        except ClientError:
            self.create_profile(user, amount)

    def create_profile(self, user, amount):
        self.table.put_item(
            Item=get_default_profile(user, amount)
        )

    def update_gold_stats(self, to_user, amount, from_user):
        try:
            self.update_win(to_user, amount, from_user)
            self.update_loss(to_user, amount, from_user)
        except ClientError:
            self.create_gold_stat(to_user, amount, from_user)

    def update_win(self, to_user, amount, from_user):
        self.table.update_item(
            Key={'id': to_user.id},
            UpdateExpression='SET #gs.#id.#total = #gs.#id.#total + :val,'
                             '#gs.#id.won = #gs.#id.won + :val',
            ExpressionAttributeNames={'#gs': 'gold_stats',
                                      '#id': from_user.id,
                                      '#total': 'total'},
            ExpressionAttributeValues={':val': amount}
        )

    def update_loss(self, to_user, amount, from_user):
        self.table.update_item(
            Key={'id': from_user.id},
            UpdateExpression='SET #gs.#id.#total = #gs.#id.#total - :val,'
                             '#gs.#id.lost = #gs.#id.lost - :val',
            ExpressionAttributeNames={'#gs': 'gold_stats',
                                      '#id': to_user.id,
                                      '#total': '#total'},
            ExpressionAttributeValues={':val': amount}
        )

    def create_gold_stat(self, to_user, amount, from_user):
        self.create_win_stat(to_user, amount, from_user)
        self.create_lose_stat(to_user, amount, from_user)

    def create_win_stat(self, to_user, amount, from_user):
        self.table.update_item(
            Key={'id': to_user.id},
            UpdateExpression='SET #gs.#id = :gs',
            ExpressionAttributeNames={'#gs': 'gold_stats',
                                      '#id': from_user.id},
            ExpressionAttributeValues={
                ':gs': {'total': amount,
                        'won': amount,
                        'lost': 0},
            }
        )

    def create_lose_stat(self, to_user, amount, from_user):

        self.table.update_item(
            Key={'id': from_user.id},
            UpdateExpression=f'SET #gs.#id = :gs',
            ExpressionAttributeNames={'#gs': 'gold_stats',
                                      '#id': to_user.id},
            ExpressionAttributeValues={
                ':gs': {'total': 0,
                        'won': 0,
                        'lost': -amount}
            }
        )

    def get_gold(self, user):
        try:
            response = self.table.get_item(Key={'id': user.id})
            item = response['Item']
            if item is not None:
                return item['gold']
        except KeyError:
            return 0
