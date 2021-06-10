# find_good_wallpaper
Console script to search for wallpaper on unsplash (or other source) save it to specific folder or discard it

```
usage: find_good_wallpaper.py [-h] [-u [URL]] [-s [SPLASH]] [-d [DEST]] [-f [FILE]] [-p PROG]

It downloads image from internet, saves it to temporary file, opens downloaded file in external application, waits until you close this app and gives you the option to copy it to the
destination dir, or to download another one and repeat the cycle

optional arguments:
  -h, --help            show this help message and exit
  -u [URL], --url [URL]
                        Url to query for images. if --splash and --url is not set --url will be (default: https://source.unsplash.com/random/)
  -s [SPLASH], --splash [SPLASH]
                        This is the last part of the source.unsplash query, for example (1920x1080/?abstract). You can ommit --url option and url will be created with --splash instead.
                        Can not be used if --url specified
  -d [DEST], --dest [DEST]
                        destination directory for accepted images (default .)
  -f [FILE], --file [FILE]
                        temporary file where images will be downloaded. It will be overwritten each download. (default /tmp/maybe-good-wallpaper)
  -p PROG, --prog PROG  program to open downloaded images. Format: program @ ,where @ is a placeholder for temp file (--file option) If not set system handler will be used
  ```
# Workflow  
For example, to load image from ```https://source.unsplash.com/1920x1080/?nature,abstract``` and open it in ```feh```.
```
python find_good_wallpaper.py -s 1920x1080/?nature,abstract -p "feh @" -d my-wallpapers-dir
```

Then you need to close feh and return to terminal. You will be asked:
```
Type s <filename> to save | n to load next | u <url> to change url | sp <splash> to change splash | q to exit
```

You can type one of the commands, for example ```s best-wallpaper-ever``` will copy tmp file to ``` my-wallpapers-dir/best-wallpaper-ever```

If you do not specify extension for the file it will be determined automatically

