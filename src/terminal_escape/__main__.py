import argparse
import inspect
import sys
import time
from typing import Callable


def sleep_and_flush(*fns: Callable[[], None]) -> None:
    for fn in fns:
        fn()
        sys.stderr.flush()
        time.sleep(1)



def main_1(args: argparse.Namespace) -> None:
    print('main_1', file=sys.stderr)


def main_2(args: argparse.Namespace) -> None:
    '''
    1234567890
              ^
        ^  (5 from the beginning of the line)
    '''
    sleep_and_flush(
        lambda: print('1234567890', end='', file=sys.stderr),
        lambda: print('\033[5G', end='', file=sys.stderr),
        lambda: print('\033[K', end='', file=sys.stderr),
    )
    print('', file=sys.stderr)


def main_3(args: argparse.Namespace) -> None:
    for i in range(11):
        for j in range(10):
            v = i * 10 + j
            print(f'\033[{v}m{v:03}\033[0m ', end='')
        print()


def main_4(args: argparse.Namespace) -> None:
    for i in range(16):
        for j in range(16):
            v = i * 16 + j
            print(f'\033[38;5;{v}m{v:03}\033[0m ', end='')
        print()


def main_5(args: argparse.Namespace) -> None:
    for i in range(16):
        for j in range(16):
            v = i * 16 + j
            print(f'\033[48;5;{v}m{v:03}\033[0m ', end='')
        print()


def main_6(args: argparse.Namespace) -> None:
    for i in range(16):
        for j in range(32):
            print(f'\033[32;2;{i<<4};{j<<3};255mX', end='')
        print('\033[0m')


def main_7(args: argparse.Namespace) -> None:
    for i in range(101):
        print(f'\r[{i:3} / 100]', end='', file=sys.stderr)
        time.sleep(0.1)
    print('\nfinish!', file=sys.stderr)


def main_8(args: argparse.Namespace) -> None:
    print('0%       50%       100%', file=sys.stderr)
    print('|---------+---------|', file=sys.stderr)
    for i in range(101):
        for _ in range(i//5 + 1):
            print('#', end='', file=sys.stderr, flush=True)
        print('', file=sys.stderr)
        print(f'{i:3}%', file=sys.stderr)
        time.sleep(0.1)
        print('\033[2A', end='', file=sys.stderr, flush=True)
    print('\nfinish!', file=sys.stderr)


def list_main_functions() -> list[str]:
    fns = inspect.getmembers(sys.modules[__name__], inspect.isfunction)
    return list(elm[0] for elm in fns if elm[0].startswith('main_'))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('main', choices=list_main_functions())
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    getattr(sys.modules[__name__], args.main)(args)
