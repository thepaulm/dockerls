#!/usr/bin/env python

import argparse
import json
import urllib.request


def paginated(base_url, key):
    url = base_url
    while True:
        with urllib.request.urlopen(url) as res:
            msg = res.readall()
            reps = json.loads(msg.decode())[key]
            for r in reps:
                print(r)

            if 'Link' not in [hn for hn, _ in res.getheaders()]:
                break

            url = base_url + '?last=' + reps[-1]


def registry_ls(registry):
    paginated(base_url='http://' + registry + '/v2/_catalog',
              key='repositories')


def tags_ls(registry, image):
    paginated(base_url='http://' + registry + '/v2/' + image + '/tags/list',
              key='tags')


def main():
    p = argparse.ArgumentParser(
        description='tool to inspect docker registries')
    p.add_argument('registry', help="docker registry")
    p.add_argument('--tags', help="show tags for this image")
    args = p.parse_args()

    if args.tags is None:
        registry_ls(args.registry)
    else:
        tags_ls(args.registry, args.tags)


if __name__ == '__main__':
    main()
