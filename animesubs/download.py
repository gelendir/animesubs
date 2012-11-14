import urllib
import logging
import os
from pprint import pformat

logger = logging.getLogger(__name__)

def determine_filename(resp):
    disposition = resp.info().get('Content-Disposition')
    if disposition:
        parts = [x for x in disposition.split("; ") if x.startswith("filename")]
        if len(parts) > 0:
            filename = parts[0].replace("filename=", "").strip('"')
            return filename

    return None

def download_torrents(anime, outdir):
    for entry in anime:

        logger.info(u"downloading %s %s", entry['anime'], entry['episode'])

        resp = urllib.urlopen(entry['torrent_url'])

        default_filename = u"{0}.torrent".format(entry['filename'])
        filename = determine_filename(resp) or default_filename
        filepath = os.path.join(outdir, filename)

        with open(filepath, 'wb') as torrentfile:
            torrentfile.write(resp.read())


