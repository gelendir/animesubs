import argparse
import yaml
import logging
import os

from animesubs import feeds, lib, download

logging.basicConfig(level=logging.INFO)

def main():

    parser = argparse.ArgumentParser(
        description="download torrent files from anime feeds")
    parser.add_argument("--filescan", help="scan directory for existing files before downloading torrents")
    parser.add_argument("config", help="YAML config file")
    parser.add_argument("torrent_dir", help="torrent files will be downloaded here")

    args = parser.parse_args()

    with open(args.config) as configfile:
        config = yaml.load(configfile)

    anime = feeds.fetch_episodes_from_feeds(config)

    if args.filescan:
        files = [x.decode('utf8') for x in os.listdir(args.filescan)]
        anime = lib.filter_missing(files, anime)

    download.download_torrents(anime, args.torrent_dir)

if __name__ == "__main__":
    main()

