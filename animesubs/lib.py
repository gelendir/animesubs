import re

REGEX = re.compile(
    r"""^
    \[(?P<subber>.*?)\]             # Subber group
    (?P<anime>.*?)                  # Anime name
    [ _]-[ _]
    (?P<episode>\d+(\.\d+)?)        # Episode
    (v(?P<version>\d+))?            # version
    [ _]?
    (?P<additional>(\[.*?\])*?)     # Other info encapsulated in []
    (\[(?P<crc32>[A-Z\d]{8})\])?    # CRC32 Hash
    \.(?P<extension>mkv|avi|mp4)    # File extension
    """,
    re.IGNORECASE | re.UNICODE | re.VERBOSE
)

RESOLUTION = re.compile("(\d+p)")

def info_from_filename(filename):

    info = {}

    match = REGEX.match(filename)
    if match:
        groups = match.groupdict()
        info.update({
            'subber'    : groups['subber'].strip(),
            'anime'     : groups['anime'].replace("_", " ").strip(),
            'extension' : groups['extension'],
        })

        episode = groups['episode']
        if '.' in episode:
            info['episode'] = float(episode)
        else:
            info['episode'] = int(episode)

        if groups['version']:
            info['version'] = int(groups['version'])

        if groups['crc32']:
            info['crc32'] = groups['crc32']

        if groups['additional']:
            match = RESOLUTION.search(groups['additional'])
            if match:
                info['resolution'] = match.group(1)

    return info


def filter_existing(filelist, episodes):
    episode_set = set(x['filename'].replace("_", " ") for x in episodes)
    file_set = set(x.replace("_", " ") for x in filelist)

    found = episode_set & file_set

    return [x for x in episodes if x['filename'].replace("_", " ") in found]

def filter_missing(filelist, episodes):
    existing = filter_existing(filelist, episodes)
    return [x for x in episodes if x not in existing]


