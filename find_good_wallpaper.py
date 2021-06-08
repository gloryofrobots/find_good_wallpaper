import os
import argparse
import urllib.request
import subprocess
from platform import system
import shutil

OSNAME = system().lower()
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'
TMP_FILENAME = '/tmp/find_good_wallpaper'
URL = "https://source.unsplash.com/1920x1080/?abstract"
SPLASH = "1920x1080/?abstract"
DEST_DIR = "."
OPEN_PROGRAM = ""

def random_string():
    import string
    import random # define the random module
    S = 10  # number of characters in the string
    # call random.choices() string module to find the string in Uppercase + numeric data.
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
    return str(ran)

class Options:
    def __init__(self):
        self.dest_dir = ""
        self.tmp_filename = ""
        self.url = ""
        self.open_tmp_file_enabled = False
        self.open_program = ""
        self.interactive = False

def parse_args():
    parser = argparse.ArgumentParser(
        description='It downloads image from internet, saves it to temporary file and gives you' +
                'the option to copy it to the destination dir, or to download another one'
    )

    parser.add_argument('-u', '--url', type=str, nargs='?',
                        default=URL,
                        help='Url to query for images')

    parser.add_argument('-s','--splash', type=str, nargs='?',
                        default=SPLASH,
                        help='Shortcut when downloading from unsplash. This is the last part of the source.unsplash query. Can not be used if --url specified')

    parser.add_argument('-d','--dest', type=str, nargs='?', default=DEST_DIR,
                        help='destination directory for accepted images')

    parser.add_argument('-f','--file', type=str, nargs='?',
                        default=TMP_FILENAME,
                        help='temporary file where images will be downloaded. It will be overwritten each download')

    parser.add_argument('-o', '--open', action="store_true",
                        help='If set first downloaded image will be opened by the system or by specified --program')

    parser.add_argument('-p','--prog', type=str, action="store",
                        default=OPEN_PROGRAM,
                        help='program to open downloaded images. Format: program @ ,where @ is a placeholder for destination filename(--file option)')

    parser.add_argument('-i','--inter', action="store_true",
                        help='Interactive mode. After each download receives a command to repeat, save current or exit')


    args = parser.parse_args()
    opts = Options()
    opts.dest_dir = args.dest
    opts.tmp_filename = args.file
    opts.url = args.url
    opts.open_tmp_file_enabled = args.open
    opts.open_program = args.prog
    opts.interactive = args.inter
    return opts


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
    print("downloaded", image_url)


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
    single_run()


def single_run(options):
    download(options.url, options.tmp_filename)
    open_tmp_file(options)
    interactive_run(options)

def display_prompt():
    MSG = "Type n to load next, s to save, q to exit"
    answer = input(MSG)
    return answer

def save(options):
    filename = random_string()

def interactive_run(options):
    if options.interactive is False:
        return
    while True:
        answer = display_prompt()
        if answer == "q":
            return
        elif answer == "n":
            download(options.url, options.tmp_filename)
        elif answer == "s":
            save(options)

def create_options(args):
    o = Options()
    o.dest_dir = args.get("dest_dir", DEST_DIR)
    o.tmp_filename = args.get("tmp_filename", TMP_FILENAME)
    o.url = args.get("url", URL)
    o.open_tmp_file_enabled = True
    o.open_program = ""
    return o


if __name__ == "__main__":
    opts = parse_args()
    main(opts)

