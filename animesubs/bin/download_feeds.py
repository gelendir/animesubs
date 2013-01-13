import argparse
import yaml
import logging
import os
from pprint import pprint

from animesubs import feeds, lib, download

logging.basicConfig(level=logging.INFO)

def all_files_recursively(path):
    fileset = set()
    for root, dirs, files in os.walk(path):
        for filename in files:
            fileset.add(filename.decode('utf8'))
    return fileset

def scan_directories(anime, directories):
    files = set()

    for directory in directories:
        files.update(all_files_recursively(directory))

    return lib.filter_missing(files, anime)

def main():

    parser = argparse.ArgumentParser(
        description="download torrent files from anime feeds")
    parser.add_argument("-s", "--scan", action="append",
        help="don't download torrents already downloaded in scanned directory "
             "(can be specified multiple times)")
    parser.add_argument("-l", "--latest-version", action='store_true',
        help="download only latest version of an episode (v2, v3, etc)")
    parser.add_argument("-c", "--config", default="config.yml",
        help="YAML config file (default: config.yml)")
    parser.add_argument("torrent_dir",
        help="torrent files will be downloaded here")

    args = parser.parse_args()

    with open(args.config) as configfile:
        config = yaml.load(configfile)

    anime = feeds.fetch_episodes_from_feeds(config)

    discarded = [a for a in anime if not 'anime' in a]
    anime = [a for a in anime if a not in discarded]

    if args.latest_version:
        anime = feeds.filter_episode_versions(anime)

    if args.scan:
        anime = scan_directories(anime, args.scan)

    download.download_torrents(anime, args.torrent_dir)

    if len(discarded) > 0:
        print "the following entries could not be processed:"
        pprint(discarded)

if __name__ == "__main__":
    main()

