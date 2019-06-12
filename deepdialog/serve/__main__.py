# -*- coding: utf-8 -*-
"""Serve entrace."""

from .serve import Serve


def main(model_path, outside_function={}):
    """Serve entrace."""
    return Serve(model_path, outside_function)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Test DeepDialog Model in console')
    parser.add_argument(
        'model_dir', type=str)
    args = parser.parse_args()
    s = main(args.model_dir)
    while True:
        utterance = input('user:')
        if utterance.lower() in ('quit', 'exit'):
            exit(0)
        sys_response = s(utterance)
        print('sys:', sys_response)
