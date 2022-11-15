from sys import exit
import argparse


def main():
    ap = argparse.ArgumentParser(prog="dotinstall")
    args, extras = ap.parse_known_args()


if __name__ == "__main__":
    exit(main())
