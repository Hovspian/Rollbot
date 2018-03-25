import boto3
from botocore.exceptions import ClientError

from Managers.user_profile import get_default_profile


class RemoteDataManager:
    def __init__(self, bot):
        self.gold_manager = GoldManager(bot)

    def batch_transfer(self, payouts: dict):
        for payout in payouts:
            self.gold_manager.transfer_gold(payout['to_user'],
                                            payout['amount'],
                                            payout['from_user'])

    def single_transfer(self, to_user, amount, from_user):
        if self.is_valid_transfer(to_user, from_user):
            self.gold_manager.transfer_gold(to_user, amount, from_user)

    def get_gold(self, user):
        return self.gold_manager.get_gold(user)

    def get_gold_stats(self, user):
        return self.gold_manager.get_gold_stats(user)

    @staticmethod
    def is_valid_transfer(to_user, from_user) -> bool:
        return to_user.id != from_user.id


class GoldManager:
    def __init__(self, bot):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('RollbotGold')
        self.old_table = dynamodb.Table('Gold')
        self.bot = bot
        self.__refresh_rollbot()

    def transfer_gold(self, to_user, amount, from_user):
        final_amount = self.__get_final_gold_amount(amount, from_user)
        self.__update_gold(to_user, final_amount)
        self.__update_gold(from_user, -final_amount)  # Subtract from the giver
        self.__update_gold_stats(to_user, final_amount, from_user)

    def get_gold(self, user):
        try:
            response = self.table.get_item(Key={'id': user.id})
            item = response['Item']
            if item is not None:
                return item['gold']
        except KeyError:
            return 0

    def get_gold_stats(self, user) -> dict or None:
        try:
            response = self.table.get_item(Key={'id': user.id})
            item = response['Item']
            if item is not None:
                return item['gold_stats']
        except KeyError:
            return None

    def __refresh_rollbot(self):
        try:
            self.table.update_item(
                Key={'id': self.bot.user.id},
                UpdateExpression='SET gold = :val',
                ExpressionAttributeValues={':val': 1000000}
            )
        except ClientError:
            self.create_profile(self.bot.user, 1000000)

    def __get_final_gold_amount(self, amount, from_user) -> int:
        """
        When transferring gold, users can't lose more gold than they have.
        """
        gold = self.get_gold(from_user)

        if not gold:
            return 0
        elif gold - amount < 0:
            return gold
        else:
            return amount

    def __update_gold(self, user, amount):
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

    def __update_gold_stats(self, to_user, amount, from_user):
        try:
            self.__update_win(to_user, amount, from_user)
            self.__update_loss(to_user, amount, from_user)
        except ClientError:
            self.__create_win_stat(to_user, amount, from_user)
            self.__create_lose_stat(to_user, amount, from_user)

    def __update_win(self, to_user, amount, from_user):
        self.table.update_item(
            Key={'id': to_user.id},
            UpdateExpression='SET #gs.#id.#total = #gs.#id.#total + :val,'
                             '#gs.#id.won = #gs.#id.won + :val',

            ExpressionAttributeNames={'#gs': 'gold_stats',
                                      '#id': from_user.id,
                                      '#total': 'total'},

            ExpressionAttributeValues={':val': amount}
        )

    def __update_loss(self, to_user, amount, from_user):
        self.table.update_item(
            Key={'id': from_user.id},
            UpdateExpression='SET #gs.#id.#total = #gs.#id.#total - :val,'
                             '#gs.#id.lost = #gs.#id.lost + :val',

            ExpressionAttributeNames={'#gs': 'gold_stats',
                                      '#id': to_user.id,
                                      '#total': 'total'},

            ExpressionAttributeValues={':val': amount}
        )

    def __create_win_stat(self, to_user, amount, from_user):
        self.table.update_item(
            Key={'id': to_user.id},
            UpdateExpression='SET #gs.#id = :gs',
            ExpressionAttributeNames={'#gs': 'gold_stats',
                                      '#id': from_user.id},
            ExpressionAttributeValues={
                ':gs': {'total': amount,
                        'won': amount,
                        'lost': 0}
            }
        )

    def __create_lose_stat(self, to_user, amount, from_user):
        self.table.update_item(
            Key={'id': from_user.id},
            UpdateExpression='SET #gs.#id = :gs',
            ExpressionAttributeNames={'#gs': 'gold_stats',
                                      '#id': to_user.id},
            ExpressionAttributeValues={
                ':gs': {'total': -amount,
                        'won': 0,
                        'lost': amount}
            }
        )


class MigrateTable:
    """
    Calling migrate() will delete all known users from the RollbotGold table and refill it with gold from the Gold table!
    """
    def __init__(self, bot, gold_manager):
        self.bot = bot
        self.gold_manager = gold_manager
        dynamodb = boto3.resource('dynamodb')
        self.new_table = dynamodb.Table('RollbotGold')
        self.old_table = dynamodb.Table('Gold')

    def reset_users(self):
        users = self.bot.get_all_members()
        for user in users:
            self.new_table.delete_item(Key={'id': user.id})
        print("Users deleted.")
        self.new_table.delete_item(Key={'id': self.bot.user.id})
        self.gold_manager.create_profile(self.bot.user, 1000000)
        print("Profile created for Rollbot.")

    def migrate(self):
        self.reset_users()
        users = self.bot.get_all_members()
        for user in users:
            old_gold = self.get_old_gold(user)
            if self.can_migrate(user):
                self.gold_manager.transfer_gold(user, old_gold, self.bot.user)
                print("Transferring", old_gold, "to", user)

    def can_migrate(self, user):
        old_gold = self.get_old_gold(user)
        new_gold = self.gold_manager.get_gold(user)
        return user != self.bot.user and \
               old_gold > 0 and \
               new_gold == 0

    def get_old_gold(self, user):
        name = str(user)
        try:
            response = self.old_table.get_item(Key={'username': name})
            item = response['Item']
            if item is not None:
                return item['gold']
        except KeyError:
            return 0