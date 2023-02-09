import os

from battleship.activity.main_activity import MainActivity


def main():
    main_activity = MainActivity()
    main_activity.run(os.get_terminal_size())


if __name__ == '__main__':
    main()
