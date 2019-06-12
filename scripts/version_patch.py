#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""update version."""


def main():
    """Update version."""
    version = open('deepdialog/version.txt', 'r').read().strip()
    a, b, c = [int(x) for x in version.split('.')]
    c += 1
    new_version = '{}.{}.{}'.format(a, b, c)
    print('shipped:', new_version)
    with open('deepdialog/version.txt', 'w') as fp:
        fp.write(new_version)


if __name__ == '__main__':
    main()
