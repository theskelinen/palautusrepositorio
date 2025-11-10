import requests
from .player import Player

class PlayerReader:
    def __init__(self, url):
        self.url = url
        self.response = requests.get(self.url).json()
    
    def get_players(self):
        players = []
        for player_dict in self.response:
            player = Player(player_dict)
            players.append(player)
        return players