#!/usr/bin/python3

from sys import stderr, stdin


def main():
    while True:
        try:
            line = input()
        except EOFError:
            break
        parts = line.split(" ")
        if parts[0] == "settings":
            print("no_moves")
        elif parts[0] == "update":
            print("no_moves")
        elif parts[0] == "action":
            print("buy USDT_ETH 0.01")


if __name__ == "__main__":
    main()
