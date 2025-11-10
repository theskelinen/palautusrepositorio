import requests
from .player import Player

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    response = requests.get(url).json()

    players = []
    nationality = "FIN"

    for player_dict in response:
        player = Player(player_dict)
        if player.nationality == nationality:
            players.append(player)
    
    sorted_players = sorted(players, key=lambda p: p.points, reverse=True)

    print(f"Players from {nationality}:")

    for player in sorted_players:
        print(player)

if __name__ == "__main__":
    main()