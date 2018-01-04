#!/usr/bin/env python3
import re
import argparse
import subprocess


def main():
    argparser = argparse.ArgumentParser(description='Filter files from fdupes log by size')
    argparser.add_argument('--size', '-s', type=str, default='10mb')
    argparser.add_argument('--log', '-l', type=str, default='log.txt')
    args = argparser.parse_args()
    minsize = convert_size(args.size)
    number_reg = re.compile('^(\d+) bytes', re.IGNORECASE)
    with open(args.log, 'r') as fh:
        size = 0
        for line in fh:
            m = number_reg.match(line)
            if m:
                size = int(m.group(1))
            else:
                files = re.split('(?<!\\\) ', line.strip())
                files = [f.replace('\\', '') for f in files]
                if size > minsize:
                    print('size:', human_readable(size))
                    for n, f in enumerate(files):
                        print('{}.) {}'.format(n + 1, f))
                    answer = input('Which to keep?:')
                    try:
                        answer = int(answer)
                        files = files[:answer - 1] + files[answer:]
                    except ValueError:
                        if answer == 'all' or answer == '':
                            continue
                    for f in files:
                        subprocess.run(['trash-put', f])


def convert_size(input):
    KB = 1024
    units = {
        'KB': float(KB),
        'MB': float(KB ** 2),
        'GB': float(KB ** 3),
        'TB': float(KB ** 4),
    }
    m = re.match('(?P<number>\d+(?:\.\d+)?) ?(?P<unit>\w+)', input)
    number = float(m.group('number'))
    unit = m.group('unit')
    return number * units[unit.upper()]


def human_readable(B):
    'Return the given bytes as a human friendly KB, MB, GB, or TB string'
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)
    GB = float(KB ** 3)
    TB = float(KB ** 4)

    if B < KB:
        return '{0} {1}'.format(B, 'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        return '{0:.2f} KB'.format(B / KB)
    elif MB <= B < GB:
        return '{0:.2f} MB'.format(B / MB)
    elif GB <= B < TB:
        return '{0:.2f} GB'.format(B / GB)
    elif TB <= B:
        return '{0:.2f} TB'.format(B / TB)

if __name__ == '__main__':
    main()
