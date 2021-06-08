import os
import argparse
import urllib.request
import subprocess
from platform import system

OSNAME = system().lower()
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'
TMP_FILENAME = '/tmp/find_good_wallpaper'
URL = "https://source.unsplash.com/1600x900/?nature,water"
URL = "https://source.unsplash.com/1920x1080/?abstract"
DEST_DIR = "wallpapers"
OPEN_PROGRAM = "feh @"

class Options:
    def __init__(self):
        self.dest_dir = ""
        self.tmp_filename = ""
        self.url = ""
        self.open_tmp_file_enabled = False
        self.open_program = ""

def get_open_command(filepath):
    if 'windows' in OSNAME:
        opener = 'start'
    elif 'osx' in OSNAME or 'darwin' in OSNAME:
        opener = 'open'
    else:
        opener = 'xdg-open'
    return '{opener} {filepath}'.format(opener=opener, filepath=filepath)


def init_url_lib():
    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent', USER_AGENT)]
    urllib.request.install_opener(opener)


def download(image_url, filename):
    filename, headers = urllib.request.urlretrieve(image_url, filename)
    print("retrieved", image_url)


def run_program(program):
    # subprocess.run([program], check=True)
    os.system(program)


def create_open_program(opts):
    if opts.open_program == "":
        return get_open_command(opts.tmp_filename)
    if opts.open_program.find("@") == -1:
        return opts.open_program + " " + opts.tmp_filename
    else:
        return opts.open_program.replace("@", opts.tmp_filename)


def open_tmp_file(options):
    if options.open_tmp_file_enabled is False:
        return
    program = create_open_program(options)
    run_program(program)


def main(options):
    init_url_lib()
    download(options.url, options.tmp_filename)
    open_tmp_file(options)


def create_options(args):
    o = Options()
    o.dest_dir = args.get("dest_dir", DEST_DIR)
    o.tmp_filename = args.get("tmp_filename", TMP_FILENAME)
    o.url = args.get("url", URL)
    o.open_tmp_file_enabled = True
    o.open_program = ""
    return o


if __name__ == "__main__":
    opts = create_options({})
    main(opts)
