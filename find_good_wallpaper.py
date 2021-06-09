import os
import os.path
import argparse
import urllib.request
import subprocess
import sys
from platform import system
import shutil

OSNAME = system().lower()
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'
TMP_FILENAME = '/tmp/maybe-good-wallpaper'
URL = "https://source.unsplash.com/1920x1080/?abstract"
SOURCE_URL = "https://source.unsplash.com/"
SPLASH = "1920x1080/?abstract"
DEST_DIR = "."
OPEN_PROGRAM = ""

class Options:
    def __init__(self):
        self.dest_dir = ""
        self.tmp_filename = ""
        self.url = ""
        self.open_program = ""
        self.interactive = False
        self.extension = ""
        self.process = None

def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='It downloads image from internet, saves it to temporary file and gives you' +
                'the option to copy it to the destination dir, or to download another one'
    )

    parser.add_argument('-u', '--url', default="", type=str, nargs='?',
                        help='Url to query for images. if --splash and --url is not set --url will be ' + URL)

    parser.add_argument('-s','--splash', type=str, nargs='?',
                        default=SPLASH,
                        help='Shortcut when downloading from unsplash. This is the last part of the source.unsplash query. Can not be used if --url specified')

    parser.add_argument('-d','--dest', type=str, nargs='?', default=DEST_DIR,
                        help='destination directory for accepted images')

    parser.add_argument('-f','--file', type=str, nargs='?',
                        default=TMP_FILENAME,
                        help='temporary file where images will be downloaded. It will be overwritten each download')

    parser.add_argument('-p','--prog', type=str, action="store",
                        default=OPEN_PROGRAM,
                        help='program to open downloaded images. Format: program @ ,where @ is a placeholder for destination filename(--file option)')

    parser.add_argument('-i','--inter', action="store_true",
                        help='Interactive mode. After each download receives a command to repeat, save current or exit')

    parser.add_argument('-e','--extension', default="", action="store",
                        help='Extension appended to each saved file')

    return parser.parse_args()


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
    try:
        # print("Downloading: ", image_url)
        filename, headers = urllib.request.urlretrieve(image_url, filename)
        print("Downloaded: ", image_url)
    except Exception as e:
        printerr("Download error: {0}".format(e))
        raise e


def run_program(options, program):
    # if options.process != None:
    #     options.process.terminate()
    #     options.process.kill()

    # args = [arg.strip() for arg in program.split(" ")]
    #options.process =  subprocess.Popen(args)
    try:
        os.system(program)
    except Exception as e:
        printerr("Error: {0}".format(e))

def printerr(*args):
    print(*args, file=sys.stderr)


def create_open_program(opts):
    if opts.open_program == "":
        return get_open_command(opts.tmp_filename)
    if opts.open_program.find("@") == -1:
        return opts.open_program + " " + opts.tmp_filename
    else:
        return opts.open_program.replace("@", opts.tmp_filename)


def open_tmp_file(options):
    program = create_open_program(options)
    run_program(options, program)

def download_and_open(options):
    download(options.url, options.tmp_filename)
    open_tmp_file(options)

def create_url_from_splash(splash):
    return SOURCE_URL + splash

def create_options(args):
    print(args)
    opts = Options()
    opts.dest_dir = args.dest
    opts.tmp_filename = args.file
    if args.url != "" and args.splash != "":
        printerr("Both --url and --splash options are set so --splash is ignored")

    if args.url != "":
        opts.url = args.url
    elif args.url == "" and args.splash != "":
        opts.url = create_url_from_splash(args.splash)
    else:
        opts.url = URL

    opts.open_program = args.prog
    opts.interactive = args.inter
    opts.extension = args.extension
    return opts

def main():
    args = parse_args()
    options = create_options(args)

    init_url_lib()

    download_and_open(options)
    if options.interactive is False:
        return
    interactive_run(options)

def display_prompt():
    MSG = "Type s <filename> to save, type n to load next, type q to exit\n"
    answer = input(MSG)
    return answer

def save(command, options):
    filename = command[1:].strip()
    filepath = os.path.join(options.dest_dir, filename)
    if options.extension != "":
        extension = options.extension
        if extension.startswith("."):
            extension = extension[1:]
        filepath = filepath + "." + extension
    try:
        shutil.copyfile(options.tmp_filename, filepath)
        print("File saved into " + filepath)
    except Exception as err:
        printerr("Error: {0}".format(err))


def interactive_run(options):
    while True:
        answer = display_prompt()
        if answer == "q":
            return
        elif answer == "n":
            download_and_open(options)
        elif answer.startswith("s "):
            save(answer, options)
        else:
            print("wrong command!")

if __name__ == "__main__":
    try:
        main()
    except:
        printerr("Terminated")
        exit(-1)
