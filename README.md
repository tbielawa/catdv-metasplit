# CatDV MetaSplit

Split individual clips out of metadata files from CatDV XML exports
into individual files.

## Usage

    usage: split_catdv_clips.py [-h] [-d] [-f] [-o OUT] source

    Split CatDV XML files into chunks

    positional arguments:
    source             Path to the master XML source file to split

    optional arguments:
    -h, --help         show this help message and exit
    -d, --debug        Enables debug information printing
    -f, --force        Overwrite destination clip files if they already exist
    -o OUT, --out OUT  Path of the location to store the split-out clip files in
                       default: ./clips/, will be created automatically

**Simplest Use Case**

    split_catdv_clips.py -o /tmp/splitter ./source/MasterSourceMetadata.xml
    12252 clips to write out...
    ..........................................................................
    ...

    All done. Your 12252 clips are located in: /tmp/splitter


By **default** the split out clip files will be written into
``./clips/``. This directory will be *created automatically* if it
does not exist.

To prevent some accidents from happening the script will **refuse to
operate** if it detects that a destination clip file **already
exists**. The following message will appear if this happens to you:

    $ ./split_catdv_clips.py -o /tmp/splitter ./source/MasterSourceMetadata.xml
    12252 clips to write out...
    [ERROR] Destination clip file already exists: /tmp/splitter/WRAL_1_SD_Air.mp4.xml
    [INFO] Run this script again with the --force option to overwrite existing files

Per **the instructions in the error message**, all you have to do is
use the ``--force`` option to continue. Or, should you choose to do
so, you may delete all the previously generated clip files.
