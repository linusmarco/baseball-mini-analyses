import os
import urllib.request as rq
import zipfile as zf


RETROSHEET_EVENTS = "http://www.retrosheet.org/events/{}eve.zip"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def download(url, file):
    f = rq.urlretrieve(url, file)


def unzip(path):
    with zf.ZipFile(path, 'r') as z:
        z.extractall(os.path.split(path)[0])


def main():
    mkdir(DATA_DIR)

    url = RETROSHEET_EVENTS.format(2016)
    file = os.path.join(DATA_DIR, os.path.basename(url))
    download(url, file)
    unzip(file)


if (__name__ == "__main__"):
    main()