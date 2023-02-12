from dataclasses import dataclass, field
from typing import Tuple, Dict
from pathlib import Path

from battleship.model.coordinates import Coordinates


@dataclass
class Settings:
    field_size: Tuple[int, int] = (10, 10)
    axes_offset: Coordinates = ('A', 1)
    ships_count: Dict[int, int] = field(
        default_factory=lambda: {
            1: 2,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
        }
    )
    logs_path: Path = field(default_factory=lambda: Path.home().joinpath(".battleship"))
