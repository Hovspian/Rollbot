import os

import asyncio

import math
from dataIO import js


class LocalDataManager:
    def __init__(self, bot):
        self.bot = bot
        self.data_handler = PersistentDataHandler()
        self.players = self.data_handler.get_data()
        self.__initialize_rollbot()

    def single_transfer(self, to_user, gold_difference, from_user):
        self.__transfer_gold(to_user, gold_difference, from_user)
        self.__save_data()

    def batch_transfer(self, payouts: dict):
        for payout in payouts:
            self.__transfer_gold(payout['to_user'],
                                 payout['gold_difference'],
                                 payout['from_user'])
        self.__save_data()

    def get_gold(self, user) -> int:
        """
        How much gold a user has.
        """
        if user.id in self.players:
            return self.players[user.id]['gold']

    def get_gold_stats(self, user) -> dict:
        """
        Gold won from/lost to other users on the profile.
        """
        user_id = self.players[user.id]
        if user_id is not None:
            return self.players[user.id]['gold_stats']

    def __transfer_gold(self, to_user, gold_difference, from_user):
        """
        How much total gold has been transferred between two users.
        """
        self.__create_profile_if_not_exists(to_user)
        self.__create_profile_if_not_exists(from_user)
        amount = self.__get_final_gold_difference(to_user, gold_difference, from_user)
        self.__update(to_user, amount, from_user)

    def __update(self, to_user, amount, from_user):
        self.__update_gold(to_user, amount)
        self.__update_gold_stats(to_user, amount, from_user)
        # Apply the reverse for from_user
        self.__update_gold(from_user, -amount)
        self.__update_gold_stats(from_user, -amount, to_user)

    def __update_gold(self, user, amount) -> None:
        self.players[user.id]['gold'] += amount

    def __get_final_gold_difference(self, to_user, gold_difference, from_user) -> int:
        """
        When transferring gold, users can't lose more gold than they have.
        """
        first_user = self.players[to_user.id]
        second_user = self.players[from_user.id]

        if first_user['gold'] + gold_difference < 0:
            return first_user['gold']
        elif second_user['gold'] + gold_difference < 0:
            return second_user['gold']
        else:
            return gold_difference

    def __initialize_rollbot(self) -> None:
        """
        Rollbot can't run out of gold.
        """
        self.__create_profile_if_not_exists(self.bot.user)
        self.players[self.bot.user.id]['gold'] = math.inf

    def __update_gold_stats(self, to_user, amount, from_user) -> None:
        self.__create_gold_stat_if_not_exists(to_user, from_user)
        self.players[to_user.id]['gold_stats'][from_user.id]['gold'] += amount

    def __create_profile_if_not_exists(self, user) -> None:
        if user.id in self.players:
            return
        self.players[user.id] = self.__get_default_profile()

    def __create_gold_stat_if_not_exists(self, user_one, user_two) -> None:
        """
        Create a statistic for tracking gold won/lost from another user.
        """
        user_one_stats = self.players[user_one.id]['gold_stats']
        if user_two.id in user_one_stats:
            return
        user_one_stats[user_two.id] = {'gold': 0,
                                       'name': user_two.display_name}

    def __save_data(self):
        self.players[self.bot.user.id]['gold'] = 0  # Infinity isn't valid JSON, so set Rollbot's gold to 0.
        self.data_handler.save_data(self.players)
        self.players[self.bot.user.id]['gold'] = math.inf

    @staticmethod
    def __get_default_profile() -> dict:
        return {'gold': 0,
                'gold_stats': {},  # Key: from_user.id, value: dict
                'butts': {}  # TODO dunno what goes in here yet
                }


class PersistentDataHandler:

    def __init__(self):
        self.file_path = "Data/player_data.json"
        self.folder_path = "Data"
        self.__check_folder()
        self.__check_file()

    def save_data(self, player_data):
        js.safe_dump(player_data, self.file_path)

    def get_data(self):
        return js.load(self.file_path)

    def __check_folder(self):
        if not os.path.exists(self.folder_path):
            print("Creating Data folder for player data.")
            os.makedirs("Data")

    def __check_file(self):
        default = {}
        if not js.load(self.file_path):
            print("Creating JSON file for record-keeping.")
            self.save_data(default)
