#!/usr/bin/python3

from bot import Bot


def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    main()
else:
    raise ImportError("Run this file directly, don't import it!")
