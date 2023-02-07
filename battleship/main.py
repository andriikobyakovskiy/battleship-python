from battleship.model.battlefield import Ship


def main():
    ship = Ship(
        position=(1, 'A'),
        orientation=Ship.Orientation.HORIZONTAL,
        length=2,
    )
    print(ship)


if __name__ == '__main__':
    main()
