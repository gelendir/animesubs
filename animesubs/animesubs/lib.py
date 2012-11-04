import re

REGEX = re.compile(
    r"^\[(.*?)\](.*?)[ _]-[ _](\d+)(v(\d+))?"
)

def info_from_filename(filename):

    info = {}

    match = REGEX.match(filename)
    if match:
        info['subber'] = match.group(1).strip()
        info['anime'] = match.group(2).replace("_", " ").strip()
        info['episode'] = int(match.group(3))
        version = match.group(5)
        if version:
            info['version'] = int(version)

    return info
