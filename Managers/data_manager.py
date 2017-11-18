import os
from dataIO import js


class SessionDataManager:
    def __init__(self):
        # Save the running session gold etc.
        self.data_handler = PersistentDataHandler()
        self.players = self.data_handler.get_data()

    def update_gold(self, user, gold_earned):
        name = str(user)
        if name not in self.players:
            print("Creating a new gold storage for", name)
            self.players[name] = {'gold': 0}
        self.players[name]['gold'] += gold_earned
        self.update_data()

    def update_data(self):
        self.data_handler.save_data(self.players)

    def get_gold(self, user):
        name = str(user)
        if name in self.players:
            return self.players[name]['gold']


class PersistentDataHandler:
    def __init__(self):
        # Updates a member object with gold gained and writes it into a file. All games should do this.
        self.file_path = "Data/player_data.json"
        self.folder_path = "Data"
        self.check_folder()
        self.check_file()

    def check_folder(self):
        if not os.path.exists(self.folder_path):
            print("Creating Data folder for player data.")
            os.makedirs("Data")

    def check_file(self):
        default = {}
        if not js.load(self.file_path):
            print("Creating JSON file for record-keeping.")
            self.save_data(default)

    def save_data(self, data):
        js.safe_dump(data, self.file_path)

    def get_data(self):
        return js.load(self.file_path)