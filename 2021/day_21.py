import functools
from collections import Counter
from itertools import product
from pathlib import Path
from typing import NamedTuple


class GameState(NamedTuple):
    positions: tuple[int, int]
    scores: tuple[int, int]
    p2_next: bool


class Die:
    def __init__(self):
        self.next_roll = 1
        self.rolls = 0

    def roll(self) -> int:
        self.rolls += 1
        roll = self.next_roll
        self.next_roll += 1
        if self.next_roll > 100:
            self.next_roll = 1
        return roll


class Game:
    def __init__(self, player_1: int, player_2: int):
        self.positions = {1: player_1, 2: player_2}
        self.scores = {1: 0, 2: 0}
        self._next_player = 0
        self._die = Die()

    def _get_player(self) -> int:
        player = self._next_player + 1
        self._next_player = not self._next_player
        return player

    def do_turn(self) -> bool:
        player = self._get_player()
        move = sum(self._die.roll() for _ in range(3))

        new_position = (self.positions[player] + move) % 10 or 10
        self.positions[player] = new_position
        self.scores[player] += new_position
        return self.scores[player] >= 1000

    def play_game(self) -> int:
        player_won = False
        while not player_won:
            player_won = self.do_turn()
        return min(self.scores.values()) * self._die.rolls


ROLLS: dict[int, int] = dict(Counter(map(sum, product(range(1, 4), repeat=3))).items())


@functools.cache
def take_turn(state: GameState) -> dict[int, int]:
    wins = {0: 0, 1: 0}
    for move, count in ROLLS.items():
        player = int(state.p2_next)
        position = (state.positions[player] + move) % 10 or 10
        score = state.scores[player] + position
        if score >= 21:
            turn_wins = {player: 1}
        else:
            turn_wins = take_turn(
                GameState(
                    (
                        position if player == 0 else state.positions[0],
                        position if player == 1 else state.positions[1],
                    ),
                    (
                        score if player == 0 else state.scores[0],
                        score if player == 1 else state.scores[1],
                    ),
                    not state.p2_next,
                )
            )
        for player, win_count in turn_wins.items():
            wins[player] += win_count * count
    return wins


def main():
    with Path(__file__).parent.joinpath("day_21-input.txt").open("r") as input_f:
        player_1 = int(input_f.readline().split(":", 1)[1])
        player_2 = int(input_f.readline().split(":", 1)[1])
        game = Game(player_1, player_2)

    print("Part1: ", game.play_game())
    print(
        "Part2: ",
        max(take_turn(GameState((player_1, player_2), (0, 0), False)).values()),
    )


if __name__ == "__main__":
    main()
