import os

from battleship.model.coordinates import Plane
from battleship.model.battlefield import Ship, Battlefield
from battleship.model.battlelog import BattleLog
from battleship.view.battlefield_representation import BattlefieldRepresentation
from battleship.view.hitmap_representation import HitmapRepresentation


def main():
    bf = Battlefield(Plane((3, 3), ("A", 1)))
    bf.add_ship(Ship(
        position=('A', 1),
        orientation=Ship.Orientation.HORIZONTAL,
        length=2,
    ))
    bf_repr = BattlefieldRepresentation(bf)
    print(bf_repr.get_representation(os.get_terminal_size()[0]))
    print('=' * 20)
    bl = BattleLog({"test": bf})
    bl.make_move(("A", 2))
    bl.make_move(("B", 1))
    hm_repr = HitmapRepresentation(bl.hitmaps["test"]) + HitmapRepresentation(bl.hitmaps["test"], True)
    print(hm_repr.get_representation(os.get_terminal_size()[0]))


if __name__ == '__main__':
    main()
