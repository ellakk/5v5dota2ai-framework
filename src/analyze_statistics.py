import csv
import json


# Just experimenting with the csv files that the statistics module is generating.

def load_statistics(filename: str):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        return list(reader)


def column_indices(column_names, *target_names) -> list[int]:
    return [i for i, name in enumerate(column_names) if name in target_names]


def main():
    filename = 'statistics/2021_12_10_15_36_40_game_stats_0.csv'
    stats = load_statistics(filename)
    indices = column_indices(stats[0],
                             '0_dmg_received_hero',
                             '1_dmg_received_hero',
                             '2_dmg_received_hero',
                             '3_dmg_received_hero',
                             '4_dmg_received_hero',
                             '5_dmg_received_hero',
                             '6_dmg_received_hero',
                             '7_dmg_received_hero',
                             '8_dmg_received_hero',
                             '9_dmg_received_hero'
                             )

    for row in stats:
        for i in indices:
            print(f"{row[i]}, ", end="")
        print("")


if __name__ == '__main__':
    with open('statistics/2021_12_17_16_51_14_game_state_dire_0.json') as fp:
        raw = fp.read()

    state = json.loads(raw)

