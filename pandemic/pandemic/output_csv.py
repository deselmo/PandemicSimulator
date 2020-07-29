import pandemic as pd
from typing import Sequence
import csv


def save_csv(path: str, data_epochs: Sequence[pd.DataEpoch]) -> bool:
    try:
        with open(path, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(pd.DataEpoch._fields)
            writer.writerows([data_epoch._asdict().values() for data_epoch in data_epochs])
    except Exception:
        return True

    return False


def print_csv(data_epochs: Sequence[pd.DataEpoch]) -> None:
    print(*pd.DataEpoch._fields)
    for data_epoch in data_epochs:
        print(*data_epoch._asdict().values())
