from battleship.activity.activity import Activity
from battleship.activity.game_stage import GameStage


class ScoreboardActivity(Activity):

    def __init__(self, data: list):
        self._scores = [
            {
                key: data["score"]
                for key, data in record.items()
                if key != "moves"
            }
            for record in data
        ]

    def run(self, console_width: int) -> (object, GameStage):
        self.clean_console()
        print("TOP 10 SCORES:")
        print("=" * 20)
        sorted_records = sorted(
            self._scores,
            key=lambda r: max(*(r.values())),
            reverse=True,
        )
        for record in sorted_records[:10]:
            winner, loser = list(sorted(
                record.keys(),
                key=lambda player: record[player],
                reverse=True,
            ))
            print(f"{winner} (vs {loser}): {record[winner]}")
        print("=" * 20)
        input("Press enter to return to menu...")

        return None, GameStage.START_MENU
