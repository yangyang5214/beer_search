from scrapy.cmdline import execute

import sys
import os
import argparse


def main(args):
    if not args.name:
        return
    params = ['scrapy', 'crawl', args.name]
    if args.url:
        params.append('-a')
        params.append('prod_url={}'.format(args.url))
    execute(params)
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-u', '--url', type=str, help='prod url link')
    ap.add_argument('-n', '--name', type=str, help='spider name')
    args = ap.parse_args()
    main(args)
