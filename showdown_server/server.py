import asyncio
from poke_env.player import RandomPlayer
from teambuilder.custom_team_builder import CustomTeamBuilder
from showdown_server.teams import team_1

async def main():
    print("Starting battle...")
    custom_builder = CustomTeamBuilder(team_1)

    player_1 = RandomPlayer(
        battle_format="gen8anythinggoes",
        max_concurrent_battles=1,
        team=custom_builder
    )
    player_2 = RandomPlayer(
        battle_format="gen8anythinggoes",
        max_concurrent_battles=1,
        team=custom_builder
    )

    await player_1.battle_against(player_2, n_battles=1)

    print(f"Finished battles: {player_1.n_finished_battles}")
    print(f"Player 1 wins: {player_1.n_won_battles}")


if __name__ == "__main__":
    asyncio.run(main())