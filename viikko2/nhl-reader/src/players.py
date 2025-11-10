from .player_reader import PlayerReader
from .player_stats import PlayerStats
from rich.console import Console
from rich.table import Table
from rich import box

def main():
    console = Console()
    while True:
        season = input("Enter season (for example, 2024-25), or 'exit' to quit: ")
        if season.lower() == 'exit':
            break
        nationality = input("Enter nationality (for example, FIN), or 'exit' to quit: ")
        if nationality.lower() == 'exit':
            break

        url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
        reader = PlayerReader(url)
        stats = PlayerStats(reader)
        players = stats.top_scorers_by_nationality(nationality)
        print(f"Players from {nationality} in season {season}:")

        table = Table(title=f"Top Scorers from {nationality} ({season})", box=box.ROUNDED)
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Team", style="magenta")
        table.add_column("Goals", justify="right", style="green")
        table.add_column("Assists", justify="right", style="blue")
        table.add_column("Points", justify="right", style="yellow")
        table.add_column("Games", justify="right", style="red")

        for player in players:
            points = player.goals + player.assists
            table.add_row(
                player.name,
                player.team,
                str(player.goals),
                str(player.assists),
                str(points),
                str(player.games)
            )

        console.print(table)

if __name__ == "__main__":
    main()